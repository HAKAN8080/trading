import streamlit as st
from pathlib import Path
import sys

# Path setup - Streamlit Cloud için düzeltildi
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def main():
    st.set_page_config(
        page_title="EVE Kozmetik",
        page_icon="💄",
        layout="wide"
    )
    
    st.sidebar.title("📊 EVE KOZMETİK")
    
    # Veri durumu göster
    if 'data_loaded' in st.session_state and st.session_state.data_loaded:
        st.sidebar.success("✅ Veri Yüklendi")
        if 'data_info' in st.session_state:
            info = st.session_state.data_info
            st.sidebar.info(f"""
            **Veri Bilgisi:**
            - SKU: {info.get('total_sku', 0):,}
            - Tarih: {info.get('date', 'N/A')}
            """)
    else:
        st.sidebar.warning("⚠️ Veri Yüklenmedi")
    
    st.sidebar.markdown("---")
    
    menu = st.sidebar.radio("Menü", [
        "🏠 Ana Sayfa",
        "📤 Veri Yükleme",  
        "📊 CEO Dashboard",
        "⚙️ Elastikiyet Yönetimi"
    ])
    
    if menu == "🏠 Ana Sayfa":
        home_page()
    elif menu == "📤 Veri Yükleme":
        try:
            from modules.veri_yukleme.veri_yukleme import veri_yukleme_ui
            veri_yukleme_ui()
        except ImportError as e:
            st.error(f"❌ Veri Yükleme modülü bulunamadı: {e}")
            st.info("Modül dosyaları eksik olabilir. GitHub'daki dosyaları kontrol edin.")
    elif menu == "📊 CEO Dashboard":
        try:
            from modules.dashboard.executive_dashboard import executive_dashboard_ui
            executive_dashboard_ui()
        except ImportError as e:
            st.error(f"❌ Dashboard modülü bulunamadı: {e}")
            st.info("Modül dosyaları eksik olabilir. GitHub'daki dosyaları kontrol edin.")
    elif menu == "⚙️ Elastikiyet Yönetimi":
        try:
            from modules.elastikiyet.elastikiyet_yonetimi import elastikiyet_yonetimi_ui
            elastikiyet_yonetimi_ui()
        except ImportError as e:
            st.error(f"❌ Elastikiyet modülü bulunamadı: {e}")
            st.info("Modül dosyaları eksik olabilir. GitHub'daki dosyaları kontrol edin.")
    else:
        st.info("🚧 Bu modül yakında eklenecek!")

def home_page():
    st.title("💄 EVE KOZMETİK")
    st.header("Stok & Bütçe Analiz Sistemi")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Modüller", "4", "Aktif")
    
    with col2:
        st.metric("Kategoriler", "25+", "Elastikiyet Tanımlı")
    
    with col3:
        st.metric("Versiyon", "1.0.0", "Beta")
    
    st.markdown("---")
    
    st.markdown("""
    ## 🎯 Sistem Özellikleri
    
    ### 📤 Veri Yükleme
    - Excel dosyası yükleme
    - Otomatik cover hesaplama
    - Marj hesaplama
    
    ### ⚙️ Elastikiyet Yönetimi
    - Kategori bazlı elastikiyet tanımlama
    - Canlı düzenleme
    - Örnek hesaplamalar
    
    ### 📊 CEO Dashboard
    - Genel metrikler
    - SKU istatistikleri
    - Performans göstergeleri
    
    ## 🚀 Başlangıç
    
    1. Sol menüden **"📤 Veri Yükleme"** seç
    2. Excel dosyanı yükle
    3. **"🚀 İşle ve Yükle"** butonuna tıkla
    4. Dashboard'ları kullan!
    """)
    
    st.markdown("---")
    st.info("💡 **İpucu:** Veri yükleme yapana kadar Elastikiyet Yönetimi'ni kullanabilirsin.")

if __name__ == "__main__":
    main()
