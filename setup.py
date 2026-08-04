import os
import sys
import subprocess
import venv
import shutil

def main():
    print("🚀 OmniScope Kurulum Başlatılıyor...")
    
    venv_dir = "venv"
    if not os.path.exists(venv_dir):
        print("📦 Sanal environment oluşturuluyor...")
        venv.create(venv_dir, with_pip=True)
    else:
        print("✅ Sanal environment mevcut.")
    
    # Pip ve python yolları
    if os.name == "nt":
        pip_path = os.path.join(venv_dir, "Scripts", "pip.exe")
        python_path = os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        pip_path = os.path.join(venv_dir, "bin", "pip")
        python_path = os.path.join(venv_dir, "bin", "python")
    
    # Pip upgrade'ı atla, direkt bağımlılıkları yükle (uyarıyı bastır)
    print("📥 Bağımlılıklar yükleniyor (bu 20 saniye sürebilir)...")
    subprocess.run([pip_path, "install", "--upgrade", "pip"], check=False, capture_output=True)  # hata çıksa da devam
    subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
    
    # Test çalıştır
    print("🧪 Otomatik test başlatılıyor (sizin test yapmanıza gerek yok)...")
    result = subprocess.run([python_path, "test_runner.py"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("❌ Test başarısız! Lütfen internet bağlantınızı kontrol edin.")
        print(result.stderr)
        sys.exit(1)
    else:
        print("✅ TÜM TESTLER GEÇTİ. OmniScope kullanıma hazır!")
        print("\n💡 Kullanım:")
        print("   - API Sunucusu: python omniscope.py")
        print("   - CLI: python omniscope.py https://orneksite.com --json")

if __name__ == "__main__":
    main()
