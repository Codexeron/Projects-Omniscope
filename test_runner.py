import asyncio
import json
from engine import OmniOrchestrator

async def run_tests():
    print("⚡ OmniScope Test Sistemi Devrede...")
    orchestrator = OmniOrchestrator()
    
    # Test 1: Örnek site
    test_url = "https://example.com"
    print(f"🔗 Test URL: {test_url}")
    report = await orchestrator.analyze(test_url)
    
    # Zorunlu alan kontrolü
    required_keys = ["meta", "scores", "details", "status"]
    for key in required_keys:
        if key not in report.model_dump():
            print(f"❌ HATA: {key} alanı raporda eksik!")
            return False
    
    # Skorlar 0-100 arası mı?
    for k, v in report.scores.items():
        if not (0 <= v <= 100):
            print(f"❌ HATA: {k} skoru {v} (0-100 aralığında değil)")
            return False
    
    # Test 2: Geçersiz URL (güvenlik testi)
    invalid_url = "http://localhost:8080"
    report2 = await orchestrator.analyze(invalid_url)
    if report2.status != "error":
        print("❌ HATA: Localhost URL'i engellenmeliydi!")
        return False
    
    print("✅ Tüm testler başarıyla geçildi!")
    return True

if __name__ == "__main__":
    result = asyncio.run(run_tests())
    exit(0 if result else 1)
