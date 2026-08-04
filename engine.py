import asyncio
import time
import re
from abc import ABC, abstractmethod
from urllib.parse import urlparse, urljoin
from typing import Dict, Any, List, Optional
from datetime import datetime

import httpx
from bs4 import BeautifulSoup
import validators

# --- Güvenlik: SSRF ve Tehlikeli URL Engelleme ---
FORBIDDEN_NETWORKS = ["127.0.0.1", "localhost", "0.0.0.0", "::1", "10.", "172.16.", "192.168."]

def validate_url(url: str) -> bool:
    if not validators.url(url):
        return False
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    for blocked in FORBIDDEN_NETWORKS:
        if hostname.startswith(blocked):
            return False
    return True

async def fetch_context(url: str) -> Dict[str, Any]:
    if not validate_url(url):
        return {"error": "Güvensiz veya geçersiz URL", "status_code": 400}
    
    context = {
        "url": url,
        "headers": {},
        "html": "",
        "response_time": 0.0,
        "content_length": 0,
        "status_code": 0,
        "ssl_info": {"valid": False, "issuer": None}
    }
    
    try:
        start = time.perf_counter()
        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=httpx.Timeout(5.0, connect=2.0),
            verify=True
        ) as client:
            resp = await client.get(url, headers={"User-Agent": "OmniScope/1.0"})
            elapsed = time.perf_counter() - start
            
            context["status_code"] = resp.status_code
            context["headers"] = dict(resp.headers)
            context["html"] = resp.text
            context["content_length"] = len(resp.content)
            context["response_time"] = round(elapsed, 3)
            context["ssl_info"]["valid"] = True
    except httpx.TimeoutException:
        context["error"] = "Zaman aşımı (5 sn)"
    except httpx.SSLProtocolError:
        context["error"] = "SSL sertifika hatası"
        context["ssl_info"]["valid"] = False
    except Exception as e:
        context["error"] = f"Fetch hatası: {str(e)}"
    
    return context

# --- Base Analyzer ---
class BaseAnalyzer(ABC):
    @abstractmethod
    def analyze(self, context: Dict[str, Any]) -> Dict[str, Any]:
        pass

# 1. Performans
class PerformanceAnalyzer(BaseAnalyzer):
    def analyze(self, context):
        ttfb = context.get("response_time", 0)
        size_kb = context.get("content_length", 0) / 1024
        headers = context.get("headers", {})
        is_gzip = any("gzip" in v.lower() for k, v in headers.items() if k.lower() == "content-encoding")
        
        score_ttfb = max(0, 100 - (ttfb * 100)) if ttfb > 0 else 50
        score_size = max(0, 100 - (size_kb / 10)) if size_kb > 0 else 50
        score_gzip = 20 if is_gzip else 0
        final_score = round(min(100, (score_ttfb * 0.5) + (score_size * 0.3) + score_gzip), 2)
        
        return {
            "score": min(100, final_score),
            "details": {
                "ttfb_seconds": ttfb,
                "total_size_kb": round(size_kb, 2),
                "is_gzip": is_gzip
            }
        }

# 2. Güvenlik
class SecurityAnalyzer(BaseAnalyzer):
    def analyze(self, context):
        headers = context.get("headers", {})
        ssl_valid = context.get("ssl_info", {}).get("valid", False)
        hsts = headers.get("strict-transport-security") is not None
        xframe = headers.get("x-frame-options") is not None
        xcontent = headers.get("x-content-type-options") is not None
        
        score = 0
        if ssl_valid: score += 40
        if hsts: score += 20
        if xframe: score += 20
        if xcontent: score += 20
        
        return {
            "score": min(100, score),
            "details": {
                "ssl_valid": ssl_valid,
                "has_hsts": hsts,
                "has_xframe": xframe,
                "has_xcontent_type": xcontent
            }
        }

