import streamlit as st
import pandas as pd
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.config import APP_CONFIG
from app.utils import validate_dataframe, cover_grubu_belirle, calculate_cover

def veri_yukleme_ui():
    st.title("📤 Veri Yükleme")
    st.markdown("---")
    
    st.markdown("""
    ### Zorunlu Kolonlar
    Ürün Kodu, Ürün, Kategori, ÜMG, MG, Marka, GH Mağaza Stok TL,
    Anlık Mağaza Stok TL, LW Adet, LW SMM, TW Adet, TW SMM, TW İO, TW Marj,
    İSF, ASF, SMM Birim
    """)
    
    uploaded_file = st.file_uploader("Excel/CSV Yükle", type=['xlsx', 'csv'])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ {len(df):,} satır yüklendi")
            
            required_cols = APP_CONFIG['zorunlu_kolonlar']
            is_valid, missing = validate_dataframe(df, required_cols)
            
            if not is_valid:
                st.error(f"❌ Eksik: {', '.join(missing)}")
                return
            
            st.dataframe(df.head(10))
            
            if st.button("🚀 İşle ve Yükle", type="primary"):
                df = veri_isle(df)
                st.session_state.data_loaded = True
                st.session_state.df_main = df
                st.success("✅ Veri yüklendi!")
                st.balloons()
        
        except Exception as e:
            st.error(f"❌ Hata: {e}")

def veri_isle(df):
    df = df.copy()
    
    if 'LW SS' not in df.columns:
        df['LW SS'] = df.apply(
            lambda r: calculate_cover(r.get('GH Mağaza Stok TL', 0), r.get('LW SMM', 1)),
            axis=1
        )
    
    if 'TW SS' not in df.columns:
        df['TW SS'] = df.apply(
            lambda r: calculate_cover(r.get('Anlık Mağaza Stok TL', 0), r.get('TW SMM', 1)),
            axis=1
        )
    
    df['LW Cover Grup'] = df['LW SS'].apply(cover_grubu_belirle)
    df['TW Cover Grup'] = df['TW SS'].apply(cover_grubu_belirle)
    
    return df
