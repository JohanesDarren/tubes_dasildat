<?php
include 'includes/header.php';

// Validate POST request
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: predict.php');
    exit;
}

// Get form data
$model_type = $_POST['model'] ?? 'all';
$feature_values = [];

foreach ($features as $feature) {
    $value = $_POST[$feature['name']] ?? '';
    if ($value === '' || !is_numeric($value)) {
        $error = "Please fill in all biosensor values correctly.";
        break;
    }
    $feature_values[] = floatval($value);
}

// Build feature string for Python
$feature_string = implode(' ', $feature_values);

// Call Python predict.py
$command = escapeshellcmd("$python_path \"$predict_script\" $model_type $feature_string");
$output = shell_exec($command . " 2>&1");
$result = json_decode($output, true);

// Determine status CSS class
function getStatusClass($prediction) {
    $prediction = strtolower($prediction);
    if (strpos($prediction, 'healthy') !== false && strpos($prediction, 'stress') === false) {
        return 'healthy';
    } elseif (strpos($prediction, 'moderate') !== false) {
        return 'moderate';
    } else {
        return 'stress';
    }
}

// Get status icon
function getStatusIcon($prediction) {
    $prediction = strtolower($prediction);
    if (strpos($prediction, 'healthy') !== false && strpos($prediction, 'stress') === false) {
        return 'fas fa-heart';
    } elseif (strpos($prediction, 'moderate') !== false) {
        return 'fas fa-exclamation-triangle';
    } else {
        return 'fas fa-times-circle';
    }
}
?>

