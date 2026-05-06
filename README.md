# Analisis CB Lokal BRI Liga 1 - ASEAN Cup 2026

Proyek ini merupakan sistem analisis performa defender tengah (Center Back/CB) dari BRI Liga 1 Indonesia untuk menentukan kelayakan pemain dipanggil dalam skuad Timnas Indonesia untuk kompetisi ASEAN Cup 2026.

## Daftar Isi

- [Deskripsi Proyek](#deskripsi-proyek)
- [Metode Analisis](#metode-analisis)
- [Metode Scraping Data](#metode-scraping-data)
- [Struktur Proyek](#struktur-proyek)
- [Persyaratan Sistem](#persyaratan-sistem)
- [Tutorial Lengkap (Dari Awal)](#tutorial-lengkap-dari-awal)
- [Penggunaan](#penggunaan)
- [File Output](#file-output)
- [Dokumentasi Teknis](#dokumentasi-teknis)
- [Tips dan Troubleshooting](#tips-dan-troubleshooting)

## Deskripsi Proyek

Proyek ini menganalisis performa center back lokal dari BRI Liga 1 menggunakan metrik statistik defensif yang komprehensif. Sistem ini memberikan ranking dan klasifikasi tier untuk setiap pemain berdasarkan performa mereka di lapangan, membantu identifikasi pemain mana saja yang layak dipanggil untuk skuad Timnas.

### Tujuan Utama

1. Menganalisis performa statistik CB lokal secara objektif
2. Membandingkan pemain yang sudah dipanggil vs belum dipanggil
3. Mengidentifikasi CB dengan potensi tinggi yang mungkin terlewatkan
4. Memberikan rekomendasi berdasarkan data dan metrik terukur

## Metode Analisis

### Sistem Penilaian (CB Score)

Proyek ini menggunakan **Weighted Z-Score Normalization** untuk menghitung CB Score. Berikut adalah metrik dan bobot yang digunakan:

#### Komponen Penilaian

| Metrik | Bobot | Deskripsi |
|--------|-------|-----------|
| Clearances per Game | 20% | Kemampuan membersihkan bola dari area pertahanan |
| Aerial Duels Won | 15% | Penguasaan bola di udara |
| Total Duels Won | 15% | Kemenangan dalam pertarungan dengan lawan |
| Accurate Passes | 15% | Ketepatan passing (critical untuk modern CB) |
| Long Balls Accurate | 10% | Akurasi long ball untuk transisi |
| Balls Recovered per Game | 5% | Efektivitas merebut bola |
| Errors Leading to Shot | -10% | Penalty untuk kesalahan berbahaya |
| Dribbled Past per Game | -5% | Penalty untuk pemain yang dribble dengan mudah |
| Fouls per Game | -5% | Penalty untuk terlalu banyak pelanggaran |

#### Bonus Rating

Ditambahkan bonus 10% dari average rating pemain (normalized dari skala 6.0-8.5) untuk mempertimbangkan penilaian keseluruhan performa.

#### Tahapan Kalkulasi

1. **Normalisasi dengan Z-Score**: Setiap metrik dikonversi ke z-score untuk membandingkan dalam skala yang sama
2. **Weighted Sum**: Z-score dikalikan dengan bobot masing-masing metrik
3. **Tambah Rating Bonus**: Ditambahkan bonus dari average rating pemain
4. **Composite Score**: Hasil penjumlahan semua komponen
5. **Normalisasi 0-100**: Composite score dinormalisasi ke skala 0-100

#### Klasifikasi Tier

Berdasarkan CB Score, pemain diklasifikasikan menjadi tiga tier:

- **Timnas Ready** (Score >= 75): Pemain berkualitas tinggi siap untuk kompetisi internasional
- **Fringe Candidate** (Score 50-74): Pemain dengan potensi baik, perlu development lebih lanjut
- **Developing** (Score < 50): Pemain masih dalam tahap pengembangan

#### Kualifikasi Pemain

- Hanya pemain dengan **minimal 450 menit bermain** yang dipertimbangkan dalam ranking penuh
- Pemain dengan menit kurang dari 450 tetap ditampilkan tetapi ditandai sebagai "limited minutes"

## Metode Scraping Data

### Sumber Data

Data dikumpulkan dari platform statistik sepak bola (seperti Sofascore, Flashscore, atau API khusus) yang menyediakan data pemain BRI Liga 1.

### Format Data Input

Data disimpan dalam format CSV dengan struktur berikut:

```csv
name,club,age,nationality,position,called_up,minutes,avg_rating,clearances_pg,aerial_duels_won,total_duels_won,accurate_passes,long_balls_accurate,balls_recovered_pg,errors_leading_shot,dribbled_past_pg,fouls_pg
```

### Deskripsi Kolom Data

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| name | String | Nama pemain |
| club | String | Klub saat ini |
| age | Integer | Usia pemain |
| nationality | String | Kebangsaan pemain |
| position | String | Posisi pemain (CB/RB, dsb) |
| called_up | String | Status dipanggil (Yes/No) |
| minutes | Integer | Total menit bermain dalam season |
| avg_rating | Float | Rating rata-rata performa (skala 1-10) |
| clearances_pg | Float | Rata-rata clearances per game |
| aerial_duels_won | Float | Rata-rata aerial duels yang dimenangkan per game |
| total_duels_won | Float | Rata-rata total duels yang dimenangkan per game |
| accurate_passes | Float | Rata-rata akurat passes per game |
| long_balls_accurate | Float | Rata-rata accurate long balls per game |
| balls_recovered_pg | Float | Rata-rata balls recovered per game |
| errors_leading_shot | Float | Rata-rata errors yang berakhir dengan shot per game |
| dribbled_past_pg | Float | Rata-rata kali dribbled past per game |
| fouls_pg | Float | Rata-rata fouls per game |

### Cara Mendapatkan Data

1. **Menggunakan API Platform Statistik**: Hubungi provider statistik (Sofascore, Opta, dsb) untuk akses data
2. **Web Scraping Manual**: Jika menggunakan web scraping, gunakan tools seperti:
   - Python: `BeautifulSoup`, `Selenium`, `Scrapy`
   - Pastikan mematuhi robots.txt dan terms of service website
3. **Update Data Berkala**: Update data secara berkala (weekly/monthly) untuk refleksi performa terkini

## Struktur Proyek

```
cb-timnas-analysis/
├── README.md                    # File dokumentasi ini
├── app.py                       # Aplikasi dashboard Streamlit
├── analyze_cb.py               # Script analisis dan ranking
├── generate_infographic.py      # Script pembuat infographic
├── start.bat                    # Script untuk memulai project (Windows)
├── requirements.txt             # Dependencies Python (jika ada)
│
├── data/
│   ├── raw/
│   │   └── cb_liga1.csv        # Data mentah CB dari berbagai sumber
│   └── processed/
│       └── cb_ranked.csv       # Data hasil ranking dan scoring
│
└── utils/
    ├── __init__.py              # Python package marker
    └── cb_scoring.py            # Modul perhitungan CB Score
```

## Persyaratan Sistem

### Software Requirements

- Python 3.8 atau lebih tinggi
- pip (Python package manager)

### Python Dependencies

```
pandas>=1.3.0
numpy>=1.20.0
scipy>=1.7.0
streamlit>=1.0.0
matplotlib>=3.3.0
```

## Tutorial Lengkap (Dari Awal)

### Prasyarat

Sebelum memulai, pastikan Anda memiliki:
- Komputer dengan Windows/Mac/Linux
- Koneksi internet
- 500MB ruang disk kosong

### Fase 1: Instalasi Python

#### Step 1: Download dan Install Python

1. Kunjungi https://www.python.org/downloads/
2. Download versi Python 3.9 atau lebih tinggi
3. Jalankan installer dan CENTANG opsi "Add Python to PATH"
4. Klik "Install Now"
5. Tunggu hingga selesai

**Verifikasi instalasi:**
Buka terminal/command prompt dan ketik:
```bash
python --version
```

Akan menampilkan sesuatu seperti: `Python 3.11.0`

#### Step 2: Download Project

Opsi A - Jika punya Git:
```bash
git clone <repository-url>
cd cb-timnas-analysis
```

Opsi B - Manual:
1. Download project sebagai ZIP
2. Extract ke folder yang diinginkan
3. Buka folder tersebut

#### Step 3: Buka Terminal di Folder Project

**Windows:**
- Buka folder project
- Tekan `Shift + Right Click` di area kosong
- Pilih "Open PowerShell window here" atau "Open Command window here"

**Mac:**
- Buka Finder, masuk ke folder project
- Tekan `Cmd + Space`, ketik "Terminal"
- Drag folder ke jendela terminal

**Linux:**
- Buka file manager ke folder project
- Klik kanan, pilih "Open Terminal Here"

### Fase 2: Setup Environment

#### Step 1: Buat Virtual Environment

Virtual environment adalah folder terisolasi untuk project ini, agar tidak bertabrakan dengan Python lainnya.

Ketik perintah berikut di terminal:

```bash
python -m venv venv
```

Tunggu 1-2 menit hingga selesai.

#### Step 2: Aktifkan Virtual Environment

**Windows (Command Prompt):**
```bash
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```bash
& venv\Scripts\Activate.ps1
```

Jika ada error tentang execution policy, jalankan ini terlebih dahulu:
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

**Verifikasi:** Anda akan melihat `(venv)` di awal command line:
```
(venv) C:\Users\YourName\cb-timnas-analysis>
```

#### Step 3: Install Packages

Instalasi semua library yang diperlukan:

```bash
pip install pandas numpy scipy streamlit matplotlib
```

Proses ini akan mengunduh dan menginstall ~200MB package. Tunggu hingga selesai (biasanya 3-5 menit).

**Verifikasi instalasi:**
```bash
pip list
```

Akan menampilkan daftar packages yang sudah terinstall. Pastikan ada: pandas, numpy, scipy, streamlit, matplotlib.

### Fase 3: Memahami Struktur Data

#### Step 1: Lihat File Data

1. Buka file `data/raw/cb_liga1.csv` dengan text editor atau Excel
2. Anda akan melihat data dengan struktur:

```
name,club,age,nationality,position,called_up,minutes,avg_rating,...
Brian Fatari,Dewa United,26,Indonesia,CB,Yes,1950,6.78,...
Muhammad Ferarri,Bhayangkara FC,22,Indonesia,CB/RB,Yes,720,6.65,...
```

#### Step 2: Memahami Setiap Kolom

| Kolom | Contoh | Arti |
|-------|--------|------|
| name | Brian Fatari | Nama pemain |
| club | Dewa United | Klub pemain |
| age | 26 | Umur pemain |
| position | CB | Posisi (CB = Center Back) |
| called_up | Yes | Dipanggil ke Timnas? (Yes/No) |
| minutes | 1950 | Total menit bermain musim ini |
| avg_rating | 6.78 | Rating rata-rata (0-10) |
| clearances_pg | 1.8 | Rata-rata bola yang dibersihkan per game |
| aerial_duels_won | 1.4 | Rata-rata pertarungan udara yang dimenangkan |
| total_duels_won | 3.5 | Total pertarungan yang dimenangkan |
| accurate_passes | 42.9 | Akurasi passing |

#### Step 3: Update Data (Jika Diperlukan)

Jika Anda punya data pemain terbaru:

1. Buka `data/raw/cb_liga1.csv` dengan Excel/Google Sheets
2. Tambah pemain baru di baris terakhir
3. Isi semua kolom sesuai data pemain
4. Save file

**Format harus tetap sama** - jangan mengubah nama kolom atau urutan kolom.

### Fase 4: Menjalankan Analisis

#### Step 1: Jalankan Script Analisis Utama

Pastikan virtual environment masih aktif (lihat `(venv)` di terminal).

Jalankan perintah:
```bash
python analyze_cb.py
```

#### Step 2: Baca Output Terminal

Script akan menampilkan:

1. **Summary** (ringkasan):
```
═════════════════════════════════════════════════════════
ANALISIS CB LOKAL BRI LIGA 1 — ASEAN CUP 2026
═════════════════════════════════════════════════════════
✓ Total CB loaded : 24 pemain
  Dipanggil Herdman : 8 pemain
  Tidak dipanggil   : 16 pemain
```

2. **Full Ranking** - Daftar semua pemain berdasarkan ranking:
```
rank  name                   club              age  minutes  ...  cb_score  tier           status
1     Brian Fatari           Dewa United       26   1950     ...  92.5      Timnas Ready    ✅ Dipanggil
2     Asnawi Mangkualam      Persib Bandung    32   2700     ...  89.3      Timnas Ready    ✅ Dipanggil
3     Singo Abadi            Persik Kediri     25   1650     ...  76.8      Fringe Candidate ❌ Tidak
...
```

3. **CB yang Dipanggil** - Hanya pemain dengan status "Dipanggil":
```
✅ CB YANG DIPANGGIL HERDMAN — RANKING MEREKA
─────────────────────────────────────────────
(menampilkan ranking para pemain yang dipanggil Herdman)
```

4. **CB yang Tidak Dipanggil tapi Layak** - Candidate terbaik:
```
❌ CB YANG TIDAK DIPANGGIL — LAYAK DIPANGGIL?
─────────────────────────────────────────────
(menampilkan pemain tidak dipanggil yang punya score tinggi)
```

#### Step 3: Output File Tersimpan

Setelah script selesai, file baru dibuat di: `data/processed/cb_ranked.csv`

File ini berisi hasil ranking lengkap yang siap untuk analisis lebih lanjut.

### Fase 5: Melihat Hasil dengan Dashboard

#### Step 1: Jalankan Streamlit App

Di terminal (dengan venv masih aktif), jalankan:

```bash
streamlit run app.py
```

#### Step 2: Dashboard Akan Terbuka di Browser

Jika tidak otomatis, buka browser dan ketik: `http://localhost:8501`

Anda akan melihat dashboard interaktif dengan:
- Header dengan info ringkasan
- Tabel ranking dengan filter
- Visualisasi data
- Opsi untuk download data

#### Step 3: Gunakan Filter dan Sorting

Di dashboard Anda bisa:
- Filter berdasarkan tier (Timnas Ready, Fringe, Developing)
- Filter berdasarkan status (Dipanggil/Tidak)
- Sorting berdasarkan kolom apapun
- Melihat detail setiap pemain

#### Step 4: Stop Dashboard

Tekan `Ctrl + C` di terminal untuk menghentikan dashboard.

### Fase 6: Membuat Visualisasi Infographic (Optional)

#### Step 1: Generate Infographic

Pastikan Anda sudah jalankan `analyze_cb.py` terlebih dahulu.

Kemudian jalankan:
```bash
python generate_infographic.py
```

#### Step 2: File Gambar Dibuat

Script akan membuat file gambar yang menampilkan:
- Top CB ranking dalam format visual
- Warna-kode untuk status dipanggil/tidak
- Statistik defensif utama
- Format siap untuk presentasi atau sharing di media sosial

### Fase 7: Analisis Lebih Lanjut

#### Step 1: Export Data untuk Excel/Google Sheets

File `data/processed/cb_ranked.csv` bisa dibuka langsung di:
- Microsoft Excel
- Google Sheets
- OpenOffice Calc

Cukup buka file tersebut.

#### Step 2: Buat Pivot Table

Di Excel/Sheets, Anda bisa membuat pivot table untuk:
- Analisis per klub
- Statistik per tier
- Perbandingan dipanggil vs tidak dipanggil

#### Step 3: Analisis Lanjutan dengan Python

Jika ingin analisis lebih dalam, Anda bisa membuat script Python sendiri:

```python
import pandas as pd

# Load data hasil ranking
df = pd.read_csv('data/processed/cb_ranked.csv')

# Contoh: Rata-rata score per klub
print(df.groupby('club')['cb_score'].mean().sort_values(ascending=False))

# Contoh: Berapa pemain per tier?
print(df['tier'].value_counts())

# Contoh: Filter hanya pemain dengan score > 75
top_players = df[df['cb_score'] > 75]
print(top_players)
```

## Penggunaan

### Workflow Standar

1. **Update Data** (jika ada pemain baru atau stat update):
   - Edit atau replace file `data/raw/cb_liga1.csv`

2. **Jalankan Analisis**:
   ```bash
   python analyze_cb.py
   ```

3. **View Results**:
   - Lihat output di terminal untuk ringkasan
   - Check file `data/processed/cb_ranked.csv` untuk data lengkap
   - Atau jalankan dashboard: `streamlit run app.py`

4. **Generate Report** (Optional):
   ```bash
   python generate_infographic.py
   ```

### Interpretasi Hasil

#### Kolom Utama di Output

- **rank**: Ranking pemain berdasarkan CB Score (1 = terbaik)
- **name**: Nama pemain
- **club**: Klub pemain
- **cb_score**: Skor penilaian defensif (0-100)
- **tier**: Kategori pemain (Timnas Ready/Fringe Candidate/Developing)
- **status**: Status dipanggil Herdman (Dipanggil/Tidak Dipanggil)

#### Interpreting CB Score

- **85-100**: Pemain berkualitas elite, pasti harus dipanggil
- **75-84**: Pemain berkualitas tinggi, sangat layak dipanggil
- **60-74**: Pemain solid, perlu dipertimbangkan
- **50-59**: Pemain dengan potensi, masih berkembang
- **< 50**: Pemain muda atau sedang dalam transisi

## File Output

### data/processed/cb_ranked.csv

File ini berisi hasil ranking lengkap dengan kolom-kolom:

```
rank, name, club, age, minutes, avg_rating, clearances_pg, 
aerial_duels_won, total_duels_won, accurate_passes, cb_score, 
tier, status
```

Gunakan file ini untuk:
- Membuat laporan presentasi
- Analisis lebih lanjut dengan tools lain
- Membandingkan performa antar pemain
- Tracking progress sepanjang season

## Dokumentasi Teknis

### Mathematical Foundation

#### 1. Z-Score Calculation

Z-score adalah transformasi statistik yang mengukur berapa standard deviation suatu nilai dari mean.

Formula:
```
z = (x - μ) / σ

Dimana:
x = nilai individual
μ = mean dari semua nilai
σ = standard deviation
```

Contoh dengan data clearances_pg: [1.8, 1.4, 2.1, 0.9]
```
μ = (1.8 + 1.4 + 2.1 + 0.9) / 4 = 1.55
σ = sqrt(sum((x - μ)²) / n) ≈ 0.484

Untuk pemain dengan 1.8 clearances:
z = (1.8 - 1.55) / 0.484 ≈ 0.515
```

#### 2. Weighted Z-Score

Setiap z-score dikalikan dengan bobot untuk mengukur kepentingan relatif.

Formula:
```
weighted_z = Σ(z_i * w_i)

Dimana:
z_i = z-score untuk metrik i
w_i = weight untuk metrik i
```

#### 3. Handling Negative Weights

Untuk metrik negatif (errors, fouls, dribbled_past), kami menggunakan z-score negatif:

```
Jika weight < 0:
    weighted_z += (-z_i) * abs(weight)
Else:
    weighted_z += z_i * weight
```

#### 4. Rating Bonus

Rating bonus ditambahkan untuk mempertimbangkan penilaian keseluruhan:

Formula:
```
rating_norm = (avg_rating - 6.0) / (8.5 - 6.0) * 100
rating_bonus = rating_norm * 0.10
```

#### 5. Composite Score & Normalisasi

```
composite_score = weighted_z + rating_bonus

cb_score = ((composite - min) / (max - min)) * 100
```

Hasil selalu dalam range [0, 100].

### Implementasi Python

**File**: `utils/cb_scoring.py`

Code Flow:
1. Data preprocessing (convert to numeric)
2. Calculate z-scores per metrik
3. Apply weights (handling negative weights)
4. Add rating bonus
5. Calculate composite score
6. Normalize to 0-100
7. Classify into tiers
8. Assign status (called up)
9. Ranking and export

### Customization Opsi

#### 1. Mengubah Bobot Metrik

Edit `utils/cb_scoring.py`, ubah nilai di `CB_WEIGHTS`:

```python
CB_WEIGHTS = {
    'clearances_pg':        0.15,  # Turun dari 0.20
    'aerial_duels_won':     0.25,  # Naik dari 0.15
    'total_duels_won':      0.15,
    'accurate_passes':      0.10,  # Turun dari 0.15
    'long_balls_accurate':  0.10,
    'balls_recovered_pg':   0.05,
    'errors_leading_shot': -0.10,
    'dribbled_past_pg':    -0.05,
    'fouls_pg':            -0.05,
}
```

Total bobot positif sebaiknya ~1.0.

#### 2. Mengubah Rating Bonus

Cari baris di `utils/cb_scoring.py`:
```python
df['rating_bonus'] = rating_norm * 0.10  # Ubah angka ini
```

#### 3. Mengubah Tier Threshold

Cari section tier classification:
```python
df['tier'] = df['cb_score'].apply(lambda s:
    '🔴 Timnas Ready'     if s >= 75 else  # Ubah 75
    '🟡 Fringe Candidate' if s >= 50 else  # Ubah 50
    '🟢 Developing'
)
```

#### 4. Menambah Metrik Baru

1. Tambahkan kolom ke CSV file: `new_metric_pg`
2. Tambahkan ke `CB_WEIGHTS` di `utils/cb_scoring.py`
3. Sesuaikan bobot existing agar total tetap ~1.0

#### 5. Mengubah Rating Scale

Jika scale rating berbeda (default 6.0-8.5):

```python
# Untuk scale 0-10:
rating_norm = (df['avg_rating'] / 10.0 * 100).clip(0, 100)

# Untuk scale 1-5:
rating_norm = ((df['avg_rating'] - 1.0) / 4.0 * 100).clip(0, 100)
```

### Validasi Hasil

Setelah modifikasi, check:

- Semua file CSV valid dan bisa dibaca
- Tidak ada NaN atau error saat processing
- CB Score selalu dalam range 0-100
- Tier classification sesuai dengan score
- Ranking urut dari score tertinggi ke terendah
- Pemain dengan rating lebih tinggi cenderung score lebih tinggi

Cek file output:
```python
import pandas as pd
df = pd.read_csv('data/processed/cb_ranked.csv')

print(df['cb_score'].describe())  # Check score distribution
print(df['tier'].value_counts())  # Check tier distribution
print(df[['rank', 'name', 'cb_score', 'tier']].head(5))  # Top 5
```

## Penggunaan

### Workflow Standar

1. **Update Data** (jika ada pemain baru atau stat update):
   - Edit atau replace file `data/raw/cb_liga1.csv`

2. **Jalankan Analisis**:
   ```bash
   python analyze_cb.py
   ```

3. **View Results**:
   - Lihat output di terminal untuk ringkasan
   - Check file `data/processed/cb_ranked.csv` untuk data lengkap
   - Atau jalankan dashboard: `streamlit run app.py`

4. **Generate Report** (Optional):
   ```bash
   python generate_infographic.py
   ```

### Interpretasi Hasil

#### Kolom Utama di Output

- **rank**: Ranking pemain berdasarkan CB Score (1 = terbaik)
- **name**: Nama pemain
- **club**: Klub pemain
- **cb_score**: Skor penilaian defensif (0-100)
- **tier**: Kategori pemain (Timnas Ready/Fringe Candidate/Developing)
- **status**: Status dipanggil Herdman (Dipanggil/Tidak Dipanggil)

#### Interpreting CB Score

- **85-100**: Pemain berkualitas elite, pasti harus dipanggil
- **75-84**: Pemain berkualitas tinggi, sangat layak dipanggil
- **60-74**: Pemain solid, perlu dipertimbangkan
- **50-59**: Pemain dengan potensi, masih berkembang
- **< 50**: Pemain muda atau sedang dalam transisi

## File Output

### data/processed/cb_ranked.csv

File ini berisi hasil ranking lengkap dengan kolom-kolom:

```
rank, name, club, age, minutes, avg_rating, clearances_pg, 
aerial_duels_won, total_duels_won, accurate_passes, cb_score, 
tier, status
```

Gunakan file ini untuk:
- Membuat laporan presentasi
- Analisis lebih lanjut dengan tools lain
- Membandingkan performa antar pemain
- Tracking progress sepanjang season

## Tips dan Troubleshooting

### Tips Penggunaan Sehari-hari

#### Tip 1: Update Data Rutin

Setiap minggu/bulan, update file `data/raw/cb_liga1.csv` dengan stat terbaru pemain, lalu jalankan:
```bash
python analyze_cb.py
```

#### Tip 2: Shortcut Quick Start

Buat batch file `quick_run.bat` (Windows):
```batch
@echo off
cd /d %~dp0
call venv\Scripts\activate.bat
python analyze_cb.py
streamlit run app.py
pause
```

Setelah itu, cukup double-click file tersebut untuk menjalankan semuanya.

#### Tip 3: Backup Data Penting

Sebelum update besar-besaran, backup data:
```bash
copy data\raw\cb_liga1.csv data\raw\cb_liga1_backup_v1.csv
```

#### Tip 4: Monitor Perubahan

Setiap kali update, bandingkan hasil ranking dengan yang sebelumnya untuk melihat perubahan score pemain.

#### Tip 5: Export untuk Sharing

Di dashboard Streamlit, gunakan fitur share dan download data untuk:
- Share findings dengan tim
- Export chart untuk presentasi

### Troubleshooting Guide

#### Problem: "ModuleNotFoundError: No module named 'pandas'"

**Solusi:**
1. Pastikan virtual environment aktif (lihat `(venv)` di terminal)
2. Install ulang packages:
```bash
pip install pandas numpy scipy streamlit matplotlib
```

#### Problem: "Python command not found"

**Solusi:**
- Python belum diinstall atau tidak ada di PATH
- Reinstall Python dari python.org
- Centang opsi "Add Python to PATH" saat install

#### Problem: "File not found: data/raw/cb_liga1.csv"

**Solusi:**
- Buat folder `data/raw/` jika belum ada
- Pastikan file CSV sudah ada di lokasi tersebut
- Nama file harus tepat: `cb_liga1.csv` (bukan `cb-liga1.csv` atau lainnya)

#### Problem: Dashboard Streamlit tidak terbuka

**Solusi:**
```bash
# Cek apakah streamlit terinstall
pip install streamlit

# Jalankan dengan debug
streamlit run app.py --logger.level=debug
```

Jika masih error, coba port berbeda:
```bash
streamlit run app.py --server.port 8502
```

#### Problem: Virtual Environment Error saat Activate

**Windows PowerShell:**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
& venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**
```bash
venv\Scripts\activate.bat
```

#### Problem: Error "ModuleNotFoundError" di analyze_cb.py

**Solusi:**
1. Pastikan virtual environment aktif
2. Pastikan berada di folder project utama (bukan subfolder)
3. Run:
```bash
python analyze_cb.py
```

#### Problem: CSV File Error

Pastikan file CSV punya struktur benar:
- Header dengan nama kolom tepat
- Tidak ada baris kosong di tengah data
- Format UTF-8 (jika ada karakter Indonesia)

Buka dengan Excel, cek:
```
name,club,age,nationality,position,called_up,minutes,avg_rating,clearances_pg,...
```

### FAQ

**Q: Berapa sering saya harus update data?**
A: Minimal seminggu sekali, atau setelah ada pertandingan penting untuk capture performa terbaru.

**Q: Apakah saya bisa mengubah bobot metrik?**
A: Ya, edit file `utils/cb_scoring.py` dan ubah nilai di dictionary `CB_WEIGHTS`.

**Q: Bagaimana caranya tambah pemain baru?**
A: Edit file `data/raw/cb_liga1.csv`, tambah baris baru dengan data pemain, simpan, lalu jalankan `analyze_cb.py` lagi.

**Q: Bisa gak share dashboard dengan orang lain?**
A: Ya, gunakan `streamlit cloud` (gratis) atau deploy ke server.

**Q: Bagaimana kalau ada error di script?**
A: Check file script yang error, lihat line mana yang error dari terminal output, dan fix sesuai pesan error.

**Q: Apa bedanya Timnas Ready vs Fringe Candidate?**
A: Timnas Ready (score >= 75) sudah siap level internasional. Fringe Candidate (50-74) masih berkembang dan perlu consideration.

**Q: Bagaimana kalau pemain belum main cukup menit?**
A: Pemain dengan menit < 450 tetap ditampilkan tapi ditandai "limited minutes" dan perlu evaluasi lebih hati-hati.

## Kontribusi dan Pengembangan Lebih Lanjut

Ide untuk improvement proyek:

1. **Tambah Metrik**: Defensive actions, successful tackles, positioning quality
2. **Machine Learning**: Predictive model untuk liga mendatang
3. **Database**: Gunakan database (SQLite/PostgreSQL) untuk data management
4. **API**: Build REST API untuk integrasi dengan platform lain
5. **Real-time Updates**: Automate data scraping dan update database
6. **Advanced Visualization**: Radar charts, heatmaps, comparison tools

## Lisensi dan Catatan Hukum

- Proyek ini dibuat untuk analisis pendidikan dan sepak bola
- Pastikan mematuhi kebijakan privasi dan TOS dari sumber data yang digunakan
- Jangan gunakan data secara komersial tanpa izin pemilik data

---

**Last Updated**: May 2026
**Project Status**: Active
