# 💄 EVE KOZMETİK - STOK & BÜTÇE ANALİZ SİSTEMİ

Kapsamlı retail analytics platformu - Cover analizi, bütçe takibi ve elastikiyet bazlı indirim optimizasyonu.

## 🎯 Özellikler

- 📊 CEO Dashboard (Executive Summary)
- 📦 Cover Analizi (Stok dönüş hızı)
- 💰 Bütçe Analizi (Budget vs Actual)
- 🎯 İndirim Optimizasyonu (Elastikiyet bazlı)
- ⚙️ Elastikiyet Yönetimi (Kategori bazlı)

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+

### Adımlar
```bash
# 1. Repository'yi indir ve aç
unzip eve-kozmetik-analiz.zip
cd eve-kozmetik-analiz

# 2. Bağımlılıkları yükle
pip install -r requirements.txt

# 3. Uygulamayı başlat
streamlit run app/main.py
```

Tarayıcı otomatik açılacak: `http://localhost:8501`

## 📁 Proje Yapısı

```
eve-kozmetik-analiz/
├── app/                    # Ana uygulama
│   ├── main.py            # Navigation
│   ├── config.py          # Ayarlar
│   └── utils.py           # Yardımcı fonksiyonlar
├── modules/                # Modüller
│   ├── veri_yukleme/      # Veri yükleme
│   ├── elastikiyet/       # Elastikiyet yönetimi
│   ├── dashboard/         # Dashboard'lar
│   └── ...
├── data/                   # Veri klasörü
│   ├── config/            # Config dosyaları
│   └── sample/            # Örnek veriler
├── docs/                   # Dokümantasyon
└── tests/                  # Test dosyaları
```

## 📖 Kullanım

### 1. Veri Yükleme
1. Sol menüden **"📤 Veri Yükleme"** seç
2. Excel/CSV yükle
3. **"🚀 İşle ve Yükle"**

### 2. Elastikiyet Ayarları
1. **"⚙️ Elastikiyet Yönetimi"**
2. Kategorilere değer gir
3. Kaydet

### 3. Dashboard'ı Görüntüle
- **"📊 CEO Dashboard"** ile başla
- Diğer modüller geliştiriliyor...

## 📊 Veri Formatı

### Zorunlu Kolonlar
```
Ürün Kodu, Ürün, Kategori, ÜMG, MG, Marka
GH Mağaza Stok TL, Anlık Mağaza Stok TL
LW Adet, LW SMM, TW Adet, TW SMM
TW İO, TW Marj, İSF, ASF, SMM Birim
```

## ⚙️ Konfigürasyon

### Elastikiyet
`data/config/elastikiyet_config.json`

### Global Ayarlar
`app/config.py`

## 🧪 Test

```bash
pytest tests/
```

## 📈 Gelecek Özellikler

- [ ] Otomatik elastikiyet öğrenme
- [ ] Price scraper
- [ ] Satış tahmini (Prophet)
- [ ] PDF/Excel export
- [ ] Email raporlama

## 📝 Notlar

Bu sistem **beta** versiyonudur. Ana modüller:
- ✅ Veri Yükleme
- ✅ Elastikiyet Yönetimi  
- ✅ Basit Dashboard
- 🚧 Cover Analizi (geliştiriliyor)
- 🚧 Bütçe Analizi (geliştiriliyor)
- 🚧 İndirim Optimizasyonu (geliştiriliyor)

## 📞 İletişim

EVE Kozmetik Retail Analytics Team

---
**Made with ❤️ for EVE Kozmetik**
