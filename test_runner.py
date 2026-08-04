import asyncio
import json
from engine import OmniOrchestrator

async def run_tests():
    print("[TEST] OmniScope Test Sistemi Devrede...")
    orchestrator = OmniOrchestrator()
    
    # Test 1: Örnek site
    test_url = "https://facebook.com"
    print(f"[TEST] Test URL: {test_url}")
    report = await orchestrator.analyze(test_url)
    
    # Zorunlu alan kontrolü
    required_keys = ["meta", "scores", "details", "status"]
    for key in required_keys:
        if key not in report.model_dump():
            print(f"[ERROR] {key} alani raporda eksik!")
            return False
    
    # Skorlar 0-100 arası mı?
    for k, v in report.scores.items():
        if not (0 <= v <= 100):
            print(f"[ERROR] {k} skoru {v} (0-100 araliginda degil)")
            return False
    
    # Test 2: Geçersiz URL (güvenlik testi)
    invalid_url = "http://localhost:8080"
    report2 = await orchestrator.analyze(invalid_url)
    if report2.status != "error":
        print("[ERROR] Localhost URL'i engellenmeliydi!")
        return False
    
    print("[SUCCESS] Tum testler basariyla gecildi!")
    return True

if __name__ == "__main__":
    result = asyncio.run(run_tests())
    exit(0 if result else 1)
