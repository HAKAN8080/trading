import streamlit as st
import pandas as pd

def cover_grubu_belirle(cover):
    if pd.isna(cover) or cover > 900:
        return "N/A"
    if cover < 5:
        return "0-5"
    elif cover < 9:
        return "5-9"
    elif cover < 12:
        return "9-12"
    elif cover < 15:
        return "12-15"
    elif cover < 20:
        return "15-20"
    elif cover < 25:
        return "20-25"
    elif cover < 30:
        return "25-30"
    else:
        return "30+"

def calculate_cover(stok_tl, haftalik_smm):
    """MAĞAZA stok / haftalık SMM"""
    try:
        if haftalik_smm == 0 or pd.isna(haftalik_smm) or pd.isna(stok_tl):
            return 999
        result = stok_tl / haftalik_smm
        return min(result, 999)
    except:
        return 999

def veri_yukleme_ui():
    st.title("📤 Veri Yükleme")
    st.markdown("---")
    
    st.markdown("""
    ### 📋 Veri Formatı
    Excel dosyanızda şu kolonlar olmalı:
    - Kategori, ÜMG, MG, Marka, Ürün Kodu, Ürün
    - GH Mğz Stok TL, Anlık Mğz Stok TL
    - LW Adet, LW SMM, TW Adet, TW SMM, TW İO
    - Son İlk satış Fiyatı, Son Kasa Fiyatı
    
    **Cover Hesaplama:** Mağaza Stok TL / Haftalık SMM (sadece mağaza!)
    """)
    
    uploaded_file = st.file_uploader("Excel Dosyası Yükle", type=['xlsx', 'xls'])
    
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            st.success(f"✅ {len(df):,} satır yüklendi")
            
            # Kolon temizleme
            df.columns = df.columns.str.strip()
            
            # Rename
            column_map = {
                'GH  Mğz Stok TL': 'GH Mağaza Stok TL',
                'Anlık Mğz Stok TL': 'Anlık Mağaza Stok TL',
                'Son İlk satış Fiyatı': 'İSF',
                'Son Kasa Fiyatı': 'ASF'
            }
            df = df.rename(columns=column_map)
            
            # Önizleme
            st.markdown("### 👀 Veri Önizleme")
            display_cols = ['Ürün Kodu', 'Ürün', 'Kategori', 'Marka', 'TW Adet', 'TW İO']
            display_cols = [c for c in display_cols if c in df.columns]
            st.dataframe(df[display_cols].head(10), use_container_width=True)
            
            # Metrikler
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Toplam SKU", f"{len(df):,}")
            with col2:
                st.metric("Kategori", df['Kategori'].nunique() if 'Kategori' in df.columns else 0)
            with col3:
                st.metric("Marka", df['Marka'].nunique() if 'Marka' in df.columns else 0)
            with col4:
                mgz_stok = df['Anlık Mağaza Stok TL'].sum() if 'Anlık Mağaza Stok TL' in df.columns else 0
                st.metric("Mağaza Stok", f"{mgz_stok/1e6:.1f}M TL")
            
            if st.button("🚀 Veriyi İşle ve Sisteme Yükle", type="primary", use_container_width=True):
                with st.spinner("İşleniyor..."):
                    df_processed = veri_isle(df)
                    
                    st.session_state.data_loaded = True
                    st.session_state.df_main = df_processed
                    st.session_state.data_info = {
                        'total_sku': len(df_processed),
                        'week': 'TW',
                        'date': pd.Timestamp.now().strftime('%d.%m.%Y'),
                        'filename': uploaded_file.name
                    }
                    
                    st.success("✅ Veri yüklendi!")
                    st.balloons()
                    
                    # Cover özet
                    avg_cover = df_processed['TW SS'].mean()
                    st.info(f"""
                    💡 **Cover Bilgisi:**
                    - Ortalama Cover: {avg_cover:.1f} hafta
                    - Hesaplama: Mağaza Stok TL / Haftalık SMM
                    - Hedef: 8-12 hafta
                    """)
        
        except Exception as e:
            st.error(f"❌ Hata: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
    else:
        st.info("👆 Excel dosyasını yükleyin")

def veri_isle(df):
    df = df.copy()
    df.columns = df.columns.str.strip()
    
    # SMM Birim
    if 'SMM Birim' not in df.columns:
        df['SMM Birim'] = df['TW SMM'] / df['TW Adet'].replace(0, 1)
    
    # Marj
    if 'TW Marj' not in df.columns:
        df['ASF_KDV_Haric'] = df['ASF'] / 1.20
        df['TW Marj'] = ((df['ASF_KDV_Haric'] - df['SMM Birim']) / df['ASF_KDV_Haric']) * 100
        df['TW Marj'] = df['TW Marj'].fillna(0)
    
    # ✅ COVER HESAPLAMA - SADECE MAĞAZA STOKU!
    if 'LW SS' not in df.columns:
        df['LW SS'] = df.apply(
            lambda r: calculate_cover(
                r.get('GH Mağaza Stok TL', 0),  # Sadece mağaza!
                r.get('LW SMM', 1)
            ), 
            axis=1
        )
    
    if 'TW SS' not in df.columns:
        df['TW SS'] = df.apply(
            lambda r: calculate_cover(
                r.get('Anlık Mağaza Stok TL', 0),  # Sadece mağaza!
                r.get('TW SMM', 1)
            ), 
            axis=1
        )
    
    # Toplam SS (depo + mağaza) - referans için
    if 'Toplam SS' not in df.columns:
        df['Toplam SS'] = df.apply(
            lambda r: calculate_cover(
                r.get('Anlık Toplam Stok TL', 0), 
                r.get('TW SMM', 1)
            ), 
            axis=1
        )
    
    # Gruplar
    df['LW Cover Grup'] = df['LW SS'].apply(cover_grubu_belirle)
    df['TW Cover Grup'] = df['TW SS'].apply(cover_grubu_belirle)
    
    # İndirim grup
    df['TW İO_Pct'] = df['TW İO'] * 100
    df['TW İndirim Grup'] = pd.cut(
        df['TW İO_Pct'],
        bins=[-float('inf'), 0, 30, 50, 70, float('inf')],
        labels=['Yok', '0-30%', '30-50%', '50-70%', '70%+']
    )
    
    return df
