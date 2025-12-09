import json
from pathlib import Path

class ElastikiyetMotoru:
    def __init__(self, config_path='data/config/elastikiyet_config.json'):
        self.config_path = Path(config_path)
        self.elastikiyet_tablosu = self.yukle()
    
    def yukle(self):
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self.default_degerler()
    
    def kaydet(self):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.elastikiyet_tablosu, f, ensure_ascii=False, indent=2)
    
    def default_degerler(self):
        return {
            'MASKARA': {'elastikiyet': 3.5, 'optimal_indirim': 60, 'max_indirim': 75, 'aciklama': 'Orta elastik', 'kategori_adi': 'Maskara'},
            'FAR': {'elastikiyet': 4.2, 'optimal_indirim': 55, 'max_indirim': 70, 'aciklama': 'Yüksek elastik', 'kategori_adi': 'Far'},
            'RUJ': {'elastikiyet': 4.0, 'optimal_indirim': 57, 'max_indirim': 72, 'aciklama': 'Yüksek elastik', 'kategori_adi': 'Ruj'},
            'FONDOTEN': {'elastikiyet': 2.8, 'optimal_indirim': 50, 'max_indirim': 65, 'aciklama': 'Düşük elastik', 'kategori_adi': 'Fondöten'},
            'DEFAULT': {'elastikiyet': 3.5, 'optimal_indirim': 55, 'max_indirim': 70, 'aciklama': 'Varsayılan', 'kategori_adi': 'Varsayılan'}
        }
    
    def kategori_getir(self, mg_kategori):
        kategori_ust = mg_kategori.upper() if isinstance(mg_kategori, str) else 'DEFAULT'
        return self.elastikiyet_tablosu.get(kategori_ust, self.elastikiyet_tablosu['DEFAULT'])
    
    def satis_tahmini(self, mevcut_satis, mevcut_indirim, yeni_indirim, elastikiyet):
        indirim_degisim = (yeni_indirim - mevcut_indirim) / max(mevcut_indirim, 1)
        satis_degisim_oran = indirim_degisim * elastikiyet
        yeni_satis = max(0, mevcut_satis * (1 + satis_degisim_oran))
        
        return {
            'yeni_satis': int(yeni_satis),
            'satis_artis': int(yeni_satis - mevcut_satis),
            'satis_artis_oran': satis_degisim_oran * 100
        }
