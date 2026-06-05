<?php
/**
 * config.php - Application Configuration
 * =======================================
 * Centralized configuration for the Plant Stress Classification System.
 */

// Python executable path
// Change this if Python is installed elsewhere
$python_path = 'C:/Users/User/AppData/Local/Programs/Python/Python313/python.exe';

// Project paths
$project_root = realpath(__DIR__ . '/../../');
$predict_script = $project_root . '/python/src/predict.py';
$results_dir = $project_root . '/python/results';
$models_dir = $project_root . '/python/models';

// Application info
$app_name = 'PlantSense AI';
$app_description = 'Web-Based Plant Stress Level Classification System Using Machine Learning';
$app_version = '1.0.0';

// Team members
$team = [
    [
        'name' => 'Johanes Darren Yehuda',
        'algorithm' => 'Support Vector Machine (SVM)',
        'algo_short' => 'SVM',
        'role' => 'Model Training & Hyperparameter Tuning'
    ],
    [
        'name' => 'Afrisya Dwiky Mauliddinka',
        'algorithm' => 'K-Nearest Neighbors (KNN)',
        'algo_short' => 'KNN',
        'role' => 'Model Training & Hyperparameter Tuning'
    ],
    [
        'name' => 'Muhammad Hafizh Raharja',
        'algorithm' => 'Decision Tree',
        'algo_short' => 'Decision Tree',
        'role' => 'Model Training & Hyperparameter Tuning'
    ]
];

// Feature definitions for the input form
$features = [
    [
        'name' => 'soil_moisture',
        'label' => 'Soil Moisture',
        'unit' => '%',
        'min' => 0, 'max' => 100, 'step' => 0.1,
        'placeholder' => 'e.g. 45.2',
        'description' => 'Water content in the soil'
    ],
    [
        'name' => 'ambient_temp',
        'label' => 'Ambient Temperature',
        'unit' => '°C',
        'min' => -10, 'max' => 60, 'step' => 0.1,
        'placeholder' => 'e.g. 28.5',
        'description' => 'Surrounding air temperature'
    ],
    [
        'name' => 'soil_temp',
        'label' => 'Soil Temperature',
        'unit' => '°C',
        'min' => -5, 'max' => 50, 'step' => 0.1,
        'placeholder' => 'e.g. 22.1',
        'description' => 'Temperature around plant roots'
    ],
    [
        'name' => 'humidity',
        'label' => 'Humidity',
        'unit' => '%',
        'min' => 0, 'max' => 100, 'step' => 0.1,
        'placeholder' => 'e.g. 65.0',
        'description' => 'Air moisture level'
    ],
    [
        'name' => 'light_intensity',
        'label' => 'Light Intensity',
        'unit' => 'Lux',
        'min' => 0, 'max' => 120000, 'step' => 1,
        'placeholder' => 'e.g. 5000',
        'description' => 'Amount of light for photosynthesis'
    ],
    [
        'name' => 'soil_ph',
        'label' => 'Soil pH',
        'unit' => '',
        'min' => 0, 'max' => 14, 'step' => 0.1,
        'placeholder' => 'e.g. 6.5',
        'description' => 'Soil acidity or alkalinity'
    ],
    [
        'name' => 'nitrogen',
        'label' => 'Nitrogen Level',
        'unit' => 'mg/kg',
        'min' => 0, 'max' => 500, 'step' => 0.1,
        'placeholder' => 'e.g. 40.0',
        'description' => 'Key nutrient for leaf growth'
    ],
    [
        'name' => 'phosphorus',
        'label' => 'Phosphorus Level',
        'unit' => 'mg/kg',
        'min' => 0, 'max' => 500, 'step' => 0.1,
        'placeholder' => 'e.g. 30.0',
        'description' => 'Essential for root and flower development'
    ],
    [
        'name' => 'potassium',
        'label' => 'Potassium Level',
        'unit' => 'mg/kg',
        'min' => 0, 'max' => 1000, 'step' => 0.1,
        'placeholder' => 'e.g. 200.0',
        'description' => 'Improves resilience and water regulation'
    ],
    [
        'name' => 'chlorophyll',
        'label' => 'Chlorophyll Content',
        'unit' => 'mg/m²',
        'min' => 0, 'max' => 100, 'step' => 0.1,
        'placeholder' => 'e.g. 35.0',
        'description' => 'Indicator of photosynthetic activity'
    ],
    [
        'name' => 'electrochemical',
        'label' => 'Electrochemical Signal',
        'unit' => 'mV',
        'min' => -500, 'max' => 500, 'step' => 0.1,
        'placeholder' => 'e.g. 120.5',
        'description' => 'Plant stress signal from biosensor'
    ]
];

// Get current page for active nav highlighting
function getCurrentPage() {
    $currentFile = basename($_SERVER['PHP_SELF']);
    return pathinfo($currentFile, PATHINFO_FILENAME);
}
?>
