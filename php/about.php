<?php include 'includes/header.php'; ?>

<section class="about-section">
    <div class="container">
        <div class="about-header">
            <h1><i class="fas fa-users" style="color: var(--primary-400);"></i> Our <span class="gradient-text">Team</span></h1>
            <p>Meet the team behind the Plant Stress Classification System</p>
        </div>

        <!-- Project Info Card -->
        <div class="card animate-on-scroll" style="max-width: 800px; margin: 0 auto 48px; text-align: center;">
            <div style="margin-bottom: 20px;">
                <span class="hero-badge" style="margin-bottom: 0;">
                    <i class="fas fa-graduation-cap"></i>
                    Semester Project — Machine Learning & Data Science
                </span>
            </div>
            <h2 style="font-family: var(--font-display); font-size: 1.5rem; margin-bottom: 12px;">
                A Web-Based Plant Stress Level Classification System<br>
                <span class="gradient-text">Using Machine Learning Based on Biosensor Data and Chlorophyll Content</span>
            </h2>
            <p style="color: var(--text-secondary); font-size: 0.95rem; line-height: 1.7; margin-top: 16px;">
                This project implements three machine learning algorithms — SVM, KNN, and Decision Tree — to classify plant health status from biosensor data. The models are trained with hyperparameter optimization using GridSearchCV and deployed through a PHP web interface.
            </p>
        </div>

        <!-- Team Cards -->
        <div class="team-grid">
            <?php foreach ($team as $index => $member): ?>
            <div class="card team-card animate-on-scroll">
                <div class="team-avatar">
                    <i class="fas fa-user"></i>
                </div>
                <h3><?= htmlspecialchars($member['name']) ?></h3>
                <span class="team-algo"><?= htmlspecialchars($member['algo_short']) ?></span>
                <p class="team-role"><?= htmlspecialchars($member['role']) ?></p>
                <p style="color: var(--text-muted); font-size: 0.8rem; margin-top: 8px;">
                    Algorithm: <?= htmlspecialchars($member['algorithm']) ?>
                </p>
            </div>
            <?php endforeach; ?>
        </div>

        <!-- Dataset Info -->
        <div class="card animate-on-scroll" style="max-width: 800px; margin: 48px auto 0;">
            <h3 style="font-family: var(--font-display); margin-bottom: 16px;">
                <i class="fas fa-database" style="color: var(--primary-400);"></i> Dataset Information
            </h3>
            <table class="input-table">
                <tr>
                    <td style="font-weight: 600; width: 180px;">Dataset</td>
                    <td>Smart Plant Biosensor Monitoring Dataset</td>
                </tr>
                <tr>
                    <td style="font-weight: 600;">Source</td>
                    <td>
                        <a href="https://www.kaggle.com/datasets/muqaddasejaz/smart-plant-biosensor-monitoring-dataset"
                           target="_blank" style="color: var(--primary-400);">
                            Kaggle <i class="fas fa-external-link-alt" style="font-size: 0.75rem;"></i>
                        </a>
                    </td>
                </tr>
                <tr>
                    <td style="font-weight: 600;">Rows</td>
                    <td>1,200</td>
                </tr>
                <tr>
                    <td style="font-weight: 600;">Features</td>
                    <td>14 columns (11 input features + 1 target + Timestamp + Plant_ID)</td>
                </tr>
                <tr>
                    <td style="font-weight: 600;">Target Variable</td>
                    <td>Plant_Health_Status (Healthy, Moderate Stress, High Stress)</td>
                </tr>
                <tr>
                    <td style="font-weight: 600;">License</td>
                    <td>MIT</td>
                </tr>
            </table>
        </div>

        <!-- Tech Stack -->
        <div class="card animate-on-scroll" style="max-width: 800px; margin: 24px auto 0;">
            <h3 style="font-family: var(--font-display); margin-bottom: 16px;">
                <i class="fas fa-code" style="color: var(--accent-blue);"></i> Technology Stack
            </h3>
            <div class="card-grid card-grid-2" style="gap: 16px;">
                <div style="padding: 16px; background: rgba(255,255,255,0.03); border-radius: var(--radius-md); border: 1px solid var(--border-glass);">
                    <h4 style="color: var(--accent-blue); font-size: 0.9rem; margin-bottom: 8px;">Machine Learning</h4>
                    <div class="tech-badges">
                        <span class="badge">Python 3.x</span>
                        <span class="badge">Scikit-Learn</span>
                        <span class="badge">Pandas</span>
                        <span class="badge">NumPy</span>
                        <span class="badge">Matplotlib</span>
                        <span class="badge">Seaborn</span>
                    </div>
                </div>
                <div style="padding: 16px; background: rgba(255,255,255,0.03); border-radius: var(--radius-md); border: 1px solid var(--border-glass);">
                    <h4 style="color: var(--primary-400); font-size: 0.9rem; margin-bottom: 8px;">Web Application</h4>
                    <div class="tech-badges">
                        <span class="badge">PHP</span>
                        <span class="badge">HTML5</span>
                        <span class="badge">CSS3</span>
                        <span class="badge">JavaScript</span>
                        <span class="badge">Font Awesome</span>
                    </div>
                </div>
            </div>
        </div>

    </div>
</section>

<?php include 'includes/footer.php'; ?>
