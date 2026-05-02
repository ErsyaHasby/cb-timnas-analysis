import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import pandas as pd
import numpy as np

# ── LOAD DATA ─────────────────────────────────────────
df = pd.read_csv("data/processed/cb_ranked.csv")
# Build display frame: Top 10 overall, then any called players outside top 10
top10 = df[df['rank'] <= 10].sort_values('rank')
called_outside = df[(df['status'].str.contains('✅', na=False)) & (df['rank'] > 10)].sort_values('rank')
df_show = pd.concat([top10, called_outside], ignore_index=True)
TOTAL_ROWS = len(df_show)

# ── WARNA & STYLE ─────────────────────────────────────
COLOR_HEADER_RED   = "#8B0000"
COLOR_BG           = "#F5F0E8"
COLOR_TABLE_HEADER = "#2C2C2C"
COLOR_ROW_EVEN     = "#FFFFFF"
COLOR_ROW_ODD      = "#F9F6F0"
COLOR_TEXT_MAIN    = "#1A1A1A"
COLOR_TEXT_MUTED   = "#555555"
COLOR_CALLED       = "#1a3a6b"
COLOR_NOT_CALLED   = "#8B0000"
COLOR_DIVIDER      = "#CCCCC0"

FIG_W = 10
FIG_H = 14
DPI   = 150

fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=COLOR_BG)
ax  = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, FIG_W)
ax.set_ylim(0, FIG_H)
ax.axis('off')
ax.set_facecolor(COLOR_BG)

# ═══════════════════════════════════════════════════════
# SECTION 1 — HEADER
# ═══════════════════════════════════════════════════════
HEADER_Y      = 12.8
HEADER_HEIGHT = 1.0

header_box = FancyBboxPatch(
    (0.2, HEADER_Y), 4.2, HEADER_HEIGHT,
    boxstyle="round,pad=0.05",
    facecolor=COLOR_HEADER_RED,
    edgecolor='none',
    zorder=5
)
ax.add_patch(header_box)

ax.text(
    0.55, HEADER_Y + HEADER_HEIGHT / 2,
    "Ranking CB Lokal — BRI Liga 1 2025/26",
    color='white',
    fontsize=18,
    fontweight='bold',
    va='center',
    ha='left',
    zorder=6
)

ax.text(
    FIG_W - 0.25, HEADER_Y + HEADER_HEIGHT / 2,
    "BRI Liga 1  25/26",
    color=COLOR_TEXT_MUTED,
    fontsize=9,
    va='center',
    ha='right',
    style='italic'
)

ax.text(
    FIG_W / 2, HEADER_Y - 0.28,
    "Method: Z-Score Weighted  |  Top 10 CB Lokal  |  ASEAN Cup 2026 Selection",
    color=COLOR_TEXT_MUTED,
    fontsize=7.5,
    va='center',
    ha='center',
    style='italic'
)

# ═══════════════════════════════════════════════════════
# SECTION 2 — KOLOM HEADER TABEL
# ═══════════════════════════════════════════════════════
TABLE_TOP   = HEADER_Y - 0.55
ROW_H       = 0.82
TABLE_LEFT  = 0.20
TABLE_RIGHT = FIG_W - 0.20
TABLE_W     = TABLE_RIGHT - TABLE_LEFT

COLS = [
    ("Rank",      0.55,  'center'),
    ("Player",    1.80,  'left'),
    ("Club",      4.00,  'left'),
    ("Age",       5.30,  'center'),
    ("Tier",      6.00,  'center'),
    ("CB Score",  7.20,  'center'),
    ("Min",       8.10,  'center'),
    ("Rating",    8.70,  'center'),
    ("Status",    9.30,  'center'),
]

col_header_bg = FancyBboxPatch(
    (TABLE_LEFT, TABLE_TOP - 0.38), TABLE_W, 0.38,
    boxstyle="square,pad=0",
    facecolor='white',
    edgecolor=COLOR_DIVIDER,
    linewidth=0.5,
    zorder=3
)
ax.add_patch(col_header_bg)

for label, x, align in COLS:
    ax.text(
        x, TABLE_TOP - 0.19,
        label,
        color=COLOR_TABLE_HEADER,
        fontsize=8,
        fontweight='bold',
        va='center',
        ha=align,
        zorder=4
    )

ax.plot(
    [TABLE_LEFT, TABLE_RIGHT],
    [TABLE_TOP - 0.38, TABLE_TOP - 0.38],
    color=COLOR_DIVIDER, linewidth=1.0, zorder=4
)

