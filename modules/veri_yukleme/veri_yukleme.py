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
    ### 📋 Veri Formatı
    Excel dosyanızda şu kolonlar olmalı:
    - Kategori, ÜMG, MG, Marka
    - Ürün Kodu, Ürün
    - GH Mğz Stok TL, Anlık Mğz Stok TL
    - LW Adet, LW SMM, TW Adet, TW SMM, TW İO
    - Son İlk satış Fiyatı, Son Kasa Fiyatı
    
    **NOT:** Sistem otomatik olarak TW Marj ve SMM Birim hesaplayacak.
    """)
    
    st.markdown("---")
    
    uploaded_file = st.file_uploader("Excel Dosyası Yükle", type=['xlsx', 'xls'])
    
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ {len(df):,} satır yüklendi")
            
            # Kolon isimlerini temizle (boşlukları kaldır)
            df.columns = df.columns.str.strip()
            
            # Kolon isimleri mapping
            column_mapping = {
                'Kategori': 'Kategori',
                'Marka': 'Marka',
                'Ürün': 'Ürün',
                'GH  Mğz Stok TL': 'GH Mağaza Stok TL',
                'Anlık Mğz Stok TL': 'Anlık Mağaza Stok TL',
                'Son İlk satış Fiyatı': 'İSF',
                'Son Kasa Fiyatı': 'ASF',
                'Anlık Toplam Stok TL': 'Anlık Toplam Stok TL'
            }
            
            # Rename
            df = df.rename(columns=column_mapping)
            
            # Önizleme
            st.markdown("### 👀 Veri Önizleme")
            
            # Seçili kolonları göster
            display_cols = [
                'Ürün Kodu', 'Ürün', 'Kategori', 'Marka', 'MG',
                'Anlık Mağaza Stok TL', 'TW Adet', 'TW İO', 'İSF', 'ASF'
            ]
            display_cols = [c for c in display_cols if c in df.columns]
            
            st.dataframe(df[display_cols].head(10), use_container_width=True)
            
            # İstatistikler
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Toplam SKU", f"{len(df):,}")
            
            with col2:
                kategoriler = df['Kategori'].nunique() if 'Kategori' in df.columns else 0
                st.metric("Kategori", kategoriler)
            
            with col3:
                markalar = df['Marka'].nunique() if 'Marka' in df.columns else 0
                st.metric("Marka", markalar)
            
            with col4:
                toplam_stok = df['Anlık Toplam Stok TL'].sum() if 'Anlık Toplam Stok TL' in df.columns else 0
                st.metric("Toplam Stok", f"{toplam_stok/1e6:.1f}M TL")
            
            # İşle butonu
            if st.button("🚀 Veriyi İşle ve Sisteme Yükle", type="primary", use_container_width=True):
                with st.spinner("Veri işleniyor..."):
                    df_processed = veri_isle(df)
                    
                    st.session_state.data_loaded = True
                    st.session_state.df_main = df_processed
                    st.session_state.data_info = {
                        'total_sku': len(df_processed),
                        'week': 'TW',
                        'date': pd.Timestamp.now().strftime('%d.%m.%Y'),
                        'filename': uploaded_file.name
                    }
                    
                    st.success("✅ Veri başarıyla yüklendi ve işlendi!")
                    st.balloons()
                    
                    # Özet bilgi
                    st.info(f"""
                    💡 **İşlem Özeti:**
                    - {len(df_processed):,} SKU yüklendi
                    - Cover hesaplamaları yapıldı
                    - Gruplar belirlendi
                    - Marj hesaplandı
                    
                    Şimdi **CEO Dashboard** veya **Elastikiyet Yönetimi** sayfalarını kullanabilirsin!
                    """)
        
        except Exception as e:
            st.error(f"❌ Hata: {str(e)}")
            st.exception(e)
    
    else:
        st.info("👆 Lütfen Excel dosyasını yükleyin")

def veri_isle(df):
    """Ham veriyi işle, eksik hesaplamaları yap"""
    df = df.copy()
    
    # Kolon isimlerini temizle
    df.columns = df.columns.str.strip()
    
    # SMM Birim hesapla
    if 'SMM Birim' not in df.columns:
        df['SMM Birim'] = df['TW SMM'] / df['TW Adet'].replace(0, 1)
    
    # TW Marj hesapla (KDV hariç)
    if 'TW Marj' not in df.columns:
        df['ASF_KDV_Haric'] = df['ASF'] / 1.20  # KDV %20
        df['TW Marj'] = ((df['ASF_KDV_Haric'] - df['SMM Birim']) / df['ASF_KDV_Haric']) * 100
        df['TW Marj'] = df['TW Marj'].fillna(0)
    
    # LW SS (Last Week Cover) hesapla
    if 'LW SS' not in df.columns:
        df['LW SS'] = df.apply(
            lambda r: calculate_cover(
                r.get('GH Mağaza Stok TL', 0), 
                r.get('LW SMM', 1)
            ),
            axis=1
        )
    
    # TW SS (This Week Cover) hesapla - Mağaza
    if 'TW SS' not in df.columns:
        df['TW SS'] = df.apply(
            lambda r: calculate_cover(
                r.get('Anlık Mağaza Stok TL', 0), 
                r.get('TW SMM', 1)
            ),
            axis=1
        )
    
    # Toplam SS (Toplam Stok Cover) hesapla
    if 'Toplam SS' not in df.columns:
        df['Toplam SS'] = df.apply(
            lambda r: calculate_cover(
                r.get('Anlık Toplam Stok TL', 0), 
                r.get('TW SMM', 1)
            ),
            axis=1
        )
    
    # Cover grupları belirle
    df['LW Cover Grup'] = df['LW SS'].apply(cover_grubu_belirle)
    df['TW Cover Grup'] = df['TW SS'].apply(cover_grubu_belirle)
    
    # İndirim grupları
    df['TW İndirim Grup'] = pd.cut(
        df['TW İO'] * 100,  # Yüzdeye çevir
        bins=[-float('inf'), 0, 30, 50, 70, float('inf')],
        labels=['İndirim Yok', '0-30%', '30-50%', '50-70%', '70%+']
    )
    
    # Numeric kolonları temizle
    numeric_cols = ['TW İO', 'TW Marj', 'LW SS', 'TW SS', 'Toplam SS']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    return df
