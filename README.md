# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

## Business Understanding
Jaya Jaya Institut merupakan salah satu institusi pendidikan tinggi yang telah berdiri sejak tahun 2000. Selama lebih dari dua dekade, institusi ini telah mencetak banyak lulusan dengan reputasi yang sangat baik. Namun, di balik keberhasilan tersebut, institusi menghadapi tantangan besar berupa tingginya tingkat mahasiswa yang tidak menyelesaikan pendidikan alias dropout. Fenomena ini tidak hanya berdampak buruk pada reputasi institusi, tetapi juga mengindikasikan adanya kendala pada sistem pendukung akademik maupun non-akademik bagi mahasiswa.

### Permasalahan Bisnis
- Deteksi Keterlambatan: Institusi saat ini belum memiliki sistem peringatan dini (early warning system) yang terstruktur untuk mendeteksi mahasiswa yang berpotensi dropout.
- Intervensi yang Tidak Tepat Sasaran: Tanpa mengetahui faktor utama penyebab kegagalan mahasiswa, bimbingan khusus atau bantuan dari kampus seringkali terlambat diberikan.

### Cakupan Proyek
- Exploratory Data Analysis (EDA): Menganalisis Students' Performance Dataset untuk menemukan korelasi dan faktor utama penyebab dropout.
- Data Preparation: Melakukan pembersihan data, standardisasi (scaling), dan penanganan ketidakseimbangan kelas (imbalanced data) menggunakan teknik SMOTE.
- Machine Learning Development: Membangun model klasifikasi menggunakan algoritma Random Forest untuk memprediksi status kelulusan mahasiswa (Dropout, Enrolled, Graduate).
- Dashboard Creation: Membuat business dashboard interaktif untuk memonitor performa mahasiswa secara visual.
- Deployment: Mengembangkan prototype aplikasi berbasis web menggunakan Streamlit agar model prediksi dapat digunakan secara real-time oleh pihak institusi.

### Persiapan

Sumber data: [Klik di sini untuk mendownload dataset](https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/README.md)

Setup environment:
```
# Mengaktifkan virtual environment (contoh untuk Windows)
.venv\Scripts\activate

# Menginstal semua library yang dibutuhkan
pip install -r requirements.txt
```

## Business Dashboard
Dashboard bisnis telah dirancang menggunakan Tableau Public untuk membantu manajemen Jaya Jaya Institut memahami profil mahasiswa secara cepat. Dashboard ini menyoroti metrik-metrik krusial seperti:
- Rasio status kelulusan mahasiswa.
- Distribusi performa akademik di semester awal.
- Hubungan antara status finansial (tunggakan SPP & beasiswa) terhadap tingkat dropout.

Link Dashboard: [MASUKKAN LINK TABLEAU PUBLIC ANDA DI SINI NANTI]

## Menjalankan Sistem Machine Learning
Prototype sistem machine learning dibangun menggunakan antarmuka Streamlit. Aplikasi ini memungkinkan staf akademik untuk memasukkan data mahasiswa baru atau yang sedang berjalan, dan sistem akan secara instan memprediksi apakah mahasiswa tersebut berisiko dropout.

```
streamlit run app.py
```

## Conclusion
- Faktor Finansial dan Akademik Awal adalah Kunci: Tunggakan biaya SPP (Tuition_fees_up_to_date) dan kegagalan lulus mata kuliah di semester satu dan dua memiliki korelasi tertinggi terhadap status dropout. Sebaliknya, mahasiswa pemegang beasiswa memiliki survival rate yang jauh lebih tinggi.
- Karakteristik Demografi: Mahasiswa yang mendaftar pada usia yang lebih dewasa (non-reguler) memiliki kerentanan dropout yang lebih tinggi dibandingkan lulusan baru SMA.
- Keandalan Model: Model prediksi menggunakan Random Forest terbukti andal dengan tingkat akurasi mencapai 77%, dan mampu mendeteksi kelas rentan (Dropout) dengan precision yang tinggi. Sistem ini sudah siap diintegrasikan sebagai alat bantu deteksi dini institusi.

### Rekomendasi Action Items
Untuk menekan angka dropout, institusi direkomendasikan untuk melakukan langkah-langkah taktis berikut:
- Membangun Sistem Notifikasi Finansial (Financial Early Warning): Segera hubungi mahasiswa yang baru pertama kali menunggak SPP. Jangan tunggu hingga tunggakan menumpuk. Tawarkan opsi cicilan, penundaan pembayaran, atau konsultasi finansial sebelum mereka memutuskan berhenti kuliah.
- Program Mentoring Akademik di Tahun Pertama: Fokuskan perhatian pada mahasiswa yang gagal meluluskan 2 atau lebih mata kuliah di Semester 1. Berikan kelas tambahan, tutor sebaya, atau bimbingan akademik agar mereka tidak tertinggal terlalu jauh di Semester 2.
- Fleksibilitas untuk Mahasiswa Dewasa: Sediakan program kuliah dengan waktu yang lebih fleksibel (kelas malam/akhir pekan) atau bimbingan khusus manajemen waktu untuk mahasiswa yang mendaftar di usia dewasa, mengingat mereka rentan terbebani oleh tanggung jawab kerja atau keluarga.
- Perluasan Kuota Beasiswa Tepat Sasaran: Gunakan model Machine Learning ini untuk menyeleksi mahasiswa berprestasi dari latar belakang ekonomi kurang mampu (rentan menunggak SPP) sebagai prioritas penerima beasiswa, karena ini terbukti sangat efektif menekan angka dropout.