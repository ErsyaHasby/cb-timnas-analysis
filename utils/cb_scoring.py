import pandas as pd
import numpy as np
from scipy import stats

CB_WEIGHTS = {
    'clearances_pg':        0.20,
    'aerial_duels_won':     0.15,
    'total_duels_won':      0.15,
    'accurate_passes':      0.15,
    'long_balls_accurate':  0.10,
    'balls_recovered_pg':   0.05,
    'errors_leading_shot': -0.10,
    'dribbled_past_pg':    -0.05,
    'fouls_pg':            -0.05,
}

def calculate_cb_score(df):
    df = df.copy()

    # Pastikan numeric
    for col in CB_WEIGHTS.keys():
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    df['minutes'] = pd.to_numeric(df['minutes'], errors='coerce').fillna(0)
    df['avg_rating'] = pd.to_numeric(df['avg_rating'], errors='coerce').fillna(6.0)

    # Tampilkan semua pemain, tandai yang menit kurang
    df_qualified = df.copy()
    df_limited   = df[df['minutes'] < 450].copy()
    print(f"  ⚠ Pemain menit < 450: {len(df_limited)} (tetap diranking)")

    if len(df_qualified) < 2:
        print("⚠ Pemain qualified < 2, tambah lebih banyak data CB!")
        df_qualified['cb_score'] = 50.0
        df_qualified['tier'] = '🟢 Developing'
        df_qualified['status'] = df_qualified['called_up'].apply(
            lambda x: '✅ Dipanggil' if str(x).strip().lower() == 'yes' 
            else '❌ Tidak Dipanggil'
        )
        df_qualified['rank'] = range(1, len(df_qualified) + 1)
        return df_qualified, df_limited

    # Hitung Z-score berbobot
    weighted_z = pd.Series(0.0, index=df_qualified.index)

    for metric, weight in CB_WEIGHTS.items():
        if metric not in df_qualified.columns:
            continue
        col = df_qualified[metric]
        if col.std() == 0:
            continue
        z = stats.zscore(col)
        if weight < 0:
            weighted_z += (-z) * abs(weight)
        else:
            weighted_z += z * weight

    df_qualified['raw_score'] = weighted_z

    # Tambah bonus rating (10%)
    rating_norm = (
        (df_qualified['avg_rating'] - 6.0) / (8.5 - 6.0) * 100
    ).clip(0, 100)
    df_qualified['rating_bonus'] = rating_norm * 0.10

    df_qualified['composite_score'] = (
        df_qualified['raw_score'] + df_qualified['rating_bonus']
    )

    # Normalize 0-100
    min_s = df_qualified['composite_score'].min()
    max_s = df_qualified['composite_score'].max()
    if max_s > min_s:
        df_qualified['cb_score'] = (
            (df_qualified['composite_score'] - min_s) /
            (max_s - min_s) * 100
        ).round(1)
    else:
        df_qualified['cb_score'] = 50.0

    # Label tier
    df_qualified['tier'] = df_qualified['cb_score'].apply(lambda s:
        '🔴 Timnas Ready'     if s >= 75 else
        '🟡 Fringe Candidate' if s >= 50 else
        '🟢 Developing'
    )

    # Status dipanggil
    df_qualified['status'] = df_qualified['called_up'].apply(lambda x:
        '✅ Dipanggil' if str(x).strip().lower() == 'yes' 
        else '❌ Tidak Dipanggil'
    )

    # Sort & rank
    df_qualified = df_qualified.sort_values(
        'cb_score', ascending=False
    ).reset_index(drop=True)
    df_qualified['rank'] = range(1, len(df_qualified) + 1)

    return df_qualified, df_limited