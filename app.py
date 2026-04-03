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
        color: white;
        padding: 15px;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
    }
    .prediction-danger {
        background-color: #c92a2a;
        color: white;
        padding: 15px;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
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
        
        # Tambahkan Student_ID jika belum ada di data asli
        if 'Student_ID' not in db.columns:
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
    st.image("image/logo-dicoding.jpg", width=120)

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
        <h3 style="color:white;">👋 Selamat Datang</h3>
        <p style="color:white;">
            Gunakan aplikasi ini untuk memprediksi secara dini apakah mahasiswa berisiko dropout 
            atau diprediksi akan lulus (graduate) berdasarkan rekam jejak akademik dan administrasi mereka.
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

            # Ambil data metrik untuk UI
            tuition_status = "Lancar" if data_mhs["Tuition_fees_up_to_date"].values[0] == 1 else "Menunggak"
            scholarship_status = "Ya" if data_mhs["Scholarship_holder"].values[0] == 1 else "Tidak"
            age = data_mhs["Age_at_enrollment"].values[0]
            sks_lulus = data_mhs["Curricular_units_2nd_sem_approved"].values[0]
            nilai_rata = data_mhs["Curricular_units_2nd_sem_grade"].values[0]
            status_asli = data_mhs["Status"].values[0]

            # Siapkan data prediksi
            X_pred = data_mhs.drop(columns=["Student_ID", "Status"])
            X_pred_scaled = scaler.transform(X_pred)

            # Prediksi menggunakan model baru
            prediksi = rf_model.predict(X_pred_scaled)[0]

            # =========================
            # CARD HASIL UI
            # =========================
            st.markdown(f"""
            <div class="card">
                <h3 style="color:white;">🎓 Student ID: {student_id}</h3>
            """, unsafe_allow_html=True)

            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("💳 Status SPP", tuition_status)
            col2.metric("🎁 Beasiswa", scholarship_status)
            col3.metric("👤 Usia", age)
            col4.metric("📚 SKS Lulus", sks_lulus)
            col5.metric("📈 Nilai Rata-rata", round(nilai_rata, 2))

            st.markdown("<br>", unsafe_allow_html=True)

            # Logika Cuma 2 Output (Graduate vs Dropout)
            if prediksi == "Graduate":
                st.markdown(
                    """
                    <div class="prediction-success">
                        ✅ PREDIKSI: Mahasiswa AMAN dan berpotensi LULUS (Graduate)
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.balloons() # Efek visual
            elif prediksi == "Dropout":
                st.markdown(
                    """
                    <div class="prediction-danger">
                        🚨 PERINGATAN: Mahasiswa memiliki pola berisiko tinggi DROPOUT!
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.warning("💡 Rekomendasi Action: Segera lakukan pendampingan akademik atau periksa status tunggakan SPP mahasiswa terkait.")

            st.caption(f"Status asli di database: {status_asli}")
            st.markdown("</div>", unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("""
<div class="footer">
    © 2026 Jaya Jaya Institut • Student Dropout Prediction Dashboard
</div>
""", unsafe_allow_html=True)
