import streamlit as st
import pandas as pd
import joblib

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Jaya Jaya Institut - Prediksi Dropout",
    page_icon="🎓",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
    .main {
        background-color: #f4f6f9;
    }

    .title-container {
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        padding: 25px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }

    .title-container h1 {
        margin: 0;
        font-size: 42px;
    }

    .title-container p {
        margin-top: 10px;
        font-size: 18px;
    }

    .card {
        background-color: #17517E;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 3px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }

    .prediction-success {
        background-color: #238212;
        color: #155724;
        padding: 15px;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
    }

    .prediction-danger {
        background-color: #f8d7da;
        color: #721c24;
        padding: 15px;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
    }

    .prediction-warning {
        background-color: #fff3cd;
        color: #856404;
        padding: 15px;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
    }

    .footer {
        text-align: center;
        color: gray;
        margin-top: 40px;
        font-size: 14px;
    }

    .stButton > button {
        width: 100%;
        background-color: #1e3c72;
        color: white;
        border-radius: 10px;
        height: 45px;
        font-size: 16px;
        border: none;
    }

    .stButton > button:hover {
        background-color: #2a5298;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD MODEL DAN DATA
# =========================
@st.cache_resource
def load_assets():
    try:
        model = joblib.load("model/rf_model.joblib")
        scaler = joblib.load("model/scaler.joblib")

        db = pd.read_csv("data/data.csv", sep=';')

        # Tambahkan Student_ID
        db.insert(0, "Student_ID", range(1, len(db) + 1))

        return model, scaler, db

    except FileNotFoundError as e:
        st.error(f"❌ File tidak ditemukan: {e}")
        st.stop()

rf_model, scaler, database = load_assets()

# =========================
# HEADER + LOGO
# =========================
col_logo, col_title = st.columns([1, 5])

with col_logo:
    # GANTI path di bawah dengan lokasi file logo kampus kamu
    # Contoh:
    # st.image("assets/logo.png", width=120)
    st.image(
        "image/logo-dicoding.jpg",
        width=120
    )

with col_title:
    st.markdown("""
    <div class="title-container">
        <h1>🎓 Jaya Jaya Institut</h1>
        <p>Sistem Prediksi Risiko Dropout Mahasiswa</p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# SIDEBAR INPUT
# =========================
st.sidebar.header("🔍 Input Data Mahasiswa")
st.sidebar.markdown(
    "Masukkan satu atau beberapa Student ID.\n\n"
    "Contoh: `1, 2, 15, 100`"
)

input_ids = st.sidebar.text_input(
    "Student ID",
    placeholder="1, 2, 3"
)

predict_btn = st.sidebar.button("🚀 Proses Prediksi")

# =========================
# KONTEN AWAL
# =========================
if not predict_btn:
    st.markdown("""
    <div class="card">
        <h3>👋 Selamat Datang</h3>
        <p>
            Gunakan aplikasi ini untuk memprediksi apakah mahasiswa berisiko dropout,
            graduate, atau masih enrolled berdasarkan data akademik dan administrasi.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# PROSES PREDIKSI
# =========================
if predict_btn:

    if not input_ids.strip():
        st.warning("⚠️ Silakan masukkan minimal satu Student ID.")
    else:
        list_id_str = [x.strip() for x in input_ids.split(",")]

        st.subheader("📊 Hasil Prediksi")

        for id_str in list_id_str:

            if not id_str.isdigit():
                st.error(f"❌ '{id_str}' bukan Student ID yang valid.")
                continue

            student_id = int(id_str)

            data_mhs = database[database["Student_ID"] == student_id]

            if data_mhs.empty:
                st.error(
                    f"❌ Student ID {student_id} tidak ditemukan. "
                    f"Maksimal ID: {len(database)}"
                )
                continue

            tuition_status = (
                "Lancar"
                if data_mhs["Tuition_fees_up_to_date"].values[0] == 1
                else "Menunggak"
            )

            scholarship_status = (
                "Ya"
                if data_mhs["Scholarship_holder"].values[0] == 1
                else "Tidak"
            )

            age = data_mhs["Age_at_enrollment"].values[0]
            sks_lulus = data_mhs["Curricular_units_2nd_sem_approved"].values[0]
            nilai_rata = data_mhs["Curricular_units_2nd_sem_grade"].values[0]
            status_asli = data_mhs["Status"].values[0]

            # Siapkan data prediksi
            X_pred = data_mhs.drop(columns=["Student_ID", "Status"])
            X_pred_scaled = scaler.transform(X_pred)

            prediksi = rf_model.predict(X_pred_scaled)[0]

            # =========================
            # CARD HASIL
            # =========================
            st.markdown(f"""
            <div class="card">
                <h3>🎓 Student ID: {student_id}</h3>
            """, unsafe_allow_html=True)

            col1, col2, col3, col4, col5 = st.columns(5)

            col1.metric("💳 Status SPP", tuition_status)
            col2.metric("🎁 Beasiswa", scholarship_status)
            col3.metric("👤 Usia", age)
            col4.metric("📚 SKS Lulus", sks_lulus)
            col5.metric("📈 Nilai Rata-rata", round(nilai_rata, 2))

            st.markdown("<br>", unsafe_allow_html=True)

            if prediksi == "Graduate":
                st.markdown(
                    """
                    <div class="prediction-success">
                        ✅ PREDIKSI: Mahasiswa diperkirakan akan GRADUATE
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            elif prediksi == "Dropout":
                st.markdown(
                    """
                    <div class="prediction-danger">
                        ⚠️ PREDIKSI: Mahasiswa berisiko DROPOUT
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:
                st.markdown(
                    """
                    <div class="prediction-warning">
                        🔄 PREDIKSI: Mahasiswa masih ENROLLED / Dalam Pantauan
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.caption(f"Status asli di database: {status_asli}")

            st.markdown("</div>", unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("""
<div class="footer">
    © 2026 Jaya Jaya Institut • Student Dropout Prediction Dashboard | Create by Zulfi Sam Shiddiq
</div>
""", unsafe_allow_html=True)
