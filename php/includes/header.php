<?php
/**
 * header.php - Shared Header Component
 */
require_once __DIR__ . '/config.php';
$currentPage = getCurrentPage();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="<?= htmlspecialchars($app_description) ?>">
    <title><?= htmlspecialchars($app_name) ?> - Plant Stress Classification</title>

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">

    <!-- Font Awesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

    <!-- Custom CSS -->
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar" id="navbar">
        <div class="nav-container">
            <a href="index.php" class="nav-brand">
                <span class="brand-icon"><i class="fas fa-leaf"></i></span>
                <span class="brand-text"><?= $app_name ?></span>
            </a>

            <button class="nav-toggle" id="navToggle" aria-label="Toggle navigation">
                <span></span>
                <span></span>
                <span></span>
            </button>

            <ul class="nav-menu" id="navMenu">
                <li><a href="index.php" class="nav-link <?= $currentPage === 'index' ? 'active' : '' ?>">
                    <i class="fas fa-home"></i> Home
                </a></li>
                <li><a href="predict.php" class="nav-link <?= $currentPage === 'predict' ? 'active' : '' ?>">
                    <i class="fas fa-microscope"></i> Predict
                </a></li>
                <li><a href="comparison.php" class="nav-link <?= $currentPage === 'comparison' ? 'active' : '' ?>">
                    <i class="fas fa-chart-bar"></i> Comparison
                </a></li>
                <li><a href="about.php" class="nav-link <?= $currentPage === 'about' ? 'active' : '' ?>">
                    <i class="fas fa-users"></i> Team
                </a></li>
            </ul>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="main-content">