# ═══════════════════════════════════════════════════════
# SECTION 3 — BARIS DATA
# ═══════════════════════════════════════════════════════
ROW_START_Y = TABLE_TOP - 0.38

for i, (_, row) in enumerate(df_show.iterrows()):
    y_top = ROW_START_Y - i * ROW_H
    y_ctr = y_top - ROW_H / 2

    row_color = COLOR_ROW_EVEN if i % 2 == 0 else COLOR_ROW_ODD

    row_bg = FancyBboxPatch(
        (TABLE_LEFT, y_top - ROW_H), TABLE_W, ROW_H,
        boxstyle="square,pad=0",
        facecolor=row_color,
        edgecolor=COLOR_DIVIDER,
        linewidth=0.3,
        zorder=2
    )
    ax.add_patch(row_bg)

    # Status strip kiri
    strip_color = COLOR_CALLED if '✅' in str(row.get('status', '')) else COLOR_NOT_CALLED
    strip = FancyBboxPatch(
        (TABLE_LEFT, y_top - ROW_H), 0.08, ROW_H,
        boxstyle="square,pad=0",
        facecolor=strip_color,
        edgecolor='none',
        zorder=3
    )
    ax.add_patch(strip)

    # Rank
    rank_val   = int(row['rank'])
    rank_color = COLOR_HEADER_RED if rank_val <= 3 else COLOR_TEXT_MAIN
    rank_size  = 13 if rank_val <= 3 else 11
    ax.text(
        0.55, y_ctr,
        str(rank_val),
        color=rank_color,
        fontsize=rank_size,
        fontweight='bold' if rank_val <= 3 else 'normal',
        va='center', ha='center', zorder=4
    )

    # Nama pemain
    name = str(row['name'])
    display_name = name if len(name) <= 24 else name[:23] + '…'
    ax.text(
        1.80, y_ctr + 0.10,
        display_name,
        color=COLOR_TEXT_MAIN,
        fontsize=9.5,
        fontweight='semibold',
        va='center', ha='left', zorder=4
    )

    # Sub-text status
    is_called    = '✅' in str(row.get('status', ''))
    status_label = "✓ Dipanggil" if is_called else "Tidak Dipanggil"
    status_color = COLOR_CALLED if is_called else "#AA2222"
    ax.text(
        1.65, y_ctr - 0.18,
        status_label,
        color=status_color,
        fontsize=6.5,
        va='center', ha='left', zorder=4
    )

    # Klub
    club = str(row['club'])
    display_club = club if len(club) <= 18 else club[:17] + '…'
    ax.text(
        4.00, y_ctr,
        display_club,
        color=COLOR_TEXT_MUTED,
        fontsize=8.5,
        va='center', ha='left', zorder=4
    )

    # Usia
    ax.text(
        5.30, y_ctr,
        str(int(row['age'])),
        color=COLOR_TEXT_MAIN,
        fontsize=9,
        va='center', ha='center', zorder=4
    )

    # Tier
    tier = str(row.get('tier', ''))
    ax.text(
        6.00, y_ctr,
        tier,
        color=COLOR_TEXT_MUTED,
        fontsize=8,
        va='center', ha='center', zorder=4
    )

    # CB Score kotak berwarna
    score = float(row['cb_score'])
    if score >= 75:
        score_bg, score_text = "#1a3a6b", "white"
    elif score >= 50:
        score_bg, score_text = "#4a7ab5", "white"
    else:
        score_bg, score_text = "#cccccc", "#333333"

    score_box = FancyBboxPatch(
        (6.90, y_ctr - 0.22), 0.8, 0.44,
        boxstyle="round,pad=0.04",
        facecolor=score_bg,
        edgecolor='none',
        zorder=4
    )
    ax.add_patch(score_box)
    ax.text(
        7.30, y_ctr,
        f"{score:.1f}",
        color=score_text,
        fontsize=9,
        fontweight='bold',
        va='center', ha='center', zorder=5
    )

    # Menit Bermain
    minutes = int(row.get('minutes', row.get('minutes', 0)) if not pd.isna(row.get('minutes', 0)) else row.get('minutes', 0))
    minutes = int(row.get('minutes', row.get('minutes', 0)))
    ax.text(
        8.10, y_ctr,
        f"{minutes}",
        color=COLOR_TEXT_MAIN,
        fontsize=9,
        va='center', ha='center', zorder=4
    )

    # Rating
    rating = float(row.get('avg_rating', row.get('rating', row.get('avg_rating', 0))))
    ax.text(
        8.70, y_ctr,
        f"{rating:.2f}",
        color=COLOR_TEXT_MAIN,
        fontsize=9,
        va='center', ha='center', zorder=4
    )

    # Status text column
    is_called = '✅' in str(row.get('status', ''))
    status_text = 'Dipanggil' if is_called else 'Tidak Dipanggil'
    status_color = COLOR_CALLED if is_called else '#AA2222'
    ax.text(
        9.30, y_ctr,
        status_text,
        color=status_color,
        fontsize=8,
        va='center', ha='center', zorder=4
    )

