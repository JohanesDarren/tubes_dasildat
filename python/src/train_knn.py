"""
train_knn.py - KNN Model Training (Afrisya Dwiky Mauliddinka)
==============================================================
K-Nearest Neighbors classifier with:
- GridSearchCV hyperparameter optimization
- StratifiedKFold cross-validation (k=5)
- Classification report & confusion matrix
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import (classification_report, confusion_matrix,
                             accuracy_score, ConfusionMatrixDisplay)
import joblib
import json
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preprocessing import prepare_data, MODELS_DIR, RESULTS_DIR


def train_knn():
    """Train KNN model with hyperparameter tuning."""
    print("\n" + "=" * 60)
    print("  KNN MODEL TRAINING")
    print("  By: Afrisya Dwiky Mauliddinka")
    print("=" * 60)

    # 1. Prepare data
    X_train, X_test, y_train, y_test, feature_names, le = prepare_data()

    # 2. Define hyperparameter grid
    param_grid = {
        'n_neighbors': [3, 5, 7, 9, 11, 13, 15],
        'weights': ['uniform', 'distance'],
        'metric': ['euclidean', 'manhattan', 'minkowski'],
        'p': [1, 2, 3],  # Power parameter for Minkowski
    }

    print(f"\n[KNN] Hyperparameter grid:")
    for key, values in param_grid.items():
        print(f"  {key}: {values}")

    # 3. GridSearchCV with StratifiedKFold
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    knn = KNeighborsClassifier()

    print(f"\n[KNN] Running GridSearchCV (5-fold)...")
    start_time = time.time()

    grid_search = GridSearchCV(
        estimator=knn,
        param_grid=param_grid,
        cv=cv,
        scoring='accuracy',
        n_jobs=-1,
        verbose=1,
        return_train_score=True
    )
    grid_search.fit(X_train, y_train)

    elapsed = time.time() - start_time
    print(f"[KNN] GridSearchCV completed in {elapsed:.1f} seconds")

    # 4. Best model results
    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_
    best_cv_score = grid_search.best_score_

    print(f"\n[KNN] Best Parameters: {best_params}")
    print(f"[KNN] Best CV Accuracy: {best_cv_score:.4f}")

    # 5. Evaluate on test set
    y_pred = best_model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)

    print(f"[KNN] Test Accuracy: {test_accuracy:.4f}")
    print(f"\n[KNN] Classification Report:")
    report = classification_report(y_test, y_pred, target_names=le.classes_)
    print(report)

    # 6. Save confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=le.classes_)
    disp.plot(cmap='Blues', values_format='d')
    plt.title('KNN - Confusion Matrix', fontsize=16, fontweight='bold')
    plt.tight_layout()
    cm_path = os.path.join(RESULTS_DIR, 'confusion_matrices', 'knn_confusion_matrix.png')
    os.makedirs(os.path.dirname(cm_path), exist_ok=True)
    plt.savefig(cm_path, dpi=150)
    plt.close()
    print(f"[KNN] Saved confusion matrix")

    # 7. K-value vs Accuracy plot
    k_range = range(1, 21)
    k_scores = []
    for k in k_range:
        knn_temp = KNeighborsClassifier(
            n_neighbors=k,
            weights=best_params.get('weights', 'uniform'),
            metric=best_params.get('metric', 'euclidean')
        )
        knn_temp.fit(X_train, y_train)
        k_scores.append(knn_temp.score(X_test, y_test))

    plt.figure(figsize=(10, 6))
    plt.plot(k_range, k_scores, 'bo-', linewidth=2, markersize=8)
    plt.fill_between(k_range, k_scores, alpha=0.1, color='blue')
    plt.xlabel('Number of Neighbors (K)', fontsize=12)
    plt.ylabel('Accuracy', fontsize=12)
    plt.title('KNN - K Value vs Accuracy', fontsize=16, fontweight='bold')
    plt.xticks(k_range)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'knn_k_vs_accuracy.png'), dpi=150)
    plt.close()
    print(f"[KNN] Saved K vs Accuracy plot")

    # 8. Save model
    model_path = os.path.join(MODELS_DIR, 'knn_model.pkl')
    joblib.dump(best_model, model_path)
    print(f"[KNN] Saved model to {model_path}")

    # 9. Save results
    results = {
        'model': 'KNN',
        'author': 'Afrisya Dwiky Mauliddinka',
        'best_params': best_params,
        'best_cv_accuracy': round(best_cv_score, 4),
        'test_accuracy': round(test_accuracy, 4),
        'classification_report': classification_report(y_test, y_pred,
                                                       target_names=le.classes_,
                                                       output_dict=True),
        'training_time_seconds': round(elapsed, 1)
    }

    results_path = os.path.join(RESULTS_DIR, 'knn_results.json')
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"[KNN] Saved results to {results_path}")

    print("\n" + "=" * 60)
    print(f"  KNN TRAINING COMPLETE!")
    print(f"  Best Accuracy: {test_accuracy:.4f}")
    print("=" * 60)

    return best_model, results


if __name__ == '__main__':
    train_knn()