# 3. SEO
class SeoAnalyzer(BaseAnalyzer):
    def analyze(self, context):
        html = context.get("html", "")
        soup = BeautifulSoup(html, "lxml") if html else None
        if not soup:
            return {"score": 0, "details": {"error": "HTML parse edilemedi"}}
        
        title_tag = soup.find("title")
        title = title_tag.text.strip() if title_tag else ""
        has_title = bool(title)
        title_len = len(title)
        
        meta_desc = soup.find("meta", attrs={"name": "description"})
        desc = meta_desc.get("content", "").strip() if meta_desc else ""
        has_meta = bool(desc)
        meta_len = len(desc)
        
        h1_tags = soup.find_all("h1")
        has_h1 = len(h1_tags) > 0
        
        score = 0
        if has_title and 30 <= title_len <= 60: score += 40
        elif has_title: score += 20
        
        if has_meta and 50 <= meta_len <= 160: score += 40
        elif has_meta: score += 20
        
        if has_h1: score += 20
        
        return {
            "score": min(100, score),
            "details": {
                "has_title": has_title,
                "title_length": title_len,
                "has_meta_description": has_meta,
                "meta_description_length": meta_len,
                "has_h1": has_h1,
                "h1_count": len(h1_tags)
            }
        }

# 4. Erişilebilirlik
class AccessibilityAnalyzer(BaseAnalyzer):
    def analyze(self, context):
        html = context.get("html", "")
        soup = BeautifulSoup(html, "lxml") if html else None
        if not soup:
            return {"score": 0, "details": {"error": "HTML parse edilemedi"}}
        
        imgs = soup.find_all("img")
        imgs_with_alt = [i for i in imgs if i.get("alt") is not None and i["alt"].strip() != ""]
        img_score = (len(imgs_with_alt) / len(imgs) * 50) if imgs else 50
        
        lang = soup.html.get("lang") if soup.html else None
        lang_score = 30 if lang else 0
        
        aria_labels = soup.find_all(attrs={"aria-label": True})
        aria_score = 20 if len(aria_labels) > 0 else 0
        
        final = min(100, img_score + lang_score + aria_score)
        return {
            "score": round(final, 2),
            "details": {
                "total_images": len(imgs),
                "images_with_alt": len(imgs_with_alt),
                "has_lang_attr": bool(lang),
                "has_aria_labels": len(aria_labels) > 0
            }
        }

# 5. Best Practices
class BestPracticesAnalyzer(BaseAnalyzer):
    def analyze(self, context):
        html = context.get("html", "")
        soup = BeautifulSoup(html, "lxml") if html else None
        if not soup:
            return {"score": 0, "details": {"error": "HTML parse edilemedi"}}
        
        doctype = bool(re.search(r'<!doctype\s+html', html, re.IGNORECASE))
        charset = soup.find("meta", attrs={"charset": True}) or soup.find("meta", attrs={"http-equiv": "Content-Type"})
        style_tags = soup.find_all("style")
        script_tags = soup.find_all("script")
        
        score = 0
        if doctype: score += 30
        if charset: score += 30
        if len(style_tags) <= 2: score += 20
        if len(script_tags) <= 5: score += 20
        
        return {
            "score": min(100, score),
            "details": {
                "has_doctype": doctype,
                "has_charset": bool(charset),
                "inline_style_count": len(style_tags),
                "inline_script_count": len(script_tags)
            }
        }

# 6. Eko
class EcoAnalyzer(BaseAnalyzer):
    def analyze(self, context):
        size_kb = context.get("content_length", 0) / 1024
        if size_kb <= 0:
            score = 100
        else:
            score = max(0, 100 - (size_kb * 0.05))
        return {
            "score": round(min(100, score), 2),
            "details": {
                "estimated_co2_g": round(size_kb * 0.0018, 3),
                "page_size_kb": round(size_kb, 2)
            }
        }

# 7. YENİ: Kırık Bağlantı (Broken Link) Analizi
class BrokenLinkAnalyzer(BaseAnalyzer):
    def analyze(self, context):
        html = context.get("html", "")
        soup = BeautifulSoup(html, "lxml") if html else None
        if not soup:
            return {"score": 0, "details": {"error": "HTML parse edilemedi"}}
        
        base_url = context.get("url", "")
        links = soup.find_all("a", href=True)
        total_links = len(links)
        
        if total_links == 0:
            return {"score": 100, "details": {"total_links": 0, "broken_links": 0, "broken_urls": []}}
        
        # Sadece ilk 20 linki kontrol et (performans için)
        check_links = links[:20]
        broken = []
        
        # Senkron kontrol (basitlik için)
        import requests
        for link in check_links:
            href = link.get("href", "")
            if href.startswith("#") or href.startswith("javascript:"):
                continue
            full_url = urljoin(base_url, href)
            try:
                resp = requests.head(full_url, timeout=3, allow_redirects=True)
                if resp.status_code >= 400:
                    broken.append(full_url)
            except:
                broken.append(full_url)
        
        broken_count = len(broken)
        # Skor: Her kırık link %5 düşürür (max 100)
        score = max(0, 100 - (broken_count * 5))
        
        return {
            "score": round(score, 2),
            "details": {
                "total_links": total_links,
                "broken_links": broken_count,
                "broken_urls": broken[:10]  # İlk 10 kırık linki göster
            }
        }

