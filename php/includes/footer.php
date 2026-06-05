    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-container">
            <div class="footer-content">
                <div class="footer-brand">
                    <span class="brand-icon"><i class="fas fa-leaf"></i></span>
                    <span class="brand-text"><?= $app_name ?></span>
                    <p class="footer-desc">Plant Stress Level Classification System<br>Using Machine Learning Based on Biosensor Data</p>
                </div>
                <div class="footer-links">
                    <h4>Quick Links</h4>
                    <a href="index.php">Home</a>
                    <a href="predict.php">Predict</a>
                    <a href="comparison.php">Model Comparison</a>
                    <a href="about.php">Our Team</a>
                </div>
                <div class="footer-tech">
                    <h4>Technologies</h4>
                    <div class="tech-badges">
                        <span class="badge">Python</span>
                        <span class="badge">Scikit-Learn</span>
                        <span class="badge">PHP</span>
                        <span class="badge">SVM</span>
                        <span class="badge">KNN</span>
                        <span class="badge">Decision Tree</span>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; <?= date('Y') ?> <?= $app_name ?>. Semester Project - Machine Learning & Data Science.</p>
            </div>
        </div>
    </footer>

    <!-- Custom JS -->
    <script src="assets/js/main.js"></script>
</body>
</html>
