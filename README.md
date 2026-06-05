# 🌿 PlantSense AI

## Web-Based Plant Stress Level Classification System Using Machine Learning

A web application that classifies plant health status (**Healthy**, **Moderate Stress**, **High Stress**) using machine learning models trained on biosensor data and chlorophyll content.

---

## 🧑‍🤝‍🧑 Team

| Name | Algorithm |
|---|---|
| Johanes Darren Yehuda | SVM (Support Vector Machine) |
| Afrisya Dwiky Mauliddinka | KNN (K-Nearest Neighbors) |
| Muhammad Hafizh Raharja | Decision Tree |

---

## 📦 Dataset

- **Source**: [Smart Plant Biosensor Monitoring Dataset (Kaggle)](https://www.kaggle.com/datasets/muqaddasejaz/smart-plant-biosensor-monitoring-dataset)
- **Size**: 1,200 rows × 14 columns
- **Target**: `Plant_Health_Status` (3 classes)

---

## 🚀 Setup Instructions

### 1. Download the Dataset

1. Go to [Kaggle Dataset Link](https://www.kaggle.com/datasets/muqaddasejaz/smart-plant-biosensor-monitoring-dataset)
2. Download the CSV file
3. Place it in `dataset/smart_plant_biosensor.csv`

### 2. Install Python Dependencies

```bash
cd python
pip install -r requirements.txt
```

### 3. Train All Models

```bash
cd python/src
python train_all.py
```

This will:
- Run preprocessing & feature selection
- Train SVM, KNN, and Decision Tree with GridSearchCV
- Save models to `python/models/`
- Generate comparison charts in `python/results/`

### 4. Run PHP Web Application

Using XAMPP/Laragon/WAMP:
1. Copy or symlink the `php/` folder to your web server root (e.g., `htdocs/`)
2. Open `http://localhost/php/` in your browser

Or use PHP's built-in server:
```bash
cd php
php -S localhost:8000
```

---

## 📁 Project Structure

```
tubes_dasildat/
├── dataset/
│   └── smart_plant_biosensor.csv
├── python/
│   ├── src/
│   │   ├── preprocessing.py      # Data pipeline
│   │   ├── train_svm.py          # SVM training
│   │   ├── train_knn.py          # KNN training
│   │   ├── train_dt.py           # Decision Tree training
│   │   ├── train_all.py          # Train all models
│   │   └── predict.py            # PHP bridge script
│   ├── models/                    # Saved .pkl models
│   ├── results/                   # Charts & JSON results
│   └── requirements.txt
├── php/
│   ├── index.php                  # Landing page
│   ├── predict.php                # Prediction form
│   ├── result.php                 # Prediction results
│   ├── comparison.php             # Model comparison
│   ├── about.php                  # Team info
│   ├── assets/
│   │   ├── css/style.css
│   │   └── js/main.js
│   └── includes/
│       ├── config.php
│       ├── header.php
│       └── footer.php
└── README.md
```

---

## 🔧 Technologies

- **ML**: Python, Scikit-Learn, Pandas, NumPy, Matplotlib, Seaborn
- **Web**: PHP, HTML5, CSS3, JavaScript
- **Bridge**: PHP `exec()` → Python `predict.py` → JSON response
