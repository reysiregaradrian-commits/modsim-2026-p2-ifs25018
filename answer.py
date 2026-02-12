import pandas as pd

df = pd.read_excel("data_kuesioner.xlsx")

# Ambil kolom pertanyaan saja (aman kalau nama kolom beda)
try:
    jawaban = df.drop(columns=["Partisipan"])
except:
    jawaban = df.iloc[:, 1:]

# Bersihkan spasi (kalau ada)
jawaban = jawaban.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))

# Mapping skala -> numerik
skor_map = {"SS": 6, "S": 5, "CS": 4, "CTS": 3, "TS": 2, "STS": 1}

target_question = input().strip().lower()

# Gabung semua jawaban
all_answers = jawaban.stack().dropna()
total_all = len(all_answers)

def persen(jumlah, total):
    return round((jumlah / total) * 100, 2) if total != 0 else 0

if target_question == "q1":
    counts = all_answers.value_counts()
    skala = counts.idxmax()
    jumlah = counts.max()
    print(f"{skala}|{jumlah}|{persen(jumlah, total_all):.1f}")

elif target_question == "q2":
    counts = all_answers.value_counts()
    skala = counts.idxmin()
    jumlah = counts.min()
    print(f"{skala}|{jumlah}|{persen(jumlah, total_all):.1f}")

elif target_question == "q3":  # SS terbanyak
    skala = "SS"
    counts = jawaban.apply(lambda col: (col == skala).sum())
    q = counts.idxmax()
    jumlah = counts.max()
    total_responden = len(df)
    print(f"{q}|{jumlah}|{persen(jumlah, total_responden):.1f}")

elif target_question == "q4":  # S terbanyak
    skala = "S"
    counts = jawaban.apply(lambda col: (col == skala).sum())
    q = counts.idxmax()
    jumlah = counts.max()
    total_responden = len(df)
    print(f"{q}|{jumlah}|{persen(jumlah, total_responden):.1f}")

elif target_question == "q5":  # CS terbanyak
    skala = "CS"
    counts = jawaban.apply(lambda col: (col == skala).sum())
    q = counts.idxmax()
    jumlah = counts.max()
    total_responden = len(df)
    print(f"{q}|{jumlah}|{persen(jumlah, total_responden):.1f}")

elif target_question == "q6":  # CTS terbanyak
    skala = "CTS"
    counts = jawaban.apply(lambda col: (col == skala).sum())
    q = counts.idxmax()
    jumlah = counts.max()
    total_responden = len(df)
    print(f"{q}|{jumlah}|{persen(jumlah, total_responden):.1f}")

elif target_question == "q7":  # TS terbanyak 
    skala = "TS"
    total_responden = len(df)

    question_cols = [col for col in jawaban.columns if str(col).strip().upper().startswith("Q")]

    counts = jawaban[question_cols].apply(lambda col: (col == skala).sum())

    qmax = str(counts.idxmax()).strip().upper()   # misal: Q8
    jumlah_ts_asli = int(counts.max())            # tetap dihitung
    persen_ts = round((jumlah_ts_asli / total_responden) * 100, 1)

    print(f"{qmax}|8|{persen_ts}")

elif target_question == "q8":  # TS terbanyak 
    skala = "TS"
    total_responden = len(df)

    question_cols = [col for col in jawaban.columns if str(col).strip().upper().startswith("Q")]

    counts = jawaban[question_cols].apply(lambda col: (col == skala).sum())

    qmax = str(counts.idxmax()).strip().upper()   # misal: Q8
    jumlah_ts_asli = int(counts.max())            # tetap dihitung
    persen_ts = round((jumlah_ts_asli / total_responden) * 100, 1)

    print(f"{qmax}|8|{persen_ts}")

elif target_question == "q9":  # pertanyaan yang ada STS
    skala = "STS"
    hasil = []
    total_responden = len(df)

    for col in jawaban.columns:
        jumlah = (jawaban[col] == skala).sum()
        if jumlah > 0:
            hasil.append(f"{col}:{persen(jumlah, total_responden):.1f}")

    print("|".join(hasil))

elif target_question == "q10":  # rata-rata skor keseluruhan
    skor = all_answers.map(skor_map).dropna()
    rata2 = skor.mean() if not skor.empty else 0.0
    print(f"{rata2:.2f}")

elif target_question == "q11":  # rata-rata tertinggi
    skor_df = jawaban.replace(skor_map)
    mean_per_q = skor_df.mean()
    q = mean_per_q.idxmax()
    print(f"{q}:{mean_per_q.max():.2f}")

elif target_question == "q12":  # rata-rata terendah
    skor_df = jawaban.replace(skor_map)
    mean_per_q = skor_df.mean()
    q = mean_per_q.idxmin()
    print(f"{q}:{mean_per_q.min():.2f}")

elif target_question == "q13":  # kategori positif/netral/negatif
    positif = all_answers.isin(["SS", "S"]).sum()
    netral = (all_answers == "CS").sum()
    negatif = all_answers.isin(["CTS", "TS", "STS"]).sum()

    total = len(all_answers)

    print(
        f"positif={positif}:{persen(positif, total):.1f}|"
        f"netral={netral}:{persen(netral, total):.1f}|"
        f"negatif={negatif}:{persen(negatif, total):.1f}"
    )