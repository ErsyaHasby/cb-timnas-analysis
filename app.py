import streamlit as st
import pandas as pd
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.cb_scoring import calculate_cb_score

# ── CONFIG ────────────────────────────────────────────
st.set_page_config(
    page_title="Analisis CB Timnas Indonesia",
    page_icon="🇮🇩",
    layout="wide"
)

# ── LOAD & PROCESS DATA ───────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/raw/cb_liga1.csv")
    df.columns = df.columns.str.strip()
    df['name'] = df['name'].str.strip()
    df['club'] = df['club'].str.strip()
    df_ranked, _ = calculate_cb_score(df)
    return df_ranked

df = load_data()

# ── HEADER ────────────────────────────────────────────
st.markdown("""
<div style='background: linear-gradient(135deg, #ce1126, #ffffff, #ce1126);
            padding: 20px; border-radius: 12px; text-align: center;
            margin-bottom: 24px'>
    <h1 style='color: #ce1126; margin:0; font-size: 28px'>
        🇮🇩 Analisis CB Lokal BRI Liga 1
    </h1>
    <p style='color: #f1f5f9; margin: 6px 0 0; font-size: 14px'>
        ASEAN Cup 2026 — Siapa yang Layak Dipanggil John Herdman?
    </p>
</div>
""", unsafe_allow_html=True)

# ── SUMMARY METRICS ───────────────────────────────────
total       = len(df)
dipanggil   = len(df[df['status'] == '✅ Dipanggil'])
not_called  = len(df[df['status'] == '❌ Tidak Dipanggil'])
timnas_ready= len(df[df['tier'] == '🔴 Timnas Ready'])
top_missed  = df[df['status'] == '❌ Tidak Dipanggil'].iloc[0]['name']

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total CB Dianalisis", total)
col2.metric("Dipanggil Herdman", dipanggil)
col3.metric("Tidak Dipanggil", not_called)
col4.metric("Timnas Ready", timnas_ready)
col5.metric("CB Terbaik Terlewat", top_missed)

st.divider()

# ── TABS ──────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Full Ranking",
    "✅ CB Dipanggil",
    "🚨 CB Terlewat",
    "💡 Insight"
])

# Kolom display
DISPLAY_COLS = {
    'rank':               'Rank',
    'name':               'Nama',
    'club':               'Klub',
    'age':                'Usia',
    'minutes':            'Menit',
    'avg_rating':         'Rating',
    'clearances_pg':      'Clearances/G',
    'aerial_duels_won':   'Aerial Won',
    'total_duels_won':    'Duels Won',
    'accurate_passes':    'Acc. Passes',
    'cb_score':           'CB Score',
    'tier':               'Tier',
    'status':             'Status',
}

def show_table(data, title=None):
    """Render tabel dengan styling warna per tier & status"""
    if title:
        st.markdown(f"### {title}")

    show = [c for c in DISPLAY_COLS.keys() if c in data.columns]
    display = data[show].rename(columns=DISPLAY_COLS).reset_index(drop=True)

    def color_row(row):
        if '✅' in str(row.get('Status', '')):
            return ['background-color: #14532d; color: #ffffff; font-weight: 600'] * len(row)
        if row.get('Tier') == '🔴 Timnas Ready':
            return ['background-color: #9a3412; color: #ffffff; font-weight: 600'] * len(row)
        return ['background-color: #f8fafc; color: #0f172a'] * len(row)

    styled = display.style.apply(color_row, axis=1).format({
        'Rating':       '{:.2f}',
        'CB Score':     '{:.1f}',
        'Clearances/G': '{:.1f}',
        'Aerial Won':   '{:.1f}',
        'Duels Won':    '{:.1f}',
        'Acc. Passes':  '{:.1f}',
        'Menit':        '{:.0f}',
    })

    st.dataframe(
        styled,
        use_container_width=True,
        hide_index=True,
        height=min(50 + len(display) * 38, 600),
        column_config={
            'CB Score': st.column_config.ProgressColumn(
                'CB Score',
                min_value=0,
                max_value=100,
                format='%.1f'
            ),
            'Rating': st.column_config.NumberColumn(
                'Rating', format='%.2f'
            ),
        }
    )

# ── TAB 1: FULL RANKING ───────────────────────────────
with tab1:
    st.markdown("#### Filter")
    fc1, fc2, fc3 = st.columns(3)

    with fc1:
        tier_filter = st.multiselect(
            "Tier",
            options=df['tier'].unique().tolist(),
            default=df['tier'].unique().tolist()
        )
    with fc2:
        clubs = sorted(df['club'].unique().tolist())
        club_filter = st.multiselect(
            "Klub",
            options=clubs,
            default=clubs
        )
    with fc3:
        status_filter = st.multiselect(
            "Status Panggilan",
            options=['✅ Dipanggil', '❌ Tidak Dipanggil'],
            default=['✅ Dipanggil', '❌ Tidak Dipanggil']
        )

    filtered = df[
        df['tier'].isin(tier_filter) &
        df['club'].isin(club_filter) &
        df['status'].isin(status_filter)
    ]

    st.caption(f"Menampilkan {len(filtered)} dari {len(df)} CB")
    show_table(filtered, f"📊 Ranking CB Lokal BRI Liga 1 ({len(filtered)} pemain)")

# ── TAB 2: CB DIPANGGIL ───────────────────────────────
with tab2:
    called = df[df['status'] == '✅ Dipanggil'].copy()
    show_table(called, "✅ CB yang Dipanggil John Herdman")

    st.divider()
    st.markdown("#### Posisi Mereka di Antara Semua CB Liga 1")

    for _, row in called.iterrows():
        rank = int(row['rank'])
        score = row['cb_score']
        name = row['name']
        tier = row['tier']
        pct = score / 100

        st.markdown(f"**{name}** — Rank #{rank} dari {total} CB")
        col_a, col_b = st.columns([3, 1])
        with col_a:
            st.progress(pct, text=f"CB Score: {score:.1f}")
        with col_b:
            st.caption(tier)

