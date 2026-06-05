"""
train_svm.py - SVM Model Training (Afrisya Dwiky Mauliddinka)
==========================================================
Support Vector Machine classifier with:
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
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import (classification_report, confusion_matrix,
                             accuracy_score, ConfusionMatrixDisplay)
import joblib
import json
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preprocessing import prepare_data, MODELS_DIR, RESULTS_DIR


def train_svm():
    """Train SVM model with hyperparameter tuning."""
    print("\n" + "=" * 60)
    print("  SVM MODEL TRAINING")
    print("  By: Afrisya Dwiky Mauliddinka")
    print("=" * 60)

    # 1. Prepare data
    X_train, X_test, y_train, y_test, feature_names, le = prepare_data()

    # 2. Define hyperparameter grid
    param_grid = {
        'C': [0.1, 1, 10, 100],
        'kernel': ['linear', 'rbf', 'poly'],
        'gamma': ['scale', 'auto', 0.01, 0.1],
        'degree': [2, 3],  # Only used for poly kernel
    }

    print(f"\n[SVM] Hyperparameter grid:")
    for key, values in param_grid.items():
        print(f"  {key}: {values}")

    # 3. GridSearchCV with StratifiedKFold
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    svm = SVC(probability=True, random_state=42)

    print(f"\n[SVM] Running GridSearchCV (5-fold)...")
    start_time = time.time()

    grid_search = GridSearchCV(
        estimator=svm,
        param_grid=param_grid,
        cv=cv,
        scoring='accuracy',
        n_jobs=-1,
        verbose=1,
        return_train_score=True
    )
    grid_search.fit(X_train, y_train)

    elapsed = time.time() - start_time
    print(f"[SVM] GridSearchCV completed in {elapsed:.1f} seconds")

    # 4. Best model results
    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_
    best_cv_score = grid_search.best_score_

    print(f"\n[SVM] Best Parameters: {best_params}")
    print(f"[SVM] Best CV Accuracy: {best_cv_score:.4f}")

    # 5. Evaluate on test set
    y_pred = best_model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)

    print(f"[SVM] Test Accuracy: {test_accuracy:.4f}")
    print(f"\n[SVM] Classification Report:")
    report = classification_report(y_test, y_pred, target_names=le.classes_)
    print(report)

    # 6. Save confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=le.classes_)
    disp.plot(cmap='Greens', values_format='d')
    plt.title('SVM - Confusion Matrix', fontsize=16, fontweight='bold')
    plt.tight_layout()
    cm_path = os.path.join(RESULTS_DIR, 'confusion_matrices', 'svm_confusion_matrix.png')
    os.makedirs(os.path.dirname(cm_path), exist_ok=True)
    plt.savefig(cm_path, dpi=150)
    plt.close()
    print(f"[SVM] Saved confusion matrix")

    # 7. Save model
    model_path = os.path.join(MODELS_DIR, 'svm_model.pkl')
    joblib.dump(best_model, model_path)
    print(f"[SVM] Saved model to {model_path}")

    # 8. Save results
    results = {
        'model': 'SVM',
        'author': 'Afrisya Dwiky Mauliddinka',
        'best_params': best_params,
        'best_cv_accuracy': round(best_cv_score, 4),
        'test_accuracy': round(test_accuracy, 4),
        'classification_report': classification_report(y_test, y_pred,
                                                       target_names=le.classes_,
                                                       output_dict=True),
        'training_time_seconds': round(elapsed, 1)
    }

    results_path = os.path.join(RESULTS_DIR, 'svm_results.json')
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"[SVM] Saved results to {results_path}")

    # 9. Cross-validation score details
    cv_results = pd.DataFrame({
        'Fold': range(1, 6),
        'Score': grid_search.cv_results_['mean_test_score'][:5]
    })
    print(f"\n[SVM] Cross-validation fold scores:")
    print(cv_results.to_string(index=False))

    print("\n" + "=" * 60)
    print(f"  SVM TRAINING COMPLETE!")
    print(f"  Best Accuracy: {test_accuracy:.4f}")
    print("=" * 60)

    return best_model, results


if __name__ == '__main__':
    train_svm()