# 8. YENİ: Mobil Uyumluluk (Mobile Friendly) Analizi
class MobileFriendlyAnalyzer(BaseAnalyzer):
    def analyze(self, context):
        html = context.get("html", "")
        soup = BeautifulSoup(html, "lxml") if html else None
        if not soup:
            return {"score": 0, "details": {"error": "HTML parse edilemedi"}}
        
        score = 0
        details = {}
        
        # 1. Viewport meta etiketi var mı?
        viewport = soup.find("meta", attrs={"name": "viewport"})
        has_viewport = viewport is not None
        if has_viewport:
            score += 30
            details["has_viewport"] = True
            details["viewport_content"] = viewport.get("content", "")
        else:
            details["has_viewport"] = False
        
        # 2. Responsive CSS (media query) var mı? (style etiketlerinde veya inline)
        style_tags = soup.find_all("style")
        has_media_query = False
        for style in style_tags:
            if style.string and "@media" in style.string:
                has_media_query = True
                break
        
        # Ayrıca link etiketlerinde CSS dosyaları kontrol et (basit)
        link_tags = soup.find_all("link", rel="stylesheet")
        for link in link_tags:
            href = link.get("href", "")
            if href and ".css" in href:
                has_media_query = True  # Varsayalım ki harici CSS responsive içeriyor (kabül)
                break
        
        if has_media_query:
            score += 30
            details["has_media_query"] = True
        else:
            details["has_media_query"] = False
        
        # 3. Görseller responsive mi? (img etiketlerinde width/height yüzde mi?)
        imgs = soup.find_all("img")
        responsive_images = 0
        for img in imgs:
            width = img.get("width", "")
            height = img.get("height", "")
            if "%" in str(width) or "%" in str(height) or "max-width: 100%" in str(img.get("style", "")):
                responsive_images += 1
        
        img_score = (responsive_images / len(imgs) * 40) if imgs else 40
        details["total_images"] = len(imgs)
        details["responsive_images"] = responsive_images
        
        score += min(40, img_score)
        
        return {
            "score": round(min(100, score), 2),
            "details": details
        }

# --- Orkestratör ---
class OmniOrchestrator:
    def __init__(self):
        self.analyzers: List[BaseAnalyzer] = [
            PerformanceAnalyzer(),
            SecurityAnalyzer(),
            SeoAnalyzer(),
            AccessibilityAnalyzer(),
            BestPracticesAnalyzer(),
            EcoAnalyzer(),
            BrokenLinkAnalyzer(),      # YENİ
            MobileFriendlyAnalyzer()   # YENİ
        ]
    
    async def analyze(self, url: str):
        from models import OmniReport
        context = await fetch_context(url)
        
        if "error" in context and context.get("status_code") != 200:
            return OmniReport(
                meta={"target_url": url, "analyzed_at": datetime.utcnow().isoformat(), "version": "1.1.0"},
                scores={
                    "performance": 0, "security": 0, "seo": 0, "accessibility": 0,
                    "best_practices": 0, "eco_score": 0, "broken_links": 0, "mobile_friendly": 0
                },
                details={"error": context["error"]},
                status="error",
                error_msg=context["error"]
            )
        
        results = {}
        details = {}
        
        for analyzer in self.analyzers:
            result = analyzer.analyze(context)
            name = analyzer.__class__.__name__.replace("Analyzer", "").lower()
            results[name] = result["score"]
            details[name] = result["details"]
        
        # Anahtar standardizasyonu
        scores_map = {
            "performance": results.get("performance", 0),
            "security": results.get("security", 0),
            "seo": results.get("seo", 0),
            "accessibility": results.get("accessibility", 0),
            "best_practices": results.get("bestpractices", 0),
            "eco_score": results.get("eco", 0),
            "broken_links": results.get("brokenlink", 0),       # YENİ
            "mobile_friendly": results.get("mobilefriendly", 0) # YENİ
        }
        
        if "bestpractices" in details:
            details["best_practices"] = details.pop("bestpractices")
        
        return OmniReport(
            meta={"target_url": url, "analyzed_at": datetime.utcnow().isoformat(), "version": "1.1.0"},
            scores=scores_map,
            details=details,
            status="success"
        )
