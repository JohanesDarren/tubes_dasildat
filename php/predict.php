<?php include 'includes/header.php'; ?>

    <section class="predict-section">
        <div class="container">
            <div class="predict-header">
                <h1><i class="fas fa-microscope" style="color: var(--primary-400);"></i> Plant Stress <span class="gradient-text">Prediction</span></h1>
                <p>Enter your biosensor readings below to classify the plant's health status</p>
            </div>

            <div class="predict-form-card">
                <form id="predictForm" action="result.php" method="POST">

                    <div class="form-grid">
                        <?php foreach ($features as $feature): ?>
                        <div class="form-group">
                            <label for="<?= $feature['name'] ?>">
                                <?= htmlspecialchars($feature['label']) ?>
                                <?php if ($feature['unit']): ?>
                                    <span class="unit">(<?= $feature['unit'] ?>)</span>
                                <?php endif; ?>
                            </label>
                            <input
                                type="number"
                                id="<?= $feature['name'] ?>"
                                name="<?= $feature['name'] ?>"
                                step="<?= $feature['step'] ?>"
                                min="<?= $feature['min'] ?>"
                                max="<?= $feature['max'] ?>"
                                placeholder="<?= $feature['placeholder'] ?>"
                                required
                            >
                            <span class="form-hint"><?= htmlspecialchars($feature['description']) ?></span>
                        </div>
                        <?php endforeach; ?>

                        <!-- Model Selection -->
                        <div class="form-group form-model-select">
                            <label for="model">
                                <i class="fas fa-brain"></i> Select ML Model
                            </label>
                            <select id="model" name="model" required>
                                <option value="all">🔄 All Models (Compare Results)</option>
                                <option value="svm">🟢 SVM - Support Vector Machine</option>
                                <option value="knn">🔵 KNN - K-Nearest Neighbors</option>
                                <option value="dt">🟠 Decision Tree</option>
                            </select>
                            <span class="form-hint">Choose a specific model or compare predictions from all three algorithms</span>
                        </div>
                    </div>

                    <div class="form-actions">
                        <button type="submit" class="btn btn-primary btn-lg">
                            <i class="fas fa-search"></i> Classify Plant Stress
                        </button>
                        <button type="reset" class="btn btn-secondary">
                            <i class="fas fa-undo"></i> Reset Form
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </section>

<?php include 'includes/footer.php'; ?>
