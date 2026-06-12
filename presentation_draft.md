# 🌿 DRAFT PRESENTASI: PLANTSENSE AI
**Sistem Klasifikasi Tingkat Stres Tanaman Berbasis Web & Machine Learning**
*Format: Markdown Presentation (Slide-by-Slide)*

---

## 📺 SLIDE 1: Judul Utama
### **🌿 PlantSense AI**
**Sistem Klasifikasi Tingkat Stres Tanaman Berbasis Web Menggunakan Machine Learning**

* **Sub-judul:** Studi Kasus Visualisasi Data & Pengembangan Model AI
* **Anggota Tim & Algoritma:**
  1. **Johanes Darren Yehuda** - *Decision Tree Classifier*
  2. **Afrisya Dwiky Mauliddinka** - *Support Vector Machine (SVM)*
  3. **Muhammad Hafizh Raharja** - *K-Nearest Neighbors (KNN)*
* **Tujuan Proyek:** Mengembangkan solusi klasifikasi kesehatan tanaman (**Healthy**, **Moderate Stress**, **High Stress**) berdasarkan data sensor dan klorofil secara realtime via web.

---

## 📊 SLIDE 2: Latar Belakang & Masalah (Dataset)
### **Mengapa Stres Tanaman Penting Dideteksi Secara Dini?**
* **Masalah:** Deteksi manual tingkat stres tanaman lambat dan kurang akurat. Dibutuhkan otomasi berbasis sensor (biosensor).
* **Dataset:** `smart_plant_biosensor.csv`
  * Berisi data pembacaan sensor dan kandungan klorofil tanaman.
  * Fitur utama: Kelembapan, suhu, intensitas cahaya, kadar klorofil, dan variabel pendukung lainnya.
  * Target Kelas: `Plant_Health_Status` (Healthy, Moderate Stress, High Stress).
  * **Pembersihan Data:** Menghapus kolom non-prediktif seperti `Timestamp` dan `Plant_ID`.

---

## 📈 SLIDE 3: Exploratory Data Analysis (EDA)
### **Memahami Hubungan Antar Data**
* **Analisis Korelasi (Feature Correlation Heatmap):**
  * Memetakan kekuatan korelasi antar fitur numerik menggunakan matriks korelasi Pearson.
  * Menentukan fitur yang paling berpengaruh terhadap perubahan status tanaman.
* **Distribusi Awal Kelas Target:**
  * Menampilkan sebaran data awal kelas target.
  * **Temuan Awal:** Distribusi kelas target tidak seimbang (*imbalanced*), yang berpotensi membuat model bias ke kelas mayoritas.

---

## ⚖️ SLIDE 4: Penanganan Data Imbalance (SMOTE)
### **Menseimbangkan Dataset untuk Performa Model yang Adil**
* **Kondisi Awal (Imbalance):**
  * *Healthy (0):* 239 sampel
  * *High Stress (1):* 400 sampel
  * *Moderate Stress (2):* 321 sampel
* **Solusi: SMOTE (Synthetic Minority Over-sampling Technique)**
  * Membuat sampel sintetis untuk kelas minoritas (*Healthy* & *Moderate Stress*) pada data training agar distribusinya sama rata (masing-masing 400 sampel).
* **Evaluasi Grafik:** Membandingkan grafik distribusi sebelum vs setelah SMOTE demi akurasi latih yang optimal tanpa kebocoran data (*data leakage* pada data uji).

---

## ⚙️ SLIDE 5: Pra-pemrosesan Data (Preprocessing)
### **Mempersiapkan Data Sebelum Pelatihan**
* **Label Encoding:** Mengubah status teks (`Healthy`, `Moderate Stress`, `High Stress`) menjadi angka numerik (0, 1, 2).
* **Feature Importance (SelectKBest f_classif):**
  * Menganalisis skor F-Score untuk menentukan fitur dengan tingkat kontribusi statistik tertinggi.
* **Standarisasi Fitur:**
  * Menggunakan `StandardScaler` untuk menyamakan skala seluruh fitur numerik agar tidak didominasi oleh fitur dengan angka besar.
* **Data Splitting:** Pembagian data 80% Training (diberi perlakuan SMOTE) dan 20% Testing (original untuk validasi objektif).

---

## 🤖 SLIDE 6: Pelatihan Model 1 - Support Vector Machine (SVM)
### **Pengembang: Afrisya Dwiky Mauliddinka**
* **Metodologi:**
  * Optimasi Hyperparameter menggunakan **GridSearchCV** dan **5-Fold Stratified Cross-Validation**.
  * Parameter yang diuji: `C` (regulasi), `kernel` (linear, rbf, poly), `gamma` (lebar kernel), dan `degree`.
