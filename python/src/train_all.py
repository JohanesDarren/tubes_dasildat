"""
train_all.py - Master Training Script
=======================================
Trains all 3 models and generates comparison results.
Run this once to train SVM, KNN, and Decision Tree.
"""

import os
import sys
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from train_svm import train_svm
from train_knn import train_knn
from train_dt import train_decision_tree
from preprocessing import RESULTS_DIR


def generate_comparison(all_results):
    """Generate comparison chart and summary of all 3 models."""
    os.makedirs(RESULTS_DIR, exist_ok=True)

    models = [r['model'] for r in all_results]
    cv_accuracies = [r['best_cv_accuracy'] for r in all_results]
    test_accuracies = [r['test_accuracy'] for r in all_results]
    train_times = [r['training_time_seconds'] for r in all_results]

    # --- Comparison Bar Chart ---
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Accuracy comparison
    colors = ['#2ecc71', '#3498db', '#e67e22']
    x = np.arange(len(models))
    width = 0.35

    axes[0].bar(x - width/2, cv_accuracies, width, label='CV Accuracy', color=colors, alpha=0.7, edgecolor='black')
    axes[0].bar(x + width/2, test_accuracies, width, label='Test Accuracy', color=colors, edgecolor='black')
    axes[0].set_xlabel('Model')
    axes[0].set_ylabel('Accuracy')
    axes[0].set_title('Model Accuracy Comparison', fontsize=14, fontweight='bold')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(models)
    axes[0].legend()
    axes[0].set_ylim(0, 1.1)
    for i, (cv, test) in enumerate(zip(cv_accuracies, test_accuracies)):
        axes[0].text(i - width/2, cv + 0.02, f'{cv:.3f}', ha='center', fontsize=9)
        axes[0].text(i + width/2, test + 0.02, f'{test:.3f}', ha='center', fontsize=9)

    # Per-class F1-Score comparison
    classes = list(all_results[0]['classification_report'].keys())
    classes = [c for c in classes if c not in ['accuracy', 'macro avg', 'weighted avg']]

    for i, cls in enumerate(classes):
        f1_scores = [r['classification_report'][cls]['f1-score'] for r in all_results]
        axes[1].bar(x + (i - 1) * width * 0.8, f1_scores, width * 0.8,
                    label=cls, alpha=0.85, edgecolor='black')
    axes[1].set_xlabel('Model')
    axes[1].set_ylabel('F1-Score')
    axes[1].set_title('F1-Score per Class', fontsize=14, fontweight='bold')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(models)
    axes[1].legend()
    axes[1].set_ylim(0, 1.1)

    # Training time comparison
    axes[2].bar(models, train_times, color=colors, edgecolor='black')
    axes[2].set_xlabel('Model')
    axes[2].set_ylabel('Time (seconds)')
    axes[2].set_title('Training Time Comparison', fontsize=14, fontweight='bold')
    for i, t in enumerate(train_times):
        axes[2].text(i, t + 0.5, f'{t:.1f}s', ha='center', fontsize=10)

    plt.suptitle('Model Comparison - Plant Stress Classification',
                 fontsize=18, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, 'model_comparison.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("\n[COMPARE] Saved model comparison chart")

    # --- Save comparison JSON ---
    best_model = max(all_results, key=lambda x: x['test_accuracy'])
    comparison = {
        'models': all_results,
        'best_model': {
            'name': best_model['model'],
            'test_accuracy': best_model['test_accuracy'],
            'author': best_model['author']
        }
    }

    comparison_path = os.path.join(RESULTS_DIR, 'model_comparison.json')
    with open(comparison_path, 'w') as f:
        json.dump(comparison, f, indent=2)
    print(f"[COMPARE] Saved comparison results to {comparison_path}")

    # --- Print summary ---
    print("\n" + "=" * 60)
    print("  MODEL COMPARISON SUMMARY")
    print("=" * 60)
    print(f"\n{'Model':<20} {'CV Accuracy':<15} {'Test Accuracy':<15} {'Time':<10}")
    print("-" * 60)
    for r in all_results:
        print(f"{r['model']:<20} {r['best_cv_accuracy']:<15.4f} {r['test_accuracy']:<15.4f} {r['training_time_seconds']:<10.1f}s")
    print("-" * 60)
    print(f"\n[BEST] Best Model: {best_model['model']} (Test Accuracy: {best_model['test_accuracy']:.4f})")
    print(f"   By: {best_model['author']}")

    return comparison


def main():
    print("=" * 60)
    print("  TRAINING ALL MODELS")
    print("  Plant Stress Level Classification System")
    print("=" * 60)

    all_results = []

    # Train SVM
    _, svm_results = train_svm()
    all_results.append(svm_results)

    # Train KNN
    _, knn_results = train_knn()
    all_results.append(knn_results)

    # Train Decision Tree
    _, dt_results = train_decision_tree()
    all_results.append(dt_results)

    # Generate comparison
    generate_comparison(all_results)

    print("\n" + "=" * 60)
    print("  ALL TRAINING COMPLETE!")
    print("=" * 60)


if __name__ == '__main__':
    main()
