import streamlit as st

def executive_dashboard_ui():
    st.title("📊 CEO Dashboard")
    st.markdown("---")
    
    if 'data_loaded' not in st.session_state or not st.session_state.data_loaded:
        st.warning("⚠️ Önce veri yüklemeniz gerekiyor!")
        st.info("Sol menüden **'📤 Veri Yükleme'** sayfasına gidin.")
        return
    
    df = st.session_state.df_main
    
    st.markdown("### 📊 Genel Performans")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Toplam SKU", f"{len(df):,}")
    
    with col2:
        total_stock = df['Anlık Toplam Stok TL'].sum() if 'Anlık Toplam Stok TL' in df.columns else 0
        st.metric("Toplam Stok", f"{total_stock/1e6:.1f}M TL")
    
    with col3:
        avg_cover = df['TW SS'].mean() if 'TW SS' in df.columns else 0
        cover_emoji = "✅" if 8 <= avg_cover <= 12 else "⚠️" if avg_cover < 20 else "🔴"
        st.metric("Ort. Cover", f"{avg_cover:.1f} hafta", delta=cover_emoji)
    
    with col4:
        avg_margin = df['TW Marj'].mean() if 'TW Marj' in df.columns else 0
        st.metric("Ort. Marj", f"{avg_margin:.1f}%")
    
    st.markdown("---")
    
    # Kategori breakdown
    st.markdown("### 📦 Kategori Dağılımı")
    
    if 'Kategori' in df.columns:
        kategori_stats = df.groupby('Kategori').agg({
            'Ürün Kodu': 'count',
            'Anlık Toplam Stok TL': 'sum',
            'TW SS': 'mean',
            'TW Marj': 'mean'
        }).round(1)
        
        kategori_stats.columns = ['SKU Sayısı', 'Stok (TL)', 'Ort Cover', 'Ort Marj (%)']
        st.dataframe(kategori_stats, use_container_width=True)
    
    st.markdown("---")
    st.info("🚧 Detaylı dashboard özellikleri geliştiriliyor...")
