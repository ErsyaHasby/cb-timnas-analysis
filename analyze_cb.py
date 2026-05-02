import pandas as pd
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.cb_scoring import calculate_cb_score

RAW_PATH = "data/raw/cb_liga1.csv"
OUT_PATH = "data/processed/cb_ranked.csv"
os.makedirs("data/processed", exist_ok=True)

if __name__ == "__main__":
    print("="*65)
    print("ANALISIS CB LOKAL BRI LIGA 1 — ASEAN CUP 2026")
    print("="*65)

    df = pd.read_csv(RAW_PATH)
    df.columns = df.columns.str.strip()
    df['name'] = df['name'].str.strip()
    df['club'] = df['club'].str.strip()

    print(f"✓ Total CB loaded : {len(df)} pemain")
    print(f"  Dipanggil Herdman : {(df['called_up'].str.lower()=='yes').sum()} pemain")
    print(f"  Tidak dipanggil   : {(df['called_up'].str.lower()=='no').sum()} pemain")

    df_ranked, df_limited = calculate_cb_score(df)
    df_ranked.to_csv(OUT_PATH, index=False)

    # ── DISPLAY KOLOM ─────────────────────────────────
    cols = ['rank','name','club','age','minutes','avg_rating',
            'clearances_pg','aerial_duels_won','total_duels_won',
            'accurate_passes','cb_score','tier','status']
    show = [c for c in cols if c in df_ranked.columns]

    pd.set_option('display.width', 140)
    pd.set_option('display.max_colwidth', 22)

    # ── FULL RANKING ──────────────────────────────────
    print("\n📊 FULL RANKING CB LOKAL BRI LIGA 1")
    print("-"*65)
    print(df_ranked[show].to_string(index=False))

    # ── YANG DIPANGGIL vs TIDAK ───────────────────────
    called  = df_ranked[df_ranked['status'] == '✅ Dipanggil']
    not_called = df_ranked[df_ranked['status'] == '❌ Tidak Dipanggil']

    print("\n\n✅ CB YANG DIPANGGIL HERDMAN — RANKING MEREKA")
    print("-"*65)
    print(called[show].to_string(index=False))

    print("\n\n❌ CB YANG TIDAK DIPANGGIL — LAYAK DIPANGGIL?")
    print("-"*65)
    print(not_called[show].head(5).to_string(index=False))

    # ── INSIGHT OTOMATIS ─────────────────────────────
    print("\n\n💡 INSIGHT ANALISIS:")
    print("-"*65)

    top_overall = df_ranked.iloc[0]
    top_not_called = not_called.iloc[0] if len(not_called) > 0 else None

    print(f"\n  🏆 CB terbaik Liga 1 berdasarkan data:")
    print(f"     {top_overall['name']} ({top_overall['club']}) — Score: {top_overall['cb_score']} | {top_overall['status']}")

    if top_not_called is not None:
        print(f"\n  🚨 CB terbaik yang TIDAK dipanggil:")
        print(f"     {top_not_called['name']} ({top_not_called['club']}) — Score: {top_not_called['cb_score']}")

        # Bandingkan dengan CB dipanggil terendah
        if len(called) > 0:
            weakest_called = called.iloc[-1]
            print(f"\n  ⚖️  Perbandingan:")
            print(f"     {top_not_called['name']} (tidak dipanggil) : {top_not_called['cb_score']}")
            print(f"     {weakest_called['name']} (dipanggil)        : {weakest_called['cb_score']}")
            if top_not_called['cb_score'] > weakest_called['cb_score']:
                print(f"\n  ⚠️  Ada CB tidak dipanggil yang statistiknya")
                print(f"     lebih baik dari CB yang dipanggil!")

    print(f"\n✓ Saved: {OUT_PATH}")