# Garis bawah tabel
final_y = ROW_START_Y - TOTAL_ROWS * ROW_H
ax.plot(
    [TABLE_LEFT, TABLE_RIGHT],
    [final_y, final_y],
    color=COLOR_DIVIDER, linewidth=1.0, zorder=4
)

# ═══════════════════════════════════════════════════════
# SECTION 4 — LEGENDA
# ═══════════════════════════════════════════════════════
LEG_Y = final_y - 0.35

leg1 = FancyBboxPatch(
    (TABLE_LEFT, LEG_Y - 0.10), 0.10, 0.20,
    boxstyle="square,pad=0",
    facecolor=COLOR_CALLED, edgecolor='none', zorder=4
)
ax.add_patch(leg1)
ax.text(TABLE_LEFT + 0.18, LEG_Y, "Dipanggil Herdman",
        color=COLOR_TEXT_MUTED, fontsize=7, va='center', ha='left')

leg2 = FancyBboxPatch(
    (TABLE_LEFT + 2.2, LEG_Y - 0.10), 0.10, 0.20,
    boxstyle="square,pad=0",
    facecolor=COLOR_NOT_CALLED, edgecolor='none', zorder=4
)
ax.add_patch(leg2)
ax.text(TABLE_LEFT + 2.38, LEG_Y, "Tidak Dipanggil",
        color=COLOR_TEXT_MUTED, fontsize=7, va='center', ha='left')

# ═══════════════════════════════════════════════════════
# SECTION 5 — INSIGHT BOX
# ═══════════════════════════════════════════════════════
INSIGHT_Y = final_y - 0.80

insight_box = FancyBboxPatch(
    (TABLE_LEFT, INSIGHT_Y - 0.55), TABLE_W, 0.55,
    boxstyle="round,pad=0.08",
    facecolor="#FFF8E1",
    edgecolor="#F59E0B",
    linewidth=1.0,
    zorder=3
)
ax.add_patch(insight_box)

called_in_top_count = top10['status'].str.contains('✅', na=False).sum()
total_called = df['status'].str.contains('✅', na=False).sum()
not_called_top = df_show[~df_show['status'].str.contains('✅', na=False)]
best_missed    = not_called_top.iloc[0] if len(not_called_top) > 0 else None

insight_text = (
    f"⚠  Hanya {called_in_top_count} dari {total_called} CB dipanggil masuk Top 10. "
    + (f"CB terbaik tidak dipanggil: {best_missed['name']} (Score {best_missed['cb_score']:.1f})"
       if best_missed is not None else "")
)

ax.text(
    TABLE_LEFT + 0.15, INSIGHT_Y - 0.27,
    insight_text,
    color="#7B4F00",
    fontsize=7.5,
    va='center', ha='left',
    zorder=4
)

# ═══════════════════════════════════════════════════════
# SECTION 6 — FOOTER WATERMARK
# ═══════════════════════════════════════════════════════
ax.text(
    TABLE_LEFT, 0.35,
    f"Generated: {pd.Timestamp.now().strftime('%d/%m/%Y')}  |  "
    f"Data: Sofascore BRI Liga 1 2025/26  |  "
    f"Method: Z-Score Weighted",
    color=COLOR_TEXT_MUTED,
    fontsize=6.5,
    va='center', ha='left',
)

ax.text(
    FIG_W - 0.25, 0.35,
    "Football Analytics ID",
    color=COLOR_TEXT_MUTED,
    fontsize=7,
    va='center', ha='right',
    style='italic'
)

# ── SIMPAN ────────────────────────────────────────────
import os
os.makedirs("data/processed", exist_ok=True)
out_path = "data/processed/cb_grade_infographic.png"
plt.savefig(out_path, dpi=DPI, bbox_inches='tight',
            facecolor=COLOR_BG, edgecolor='none')
plt.close()
print(f"✓ Saved: {out_path}")