<section class="result-section">
    <div class="container">
        <div class="result-container">

            <?php if (isset($error)): ?>
                <div class="alert alert-error">
                    <i class="fas fa-exclamation-circle"></i>
                    <?= htmlspecialchars($error) ?>
                </div>
                <div style="text-align: center; margin-top: 24px;">
                    <a href="predict.php" class="btn btn-primary">
                        <i class="fas fa-arrow-left"></i> Back to Prediction Form
                    </a>
                </div>

            <?php elseif (!$result || (isset($result['success']) && !$result['success'])): ?>
                <div class="alert alert-error">
                    <i class="fas fa-exclamation-circle"></i>
                    Error: <?= htmlspecialchars($result['error'] ?? 'Failed to get prediction. Make sure Python and models are properly configured.') ?>
                </div>
                <?php if ($output): ?>
                <div class="card" style="margin-top: 16px;">
                    <h3 style="margin-bottom: 12px; color: var(--text-secondary);">Debug Output</h3>
                    <pre style="color: var(--text-muted); font-size: 0.85rem; overflow-x: auto; white-space: pre-wrap;"><?= htmlspecialchars($output) ?></pre>
                </div>
                <?php endif; ?>
                <div style="text-align: center; margin-top: 24px;">
                    <a href="predict.php" class="btn btn-primary">
                        <i class="fas fa-arrow-left"></i> Back to Prediction Form
                    </a>
                </div>

            <?php elseif ($model_type === 'all' && isset($result['predictions'])): ?>
                <!-- ALL MODELS COMPARISON -->
                <div class="predict-header">
                    <h1><i class="fas fa-chart-bar" style="color: var(--primary-400);"></i> Comparison <span class="gradient-text">Results</span></h1>
                    <p>Predictions from all three machine learning models</p>
                </div>

                <div class="card-grid card-grid-3" style="margin-bottom: 32px;">
                    <?php
                    $model_colors = ['svm' => 'green', 'knn' => 'blue', 'dt' => 'orange'];
                    $model_labels = ['svm' => 'SVM', 'knn' => 'KNN', 'dt' => 'Decision Tree'];

                    foreach ($result['predictions'] as $mtype => $mresult):
                        if (!$mresult['success']) continue;
                        $statusClass = getStatusClass($mresult['prediction']);
                        $statusIcon = getStatusIcon($mresult['prediction']);
                    ?>
                    <div class="card animate-slide-up" style="text-align: center;">
                        <div style="margin-bottom: 16px;">
                            <span class="badge" style="font-size: 0.85rem; padding: 8px 16px;"><?= $model_labels[$mtype] ?></span>
                        </div>
                        <div class="result-status <?= $statusClass ?>" style="font-size: 1.1rem; padding: 12px 20px;">
                            <i class="<?= $statusIcon ?>"></i>
                            <?= htmlspecialchars($mresult['prediction']) ?>
                        </div>
                        <?php if (isset($mresult['probabilities'])): ?>
                        <div style="margin-top: 20px;">
                            <?php foreach ($mresult['probabilities'] as $cls => $prob): ?>
                            <div style="margin-bottom: 12px; text-align: left;">
                                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                                    <span style="font-size: 0.8rem; color: var(--text-secondary);"><?= htmlspecialchars($cls) ?></span>
                                    <span style="font-size: 0.8rem; font-weight: 600;"><?= round($prob * 100, 1) ?>%</span>
                                </div>
                                <div class="probability-bar">
                                    <div class="probability-bar-fill <?= getStatusClass($cls) ?>"
                                         data-width="<?= round($prob * 100, 1) ?>"
                                         style="width: 0%;"></div>
                                </div>
                            </div>
                            <?php endforeach; ?>
                        </div>
                        <?php endif; ?>
                    </div>
                    <?php endforeach; ?>
                </div>

                <!-- Input Summary -->
                <div class="card input-summary">
                    <h3><i class="fas fa-clipboard-list"></i> Input Summary</h3>
                    <table class="input-table">
                        <thead>
                            <tr>
                                <th>Feature</th>
                                <th>Value</th>
                                <th>Unit</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($features as $i => $feature): ?>
                            <tr>
                                <td><?= htmlspecialchars($feature['label']) ?></td>
                                <td><strong><?= htmlspecialchars($feature_values[$i]) ?></strong></td>
                                <td style="color: var(--text-muted);"><?= htmlspecialchars($feature['unit']) ?></td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>

                <div style="text-align: center; margin-top: 32px;">
                    <a href="predict.php" class="btn btn-primary">
                        <i class="fas fa-redo"></i> New Prediction
                    </a>
                </div>

            <?php else: ?>
                <!-- SINGLE MODEL RESULT -->
                <div class="predict-header">
                    <h1><i class="fas fa-leaf" style="color: var(--primary-400);"></i> Prediction <span class="gradient-text">Result</span></h1>
                </div>

                <?php
                $statusClass = getStatusClass($result['prediction']);
                $statusIcon = getStatusIcon($result['prediction']);
                ?>

                <div class="card result-card animate-slide-up">
                    <div class="result-status <?= $statusClass ?>">
                        <i class="<?= $statusIcon ?>"></i>
                        <?= htmlspecialchars($result['prediction']) ?>
                    </div>
                    <p class="result-model-name">
                        Predicted by: <strong><?= htmlspecialchars($result['model_name'] ?? strtoupper($model_type)) ?></strong>
                    </p>

                    <?php if (isset($result['probabilities'])): ?>
                    <div class="probability-grid">
                        <?php foreach ($result['probabilities'] as $cls => $prob):
                            $probClass = getStatusClass($cls);
                        ?>
                        <div class="probability-item">
                            <div class="probability-label"><?= htmlspecialchars($cls) ?></div>
                            <div class="probability-value" style="color: var(--status-<?= $probClass ?>);">
                                <?= round($prob * 100, 1) ?>%
                            </div>
                            <div class="probability-bar">
                                <div class="probability-bar-fill <?= $probClass ?>"
                                     data-width="<?= round($prob * 100, 1) ?>"
                                     style="width: 0%;"></div>
                            </div>
                        </div>
                        <?php endforeach; ?>
                    </div>
                    <?php endif; ?>
                </div>

                <!-- Input Summary -->
                <div class="card input-summary">
                    <h3><i class="fas fa-clipboard-list"></i> Input Summary</h3>
                    <table class="input-table">
                        <thead>
                            <tr>
                                <th>Feature</th>
                                <th>Value</th>
                                <th>Unit</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($features as $i => $feature): ?>
                            <tr>
                                <td><?= htmlspecialchars($feature['label']) ?></td>
                                <td><strong><?= htmlspecialchars($feature_values[$i]) ?></strong></td>
                                <td style="color: var(--text-muted);"><?= htmlspecialchars($feature['unit']) ?></td>
                            </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>

                <div style="text-align: center; margin-top: 32px;">
                    <a href="predict.php" class="btn btn-primary">
                        <i class="fas fa-redo"></i> New Prediction
                    </a>
                </div>
            <?php endif; ?>

        </div>
    </div>
</section>

<?php include 'includes/footer.php'; ?>