# ── TAB 3: CB TERLEWAT ────────────────────────────────
with tab3:
    not_called_df = df[df['status'] == '❌ Tidak Dipanggil'].copy()
    top5 = not_called_df.head(5)

    st.markdown("### 🚨 Top 5 CB Tidak Dipanggil yang Statistiknya Lebih Baik")

    for i, (_, row) in enumerate(top5.iterrows()):
        rank  = int(row['rank'])
        score = row['cb_score']
        name  = row['name']
        club  = row['club']
        age   = int(row['age'])
        mins  = int(row['minutes'])
        tier  = row['tier']

        # Bandingkan dengan CB dipanggil terlemah
        weakest_called = df[df['status'] == '✅ Dipanggil'].iloc[-1]
        diff = score - weakest_called['cb_score']

        with st.container():
            st.markdown(f"""
            <div style='background:#0f172a; border-left: 4px solid #f59e0b;
                        border-radius:8px; padding:14px; margin-bottom:12px; color:#f8fafc'>
                <div style='font-size:16px; font-weight:bold; color:#f8fafc'>
                    #{rank} {name}
                    <span style='font-size:12px; color:#cbd5e1; font-weight:normal'>
                        — {club} | Usia {age} | {mins} menit
                    </span>
                </div>
                <div style='margin-top:8px; font-size:13px; color:#e2e8f0'>
                    CB Score: <b>{score:.1f}</b> &nbsp;|&nbsp; {tier}
                    &nbsp;|&nbsp;
                    <span style='color:#fca5a5'>
                        +{diff:.1f} lebih tinggi dari CB dipanggil terlemah
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### Semua CB Tidak Dipanggil")
    show_table(not_called_df)

# ── TAB 4: INSIGHT ────────────────────────────────────
with tab4:
    st.markdown("### 💡 Insight Analisis")

    best_overall  = df.iloc[0]
    best_called   = df[df['status'] == '✅ Dipanggil'].iloc[0]
    worst_called  = df[df['status'] == '✅ Dipanggil'].iloc[-1]
    best_missed   = df[df['status'] == '❌ Tidak Dipanggil'].iloc[0]

    # Insight cards
    insights = [
        {
            "icon": "🏆",
            "title": f"CB Terbaik Liga 1: {best_overall['name']}",
            "body": f"{best_overall['club']} | Score {best_overall['cb_score']:.1f} | {best_overall['status']}",
            "color": "#14532d"
        },
        {
            "icon": "✅",
            "title": f"CB Terbaik yang Dipanggil: {best_called['name']}",
            "body": f"{best_called['club']} | Score {best_called['cb_score']:.1f} | Rank #{int(best_called['rank'])} dari {total}",
            "color": "#1d4ed8"
        },
        {
            "icon": "🚨",
            "title": f"CB Terbaik yang Terlewat: {best_missed['name']}",
            "body": f"{best_missed['club']} | Score {best_missed['cb_score']:.1f} | Lebih tinggi {best_missed['cb_score'] - worst_called['cb_score']:.1f} poin dari {worst_called['name']}",
            "color": "#b45309"
        },
        {
            "icon": "⚠️",
            "title": f"CB Dipanggil Paling Lemah: {worst_called['name']}",
            "body": f"{worst_called['club']} | Score {worst_called['cb_score']:.1f} | Rank #{int(worst_called['rank'])} dari {total} — ada {len(df[df['cb_score'] > worst_called['cb_score'] ]) - dipanggil} CB tidak dipanggil yang lebih baik",
            "color": "#9f1239"
        },
    ]

    for ins in insights:
        st.markdown(f"""
        <div style='background:{ins["color"]}; border-radius:10px;
                    padding:16px; margin-bottom:12px; color:#f8fafc'>
            <div style='font-size:16px; font-weight:bold; color:#ffffff'>
                {ins["icon"]} {ins["title"]}
            </div>
            <div style='font-size:13px; color:#e2e8f0; margin-top:6px'>
                {ins["body"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Ringkasan teks narasi
    st.divider()
    st.markdown("### 📝 Narasi untuk Konten")
    n_better = len(df[
        (df['status'] == '❌ Tidak Dipanggil') &
        (df['cb_score'] > best_called['cb_score'])
    ])

    st.info(f"""
**Berdasarkan analisis data BRI Liga 1 musim ini:**

Dari 4 CB yang dipanggil John Herdman untuk ASEAN Cup 2026, 
hanya **{best_called['name']}** yang masuk kategori *Timnas Ready* 
dengan CB Score **{best_called['cb_score']:.1f}**.

Terdapat **{n_better} CB lokal** yang tidak dipanggil namun memiliki 
statistik lebih baik dari CB terbaik yang dipanggil. 
Yang paling mencolok adalah **{best_missed['name']}** ({best_missed['club']}) 
dengan score {best_missed['cb_score']:.1f}, dan **Rizky Ridho** (Persija) 
yang selama ini jadi langganan timnas namun absen dari skuad ASEAN Cup 2026.

*Catatan: Analisis ini berdasarkan data statistik murni dan tidak 
mempertimbangkan faktor taktis, kondisi fisik, dan keputusan pelatih.*
    """)

# ── FOOTER ────────────────────────────────────────────
st.divider()
st.caption("📊 Data: Sofascore BRI Liga 1 2025/26 | Metode: Z-Score Weighted | by Football Analytics")