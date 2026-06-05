"""
predict.py - Prediction Bridge Script (PHP ↔ Python)
=====================================================
Called by PHP via exec() to make predictions.

Usage:
    python predict.py <model_type> <feature1> <feature2> ... <featureN>

    model_type: 'svm', 'knn', or 'dt'

Output:
    JSON string with prediction result

Example:
    python predict.py svm 45.2 28.5 22.1 65.0 5000 6.5 40.0 30.0 200.0 35.0 120.5
"""

import sys
import os
import json
import warnings
warnings.filterwarnings('ignore')  # Suppress sklearn warnings for clean JSON output
import joblib
import numpy as np
import pandas as pd

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')


def predict(model_type, features):
    """
    Make a prediction using the specified model.

    Args:
        model_type: 'svm', 'knn', or 'dt'
        features: list of float values (biosensor readings)

    Returns:
        dict with prediction, probabilities, and model info
    """
    try:
        # Load scaler and label encoder
        scaler = joblib.load(os.path.join(MODELS_DIR, 'scaler.pkl'))
        le = joblib.load(os.path.join(MODELS_DIR, 'label_encoder.pkl'))

        # Load feature names
        with open(os.path.join(MODELS_DIR, 'feature_names.json'), 'r') as f:
            feature_names = json.load(f)

        # Validate input
        if len(features) != len(feature_names):
            return {
                'success': False,
                'error': f'Expected {len(feature_names)} features, got {len(features)}',
                'expected_features': feature_names
            }

        # Load model
        model_map = {
            'svm': 'svm_model.pkl',
            'knn': 'knn_model.pkl',
            'dt': 'dt_model.pkl'
        }

        if model_type not in model_map:
            return {
                'success': False,
                'error': f'Unknown model type: {model_type}. Use: svm, knn, or dt'
            }

        model_path = os.path.join(MODELS_DIR, model_map[model_type])
        if not os.path.exists(model_path):
            return {
                'success': False,
                'error': f'Model file not found: {model_map[model_type]}. Run training first.'
            }

        model = joblib.load(model_path)

        # Scale features (use DataFrame with feature names to avoid sklearn warnings)
        features_df = pd.DataFrame([features], columns=feature_names)
        features_scaled = scaler.transform(features_df)

        # Predict
        prediction_encoded = model.predict(features_scaled)[0]
        prediction_label = le.inverse_transform([prediction_encoded])[0]

        # Get probabilities
        probabilities = model.predict_proba(features_scaled)[0]
        prob_dict = {}
        for i, cls in enumerate(le.classes_):
            prob_dict[cls] = round(float(probabilities[i]), 4)

        # Build result
        model_names = {
            'svm': 'Support Vector Machine (SVM)',
            'knn': 'K-Nearest Neighbors (KNN)',
            'dt': 'Decision Tree'
        }

        result = {
            'success': True,
            'prediction': prediction_label,
            'probabilities': prob_dict,
            'model_type': model_type,
            'model_name': model_names[model_type],
            'input_features': dict(zip(feature_names, features))
        }

        return result

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def predict_all(features):
    """Predict using all 3 models and return combined results."""
    results = {}
    for model_type in ['svm', 'knn', 'dt']:
        results[model_type] = predict(model_type, features)
    return {
        'success': True,
        'predictions': results
    }


if __name__ == '__main__':
    if len(sys.argv) < 3:
        error = {
            'success': False,
            'error': 'Usage: python predict.py <model_type|all> <feature1> <feature2> ... <featureN>',
            'example': 'python predict.py svm 45.2 28.5 22.1 65.0 5000 6.5 40.0 30.0 200.0 35.0 120.5'
        }
        print(json.dumps(error))
        sys.exit(1)

    model_type = sys.argv[1].lower()
    features = [float(x) for x in sys.argv[2:]]

    if model_type == 'all':
        result = predict_all(features)
    else:
        result = predict(model_type, features)

    print(json.dumps(result))
