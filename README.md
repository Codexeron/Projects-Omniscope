# 🏛️ OmniScope - Web Sitesi Analiz Motoru

**OmniScope**, bir web sitesini **6 farklı mühendislik ekseninde** analiz eden, kurulumu tek satırda biten, dosya sayısı abartılmamış (sadece 7 dosya) ve her kullanıcının kendi bilgisayarını bağımsız bir sunucu (API) gibi kullanabildiği hafif bir mikro-servis çözümüdür.

> 🎯 **Slogan:** *"Herkesin bilgisayarı, kendi güvenlikli analiz kulesi olsun."*

---

## 🚀 Özellikler (Feature Set)

| Eksen | Açıklama | Ölçütler |
| :--- | :--- | :--- |
| ⚡ **Performans** | Sayfa yüklenme hızı ve ağırlık | TTFB, Toplam Boyut (kb), Gzip sıkıştırması |
| 🔒 **Güvenlik** | Güvenlik başlıkları ve SSL sağlığı | SSL geçerliliği, HSTS, X-Frame-Options, X-Content-Type |
| 📈 **SEO** | Arama motoru optimizasyon temelleri | Title etiketi (uzunluk), Meta Description, H1 etiketi varlığı |
| ♿ **Erişilebilirlik (A11Y)** | Kapsayıcı web standartları | Alt etiketleri, HTML Lang niteliği, ARIA label kullanımı |
| 🧹 **İyi Uygulamalar** | Modern web kod standartları | Doctype, Charset bildirimi, Inline CSS/JS yoğunluğu |
| 🌿 **Eko-Skor** | Çevresel ayak izi simülasyonu | Tahmini CO₂ emisyonu (sayfa boyutuna göre) |

---

## 📦 Gereksinimler (Requirements)

- **Python 3.11** veya üzeri
- İnternet bağlantısı (kurulum ve analiz için)
- İşletim Sistemi: Windows / macOS / Linux (Tam platform bağımsız)

---

## ⚙️ Kurulum (Installation)

Projeyi kurmak, **sadece 1 komut** ve **tamamen otomatiktir**. Elinizle hiçbir bağımlılık kurmanıza, test yapmanıza veya sanal environment ile uğraşmanıza gerek yoktur.

1. Terminali açın ve proje dizinine gidin.
2. Aşağıdaki sihri çalıştırın:

```bash
python setup.py
