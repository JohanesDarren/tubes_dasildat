"""
train_dt.py - Decision Tree Model Training (Muhammad Hafizh Raharja)
=====================================================================
Decision Tree classifier with:
- GridSearchCV hyperparameter optimization
- StratifiedKFold cross-validation (k=5)
- Classification report & confusion matrix
- Tree visualization
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import (classification_report, confusion_matrix,
                             accuracy_score, ConfusionMatrixDisplay)
import joblib
import json
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preprocessing import prepare_data, MODELS_DIR, RESULTS_DIR


def train_decision_tree():
    """Train Decision Tree model with hyperparameter tuning."""
    print("\n" + "=" * 60)
    print("  DECISION TREE MODEL TRAINING")
    print("  By: Muhammad Hafizh Raharja")
    print("=" * 60)

    # 1. Prepare data
    X_train, X_test, y_train, y_test, feature_names, le = prepare_data()

    # 2. Define hyperparameter grid
    param_grid = {
        'max_depth': [3, 5, 7, 10, 15, None],
        'min_samples_split': [2, 5, 10, 20],
        'min_samples_leaf': [1, 2, 4, 8],
        'criterion': ['gini', 'entropy'],
        'max_features': ['sqrt', 'log2', None],
    }

    print(f"\n[DT] Hyperparameter grid:")
    for key, values in param_grid.items():
        print(f"  {key}: {values}")

    # 3. GridSearchCV with StratifiedKFold
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    dt = DecisionTreeClassifier(random_state=42)

    print(f"\n[DT] Running GridSearchCV (5-fold)...")
    start_time = time.time()

    grid_search = GridSearchCV(
        estimator=dt,
        param_grid=param_grid,
        cv=cv,
        scoring='accuracy',
        n_jobs=-1,
        verbose=1,
        return_train_score=True
    )
    grid_search.fit(X_train, y_train)

    elapsed = time.time() - start_time
    print(f"[DT] GridSearchCV completed in {elapsed:.1f} seconds")

    # 4. Best model results
    best_model = grid_search.best_estimator_
    best_params = grid_search.best_params_
    best_cv_score = grid_search.best_score_

    print(f"\n[DT] Best Parameters: {best_params}")
    print(f"[DT] Best CV Accuracy: {best_cv_score:.4f}")

    # 5. Evaluate on test set
    y_pred = best_model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)

    print(f"[DT] Test Accuracy: {test_accuracy:.4f}")
    print(f"\n[DT] Classification Report:")
    report = classification_report(y_test, y_pred, target_names=le.classes_)
    print(report)

    # 6. Save confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=le.classes_)
    disp.plot(cmap='Oranges', values_format='d')
    plt.title('Decision Tree - Confusion Matrix', fontsize=16, fontweight='bold')
    plt.tight_layout()
    cm_path = os.path.join(RESULTS_DIR, 'confusion_matrices', 'dt_confusion_matrix.png')
    os.makedirs(os.path.dirname(cm_path), exist_ok=True)
    plt.savefig(cm_path, dpi=150)
    plt.close()
    print(f"[DT] Saved confusion matrix")

    # 7. Tree visualization
    plt.figure(figsize=(24, 12))
    plot_tree(
        best_model,
        feature_names=feature_names,
        class_names=list(le.classes_),
        filled=True,
        rounded=True,
        fontsize=8,
        max_depth=4  # Limit depth for readability
    )
    plt.title('Decision Tree Visualization (max 4 levels shown)', fontsize=18, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'dt_tree_visualization.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[DT] Saved tree visualization")

    # 8. Feature importance from Decision Tree
    importances = best_model.feature_importances_
    feature_imp = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values('Importance', ascending=False)

    print(f"\n[DT] Feature Importance:")
    print(feature_imp.to_string(index=False))

    plt.figure(figsize=(10, 6))
    colors = plt.cm.YlOrRd(np.linspace(0.3, 0.9, len(feature_imp)))
    plt.barh(feature_imp['Feature'], feature_imp['Importance'], color=colors, edgecolor='black')
    plt.xlabel('Importance', fontsize=12)
    plt.title('Decision Tree - Feature Importance', fontsize=16, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'dt_feature_importance.png'), dpi=150)
    plt.close()
    print(f"[DT] Saved feature importance plot")

    # 9. Save model
    model_path = os.path.join(MODELS_DIR, 'dt_model.pkl')
    joblib.dump(best_model, model_path)
    print(f"[DT] Saved model to {model_path}")

    # 10. Save results
    results = {
        'model': 'Decision Tree',
        'author': 'Muhammad Hafizh Raharja',
        'best_params': {k: str(v) if v is not None else None for k, v in best_params.items()},
        'best_cv_accuracy': round(best_cv_score, 4),
        'test_accuracy': round(test_accuracy, 4),
        'classification_report': classification_report(y_test, y_pred,
                                                       target_names=le.classes_,
                                                       output_dict=True),
        'feature_importance': feature_imp.to_dict(orient='records'),
        'training_time_seconds': round(elapsed, 1)
    }

    results_path = os.path.join(RESULTS_DIR, 'dt_results.json')
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"[DT] Saved results to {results_path}")

    print("\n" + "=" * 60)
    print(f"  DECISION TREE TRAINING COMPLETE!")
    print(f"  Best Accuracy: {test_accuracy:.4f}")
    print("=" * 60)

    return best_model, results


if __name__ == '__main__':
    train_decision_tree()
