<?php
include 'includes/header.php';

// Load comparison results
$comparison_file = $results_dir . '/model_comparison.json';
$comparison = null;
if (file_exists($comparison_file)) {
    $comparison = json_decode(file_get_contents($comparison_file), true);
}

// Load individual model results
$svm_results_file = $results_dir . '/svm_results.json';
$knn_results_file = $results_dir . '/knn_results.json';
$dt_results_file = $results_dir . '/dt_results.json';

$svm_results = file_exists($svm_results_file) ? json_decode(file_get_contents($svm_results_file), true) : null;
$knn_results = file_exists($knn_results_file) ? json_decode(file_get_contents($knn_results_file), true) : null;
$dt_results = file_exists($dt_results_file) ? json_decode(file_get_contents($dt_results_file), true) : null;

$all_results = array_filter([$svm_results, $knn_results, $dt_results]);
?>

<section class="comparison-section">
    <div class="container">
        <div class="comparison-header">
            <h1><i class="fas fa-chart-bar" style="color: var(--primary-400);"></i> Model <span class="gradient-text">Comparison</span></h1>
            <p>Performance comparison of SVM, KNN, and Decision Tree classifiers</p>
        </div>

        <?php if (empty($all_results)): ?>
            <div class="alert alert-warning">
                <i class="fas fa-exclamation-triangle"></i>
                No model results found. Please train the models first by running <code>python python/src/train_all.py</code>
            </div>
        <?php else: ?>

            <!-- Overall Accuracy Table -->
            <div class="comparison-table-wrapper animate-on-scroll">
                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th>Model</th>
                            <th>Author</th>
                            <th>CV Accuracy</th>
                            <th>Test Accuracy</th>
                            <th>Training Time</th>
                            <th>Best Parameters</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php
                        // Find best test accuracy
                        $best_accuracy = max(array_column($all_results, 'test_accuracy'));

                        foreach ($all_results as $r):
                            $isBest = $r['test_accuracy'] === $best_accuracy;
                        ?>
                        <tr>
                            <td>
                                <strong><?= htmlspecialchars($r['model']) ?></strong>
                                <?php if ($isBest): ?>
                                    <span style="color: var(--primary-400); font-size: 0.75rem;"> 🏆 Best</span>
                                <?php endif; ?>
                            </td>
                            <td style="color: var(--text-secondary);"><?= htmlspecialchars($r['author']) ?></td>
                            <td class="<?= $isBest ? 'best-value' : '' ?>">
                                <?= number_format($r['best_cv_accuracy'] * 100, 2) ?>%
                            </td>
                            <td class="<?= $isBest ? 'best-value' : '' ?>">
                                <?= number_format($r['test_accuracy'] * 100, 2) ?>%
                            </td>
                            <td><?= $r['training_time_seconds'] ?>s</td>
                            <td>
                                <div style="max-width: 250px; font-size: 0.8rem; color: var(--text-muted);">
                                    <?php
                                    $params = [];
                                    foreach ($r['best_params'] as $k => $v) {
                                        $params[] = "$k=$v";
                                    }
                                    echo htmlspecialchars(implode(', ', $params));
                                    ?>
                                </div>
                            </td>
                        </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>

            <!-- Per-Class Metrics Table -->
            <h2 style="margin-bottom: 24px; font-family: var(--font-display);">
                Per-Class <span class="gradient-text">Metrics</span>
            </h2>

            <?php foreach ($all_results as $r):
                $report = $r['classification_report'] ?? [];
                $classes = array_filter(array_keys($report), function($k) {
                    return !in_array($k, ['accuracy', 'macro avg', 'weighted avg']);
                });
            ?>
            <div class="comparison-table-wrapper animate-on-scroll" style="margin-bottom: 24px;">
                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th colspan="5" style="font-size: 0.95rem; color: var(--text-primary);">
                                <?= htmlspecialchars($r['model']) ?> — Classification Report
                            </th>
                        </tr>
                        <tr>
                            <th>Class</th>
                            <th>Precision</th>
                            <th>Recall</th>
                            <th>F1-Score</th>
                            <th>Support</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($classes as $cls): ?>
                        <tr>
                            <td><strong><?= htmlspecialchars($cls) ?></strong></td>
                            <td><?= number_format($report[$cls]['precision'], 4) ?></td>
                            <td><?= number_format($report[$cls]['recall'], 4) ?></td>
                            <td><?= number_format($report[$cls]['f1-score'], 4) ?></td>
                            <td><?= $report[$cls]['support'] ?></td>
                        </tr>
                        <?php endforeach; ?>
                        <?php if (isset($report['weighted avg'])): ?>
                        <tr style="border-top: 2px solid var(--border-glass);">
                            <td><strong>Weighted Avg</strong></td>
                            <td><strong><?= number_format($report['weighted avg']['precision'], 4) ?></strong></td>
                            <td><strong><?= number_format($report['weighted avg']['recall'], 4) ?></strong></td>
                            <td><strong><?= number_format($report['weighted avg']['f1-score'], 4) ?></strong></td>
                            <td><strong><?= $report['weighted avg']['support'] ?></strong></td>
                        </tr>
                        <?php endif; ?>
                    </tbody>
                </table>
            </div>
            <?php endforeach; ?>

            <!-- Visualization Images -->
            <h2 style="margin: 48px 0 24px; font-family: var(--font-display);">
                <span class="gradient-text">Visualizations</span>
            </h2>

            <div class="comparison-images">
                <?php
                $images = [
                    ['file' => 'model_comparison.png', 'title' => 'Model Comparison Chart'],
                    ['file' => 'correlation_heatmap.png', 'title' => 'Feature Correlation Heatmap'],
                    ['file' => 'feature_importance.png', 'title' => 'Feature Importance (F-Score)'],
                    ['file' => 'feature_distributions.png', 'title' => 'Feature Distributions'],
                    ['file' => 'class_distribution.png', 'title' => 'Class Distribution'],
                    ['file' => 'confusion_matrices/svm_confusion_matrix.png', 'title' => 'SVM Confusion Matrix'],
                    ['file' => 'confusion_matrices/knn_confusion_matrix.png', 'title' => 'KNN Confusion Matrix'],
                    ['file' => 'confusion_matrices/dt_confusion_matrix.png', 'title' => 'Decision Tree Confusion Matrix'],
                    ['file' => 'dt_tree_visualization.png', 'title' => 'Decision Tree Visualization'],
                    ['file' => 'dt_feature_importance.png', 'title' => 'Decision Tree Feature Importance'],
                    ['file' => 'knn_k_vs_accuracy.png', 'title' => 'KNN: K Value vs Accuracy'],
                ];

                foreach ($images as $img):
                    $img_path = $results_dir . '/' . $img['file'];
                    if (file_exists($img_path)):
                ?>
                <div class="card comparison-img-card animate-on-scroll">
                    <h3><i class="fas fa-chart-area"></i> <?= htmlspecialchars($img['title']) ?></h3>
                    <img src="<?= '../python/results/' . $img['file'] ?>" alt="<?= htmlspecialchars($img['title']) ?>" loading="lazy">
                </div>
                <?php
                    endif;
                endforeach;
                ?>
            </div>

        <?php endif; ?>
    </div>
</section>

<?php include 'includes/footer.php'; ?>
