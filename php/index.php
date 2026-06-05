<?php include 'includes/header.php'; ?>

    <!-- Hero Section -->
    <section class="hero">
        <div class="hero-container">
            <div class="hero-content">
                <div class="hero-badge">
                    <i class="fas fa-seedling"></i>
                    Machine Learning • Biosensor Data • Classification
                </div>
                <h1>
                    Detect <span class="gradient-text">Plant Stress</span><br>
                    Before It's Too Late
                </h1>
                <p class="hero-subtitle">
                    A web-based classification system powered by SVM, KNN, and Decision Tree algorithms.
                    Analyze biosensor data and chlorophyll content to determine plant health status in real-time.
                </p>
                <div class="hero-actions">
                    <a href="predict.php" class="btn btn-primary btn-lg">
                        <i class="fas fa-microscope"></i> Start Prediction
                    </a>
                    <a href="comparison.php" class="btn btn-secondary btn-lg">
                        <i class="fas fa-chart-bar"></i> View Model Comparison
                    </a>
                </div>
            </div>
        </div>
    </section>

    <!-- Stats Section -->
    <section class="stats-section">
        <div class="stats-grid">
            <div class="stat-card animate-on-scroll">
                <div class="stat-icon green"><i class="fas fa-database"></i></div>
                <div class="stat-value" data-count="1200">0</div>
                <div class="stat-label">Data Points</div>
            </div>
            <div class="stat-card animate-on-scroll">
                <div class="stat-icon blue"><i class="fas fa-layer-group"></i></div>
                <div class="stat-value" data-count="11">0</div>
                <div class="stat-label">Biosensor Features</div>
            </div>
            <div class="stat-card animate-on-scroll">
                <div class="stat-icon purple"><i class="fas fa-brain"></i></div>
                <div class="stat-value" data-count="3">0</div>
                <div class="stat-label">ML Algorithms</div>
            </div>
            <div class="stat-card animate-on-scroll">
                <div class="stat-icon orange"><i class="fas fa-tags"></i></div>
                <div class="stat-value" data-count="3">0</div>
                <div class="stat-label">Stress Classes</div>
            </div>
        </div>
    </section>

    <!-- How It Works Section -->
    <section class="section">
        <div class="container">
            <div class="section-header">
                <h2>How It <span class="gradient-text">Works</span></h2>
                <p>Our system uses advanced machine learning to classify plant health from biosensor readings</p>
            </div>

            <div class="card-grid card-grid-3">
                <div class="card feature-card animate-on-scroll">
                    <div class="feature-icon" style="background: rgba(59, 130, 246, 0.15); color: var(--accent-blue);">
                        <i class="fas fa-upload"></i>
                    </div>
                    <h3>1. Input Sensor Data</h3>
                    <p>Enter your biosensor readings including soil moisture, temperature, pH, nutrient levels, and chlorophyll content into our prediction form.</p>
                </div>

                <div class="card feature-card animate-on-scroll">
                    <div class="feature-icon" style="background: rgba(139, 92, 246, 0.15); color: var(--accent-purple);">
                        <i class="fas fa-cogs"></i>
                    </div>
                    <h3>2. ML Processing</h3>
                    <p>Our trained models (SVM, KNN, Decision Tree) analyze your data using optimized hyperparameters and feature-scaled inputs.</p>
                </div>

                <div class="card feature-card animate-on-scroll">
                    <div class="feature-icon" style="background: rgba(16, 185, 129, 0.15); color: var(--primary-400);">
                        <i class="fas fa-leaf"></i>
                    </div>
                    <h3>3. Get Classification</h3>
                    <p>Receive an instant classification — Healthy, Moderate Stress, or High Stress — with confidence probabilities for each class.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Classification Classes -->
    <section class="section" style="border-top: 1px solid var(--border-glass);">
        <div class="container">
            <div class="section-header">
                <h2>Stress Level <span class="gradient-text">Classes</span></h2>
                <p>The system classifies plants into three health categories</p>
            </div>

            <div class="card-grid card-grid-3">
                <div class="card animate-on-scroll" style="border-top: 3px solid var(--status-healthy);">
                    <div style="text-align: center;">
                        <i class="fas fa-heart" style="font-size: 2.5rem; color: var(--status-healthy); margin-bottom: 16px;"></i>
                        <h3 style="color: var(--status-healthy); margin-bottom: 12px;">Healthy</h3>
                        <p style="color: var(--text-secondary); font-size: 0.9rem;">
                            Plant is thriving with optimal biosensor readings. Soil moisture, nutrients, and chlorophyll are within healthy ranges.
                        </p>
                    </div>
                </div>

                <div class="card animate-on-scroll" style="border-top: 3px solid var(--status-moderate);">
                    <div style="text-align: center;">
                        <i class="fas fa-exclamation-triangle" style="font-size: 2.5rem; color: var(--status-moderate); margin-bottom: 16px;"></i>
                        <h3 style="color: var(--status-moderate); margin-bottom: 12px;">Moderate Stress</h3>
                        <p style="color: var(--text-secondary); font-size: 0.9rem;">
                            Early signs of stress detected. Some parameters are deviating from optimal. Intervention recommended.
                        </p>
                    </div>
                </div>

                <div class="card animate-on-scroll" style="border-top: 3px solid var(--status-stress);">
                    <div style="text-align: center;">
                        <i class="fas fa-times-circle" style="font-size: 2.5rem; color: var(--status-stress); margin-bottom: 16px;"></i>
                        <h3 style="color: var(--status-stress); margin-bottom: 12px;">High Stress</h3>
                        <p style="color: var(--text-secondary); font-size: 0.9rem;">
                            Critical stress levels detected. Significant environmental or nutrient imbalances. Immediate action required.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </section>

<?php include 'includes/footer.php'; ?>
