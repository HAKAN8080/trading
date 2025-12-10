from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CONFIG_DIR = DATA_DIR / "config"

# Ensure directories exist
for dir_path in [DATA_DIR, CONFIG_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# App Configuration
APP_CONFIG = {
    'app_name': 'EVE Kozmetik Analiz',
    'version': '1.0.0',
    'zorunlu_kolonlar': [
        'Ürün Kodu', 'Ürün', 'Kategori', 'ÜMG', 'MG', 'Marka',
        'GH Mağaza Stok TL', 'Anlık Mağaza Stok TL',
        'LW Adet', 'LW SMM', 'TW Adet', 'TW SMM',
        'TW İO', 'İSF', 'ASF'
    ],
    'cover': {
        'hedef_min': 8,
        'hedef_max': 12,
        'kritik_seviye': 15,
        'gruplar': ['0-5', '5-9', '9-12', '12-15', '15-20', '20-25', '25-30', '30+']
    }
}

COLOR_SCHEME = {
    'kritik': '#FF4B4B',
    'uyari': '#FFA500',
    'mukemmel': '#00C851'
}

COVER_COLORS = {
    '0-5': '#FF4B4B',
    '9-12': '#00C851',
    '30+': '#FF4B4B'
}
