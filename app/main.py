import streamlit as st
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.config import APP_CONFIG

def main():
    st.set_page_config(
        page_title="EVE Kozmetik",
        page_icon="💄",
        layout="wide"
    )
    
    st.sidebar.title("📊 EVE KOZMETİK")
    menu = st.sidebar.radio("Menü", [
        "🏠 Ana Sayfa",
        "📤 Veri Yükleme",  
        "📊 CEO Dashboard",
        "⚙️ Elastikiyet Yönetimi"
    ])
    
    if menu == "🏠 Ana Sayfa":
        st.title("💄 EVE KOZMETİK")
        st.header("Stok & Bütçe Analiz Sistemi")
        st.info("Sol menüden modüllere ulaşabilirsiniz.")
    elif menu == "📤 Veri Yükleme":
        from modules.veri_yukleme.veri_yukleme import veri_yukleme_ui
        veri_yukleme_ui()
    elif menu == "⚙️ Elastikiyet Yönetimi":
        from modules.elastikiyet.elastikiyet_yonetimi import elastikiyet_yonetimi_ui
        elastikiyet_yonetimi_ui()
    else:
        st.info("🚧 Bu modül yakında eklenecek!")

if __name__ == "__main__":
    main()
