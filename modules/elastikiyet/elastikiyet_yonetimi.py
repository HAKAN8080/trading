import streamlit as st
import pandas as pd
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from modules.elastikiyet.elastikiyet_motor import ElastikiyetMotoru

def elastikiyet_yonetimi_ui():
    st.title("🎯 Elastikiyet Yönetimi")
    st.markdown("---")
    
    if 'elastikiyet_yoneticisi' not in st.session_state:
        st.session_state.elastikiyet_yoneticisi = ElastikiyetMotoru()
    
    yonetici = st.session_state.elastikiyet_yoneticisi
    
    tab1, tab2 = st.tabs(["📊 Tablo Görünümü", "➕ Yeni Kategori"])
    
    with tab1:
        st.subheader("Kategori Bazlı Elastikiyet Değerleri")
        
        df_data = []
        for key, value in yonetici.elastikiyet_tablosu.items():
            df_data.append({
                'Kod': key,
                'Kategori': value.get('kategori_adi', key),
                'Elastikiyet': value['elastikiyet'],
                'Optimal İndirim (%)': value['optimal_indirim'],
                'Max İndirim (%)': value['max_indirim']
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
        
        st.markdown("---")
        st.subheader("✏️ Kategori Düzenle")
        
        secili = st.selectbox(
            "Kategori Seç",
            list(yonetici.elastikiyet_tablosu.keys()),
            format_func=lambda x: yonetici.elastikiyet_tablosu[x].get('kategori_adi', x)
        )
        
        if secili:
            mevcut = yonetici.elastikiyet_tablosu[secili]
            
            with st.form(f"edit_{secili}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    yeni_elastikiyet = st.number_input(
                        "Elastikiyet",
                        min_value=0.1,
                        max_value=10.0,
                        value=float(mevcut['elastikiyet']),
                        step=0.1
                    )
                
                with col2:
                    yeni_optimal = st.number_input(
                        "Optimal (%)",
                        min_value=0,
                        max_value=100,
                        value=int(mevcut['optimal_indirim']),
                        step=5
                    )
                
                with col3:
                    yeni_max = st.number_input(
                        "Max (%)",
                        min_value=0,
                        max_value=100,
                        value=int(mevcut['max_indirim']),
                        step=5
                    )
                
                if st.form_submit_button("💾 Kaydet", type="primary"):
                    yonetici.elastikiyet_tablosu[secili].update({
                        'elastikiyet': yeni_elastikiyet,
                        'optimal_indirim': yeni_optimal,
                        'max_indirim': yeni_max
                    })
                    yonetici.kaydet()
                    st.success("✅ Kaydedildi!")
                    st.rerun()
    
    with tab2:
        st.subheader("➕ Yeni Kategori Ekle")
        
        with st.form("yeni_kategori"):
            yeni_kod = st.text_input("Kategori Kodu (UPPERCASE)").upper()
            yeni_ad = st.text_input("Kategori Adı")
            yeni_elastikiyet = st.number_input("Elastikiyet", value=3.5, step=0.1)
            yeni_optimal = st.number_input("Optimal (%)", value=55, step=5)
            yeni_max = st.number_input("Max (%)", value=70, step=5)
            
            if st.form_submit_button("➕ Ekle"):
                if yeni_kod and yeni_kod not in yonetici.elastikiyet_tablosu:
                    yonetici.elastikiyet_tablosu[yeni_kod] = {
                        'elastikiyet': yeni_elastikiyet,
                        'optimal_indirim': yeni_optimal,
                        'max_indirim': yeni_max,
                        'aciklama': '',
                        'kategori_adi': yeni_ad or yeni_kod
                    }
                    yonetici.kaydet()
                    st.success("✅ Eklendi!")
                    st.rerun()
                else:
                    st.error("❌ Kod boş veya mevcut!")
