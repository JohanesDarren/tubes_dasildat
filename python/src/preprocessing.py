"""
preprocessing.py - Shared Data Preprocessing & Feature Selection Module
========================================================================
Handles:
- Data loading and cleaning
- Feature selection (correlation analysis + SelectKBest)
- Feature scaling (StandardScaler)
- Train/test split (80/20 stratified)
- Export scaler and feature list for prediction
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_selection import SelectKBest, f_classif
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend (prevents tkinter crash)
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import json

# ============================================================
# PATHS
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_DIR, '..', 'dataset', 'smart_plant_biosensor.csv')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

# ============================================================
# 1. LOAD DATA
# ============================================================
def load_data():
    """Load the raw dataset from CSV."""
    df = pd.read_csv(DATASET_PATH)
    print(f"[INFO] Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"[INFO] Columns: {list(df.columns)}")
    print(f"\n[INFO] Target distribution:")
    print(df['Plant_Health_Status'].value_counts())
    return df


# ============================================================
# 2. CLEAN DATA
# ============================================================
def clean_data(df):
    """
    Clean the dataset:
    - Drop non-predictive columns (Timestamp, Plant_ID)
    - Handle missing values
    - Encode target variable
    """
    # Drop non-predictive columns
    columns_to_drop = ['Timestamp', 'Plant_ID']
    existing_drops = [col for col in columns_to_drop if col in df.columns]
    df_clean = df.drop(columns=existing_drops)
    print(f"[INFO] Dropped columns: {existing_drops}")

    # Check and handle missing values
    missing = df_clean.isnull().sum()
    if missing.sum() > 0:
        print(f"[WARNING] Missing values found:\n{missing[missing > 0]}")
        df_clean = df_clean.dropna()
        print(f"[INFO] Rows after dropping NaN: {df_clean.shape[0]}")
    else:
        print("[INFO] No missing values found")

    return df_clean


# ============================================================
# 3. EXPLORATORY DATA ANALYSIS
# ============================================================
def perform_eda(df_clean):
    """Generate EDA visualizations and save to results folder."""
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # --- Correlation Heatmap ---
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    plt.figure(figsize=(12, 10))
    corr_matrix = df_clean[numeric_cols].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='RdYlGn', center=0,
                fmt='.2f', linewidths=0.5, square=True)
    plt.title('Feature Correlation Heatmap', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'correlation_heatmap.png'), dpi=150)
    plt.close()
    print("[INFO] Saved correlation heatmap")

    # --- Feature Distribution by Health Status ---
    fig, axes = plt.subplots(3, 4, figsize=(20, 15))
    axes = axes.flatten()
    for i, col in enumerate(numeric_cols):
        if i < len(axes):
            for status in df_clean['Plant_Health_Status'].unique():
                subset = df_clean[df_clean['Plant_Health_Status'] == status]
                axes[i].hist(subset[col], alpha=0.5, label=status, bins=20)
            axes[i].set_title(col, fontsize=10)
            axes[i].legend(fontsize=7)
    # Hide unused subplots
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)
    plt.suptitle('Feature Distributions by Plant Health Status', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'feature_distributions.png'), dpi=150)
    plt.close()
    print("[INFO] Saved feature distributions plot")

    # --- Class Distribution ---
    plt.figure(figsize=(8, 5))
    colors = ['#2ecc71', '#f39c12', '#e74c3c']
    df_clean['Plant_Health_Status'].value_counts().plot(kind='bar', color=colors, edgecolor='black')
    plt.title('Plant Health Status Distribution', fontsize=16, fontweight='bold')
    plt.xlabel('Health Status')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'class_distribution.png'), dpi=150)
    plt.close()
    print("[INFO] Saved class distribution plot")

    return corr_matrix


# ============================================================
# 4. FEATURE SELECTION
# ============================================================
def select_features(X, y, k='all'):
    """
    Perform feature selection using SelectKBest with f_classif.
    Returns selected feature names and their scores.
    """
    selector = SelectKBest(score_func=f_classif, k=k)
    selector.fit(X, y)

    scores = pd.DataFrame({
        'Feature': X.columns,
        'F_Score': selector.scores_,
        'P_Value': selector.pvalues_
    }).sort_values('F_Score', ascending=False)

    print("\n[INFO] Feature Selection Scores (SelectKBest - f_classif):")
    print(scores.to_string(index=False))

    # Plot feature importance
    plt.figure(figsize=(10, 6))
    colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(scores)))
    bars = plt.barh(scores['Feature'], scores['F_Score'], color=colors, edgecolor='black')
    plt.xlabel('F-Score', fontsize=12)
    plt.title('Feature Importance (F-Score)', fontsize=16, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'feature_importance.png'), dpi=150)
    plt.close()
    print("[INFO] Saved feature importance plot")

    # Save feature scores
    scores.to_csv(os.path.join(RESULTS_DIR, 'feature_scores.csv'), index=False)

    return scores


# ============================================================
# 5. PREPARE DATA (Main Pipeline)
# ============================================================
def prepare_data(test_size=0.2, random_state=42):
    """
    Main preprocessing pipeline:
    1. Load → Clean → EDA → Feature Selection → Scale → Split
    Returns X_train, X_test, y_train, y_test, feature_names, label_encoder
    """
    # Load and clean
    df = load_data()
    df_clean = clean_data(df)

    # Perform EDA
    perform_eda(df_clean)

    # Separate features and target
    X = df_clean.drop(columns=['Plant_Health_Status'])
    y = df_clean['Plant_Health_Status']

    # Encode target labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    print(f"\n[INFO] Label encoding: {dict(zip(le.classes_, le.transform(le.classes_)))}")

    # Feature selection analysis (informational, we keep all features)
    feature_scores = select_features(X, y_encoded)
    feature_names = list(X.columns)

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=feature_names)

    # Train/test split (stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded,
        test_size=test_size,
        random_state=random_state,
        stratify=y_encoded
    )

    print(f"\n[INFO] Train set: {X_train.shape[0]} samples")
    print(f"[INFO] Test set: {X_test.shape[0]} samples")
    print(f"[INFO] Features used: {feature_names}")

    # Save scaler, label encoder, and feature names
    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(scaler, os.path.join(MODELS_DIR, 'scaler.pkl'))
    joblib.dump(le, os.path.join(MODELS_DIR, 'label_encoder.pkl'))

    with open(os.path.join(MODELS_DIR, 'feature_names.json'), 'w') as f:
        json.dump(feature_names, f)

    print("[INFO] Saved scaler.pkl, label_encoder.pkl, and feature_names.json")

    return X_train, X_test, y_train, y_test, feature_names, le


# ============================================================
# RUN STANDALONE
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print("  PREPROCESSING PIPELINE")
    print("  Plant Stress Level Classification")
    print("=" * 60)
    X_train, X_test, y_train, y_test, features, le = prepare_data()
    print("\n" + "=" * 60)
    print("  PREPROCESSING COMPLETE!")
    print("=" * 60)