* **Metrik & Evaluasi:**
  * Menghasilkan model terbaik untuk memisahkan data dengan batas keputusan berdimensi tinggi.
  * Output: Confusion Matrix SVM disimpan di `results/confusion_matrices/svm_confusion_matrix.png`.

---

## 🤖 SLIDE 7: Pelatihan Model 2 - K-Nearest Neighbors (KNN)
### **Pengembang: Muhammad Hafizh Raharja**
* **Metodologi:**
  * Menguji berbagai skenario nilai `n_neighbors` (K), tipe pembobotan (`weights`), dan metrik jarak (`metric`).
* **Visualisasi Tambahan:**
  * Menampilkan grafik kurva perbandingan **Nilai K vs Akurasi Data Uji** (`knn_k_vs_accuracy.png`) untuk menentukan nilai K paling optimal secara visual.
* **Metrik & Evaluasi:**
  * Menyimpan representasi model tetangga terdekat terbaik.
  * Output: Confusion Matrix KNN disimpan di `results/confusion_matrices/knn_confusion_matrix.png`.

---

## 🤖 SLIDE 8: Pelatihan Model 3 - Decision Tree
### **Pengembang: Johanes Darren Yehuda**
* **Metodologi:**
  * Tuning parameter pohon: `max_depth`, `min_samples_split`, `min_samples_leaf`, dan kriteria pecahan cabang (Gini / Entropy).
* **Visualisasi Struktur Pohon:**
  * Menghasilkan bagan struktur pohon keputusan (`dt_tree_visualization.png`) untuk memperlihatkan bagaimana logika percabangan klasifikasi terbentuk.
* **Feature Importance:**
  * Menghitung nilai kontribusi masing-masing fitur secara langsung berdasarkan model pohon keputusan.

---

## 🏁 SLIDE 9: Perbandingan Performa Model (Ringkasan Jupyter)
### **Model Manakah yang Terbaik?**
* **Metrik Utama yang Dibandingkan:**
  1. **Akurasi Cross-Validation** vs **Akurasi Uji**
  2. **F1-Score** per masing-masing kelas target
  3. **Waktu Pelatihan (Detik)**
* **Hasil Master Ringkasan:**
  * Ketiga model berhasil dilatih menggunakan data seimbang (SMOTE) dan disimpan dalam format file `.pkl`.
  * Hasil perbandingan komparatif disimpan ke `results/model_comparison.json`.

---

## 🌐 SLIDE 10: Transisi ke Web App (Arsitektur Vercel Serverless)
### **Membawa Model ML dari Jupyter Notebook ke Web Production**
* **Platform:** Vercel Hosting
* **Struktur Backend (Serverless):**
  * `api/index.py` ditulis menggunakan **Flask (Python)**.
  * Menggunakan pustaka `joblib` untuk memuat model terbaik secara dinamis (`svm_model.pkl`, `knn_model.pkl`, `dt_model.pkl`).
* **Fungsi API Utama:**
  1. `/api/predict` (POST): Menerima parameter sensor dari input user, melakukan standardisasi dengan `scaler.pkl`, lalu memprediksi status stres menggunakan model terpilih (atau membandingkan ketiganya).
  2. `/api/comparison` (GET): Mengirim data performa metrik evaluasi model untuk ditampilkan dalam grafik interaktif di frontend.

---

## 💻 SLIDE 11: Demo Antarmuka Web (Frontend Statis)
### **Fitur Utama Aplikasi Web PlantSense AI**
* **Dashboard Utama (`index.html`):** Informasi ringkas proyek dan visualisasi data awal.
* **Halaman Prediksi (`predict.html`):** 
  * Formulir interaktif untuk menginput data sensor realtime.
  * Menampilkan hasil prediksi klasifikasi status stres tanaman beserta persentase probabilitas keyakinan model.
* **Halaman Komparasi (`comparison.html`):**
  * Visualisasi grafik performa akurasi, presisi, recall, F1-score, dan waktu latih tiap model menggunakan data yang dikirim oleh backend API.
* **Halaman Tentang (`about.html`):** Informasi pengembang tim.

---

## 📌 SLIDE 12: Kesimpulan & Diskusi
### **Rangkuman Proyek**
1. Penanganan data menggunakan **SMOTE** berhasil meningkatkan sensitivitas model terhadap kelas minoritas.
2. Integrasi model Python dengan serverless backend Vercel memungkinkan klasifikasi real-time yang ringan dan responsif.
3. Dashboard komparasi membantu pengguna memilih model terbaik berdasarkan kebutuhan akurasi vs kecepatan komputasi.
