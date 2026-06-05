import os
import sys
import json
import warnings
import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

# Adjust path so we can locate models and results
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYTHON_DIR = os.path.join(BASE_DIR, 'python')
MODELS_DIR = os.path.join(PYTHON_DIR, 'models')
RESULTS_DIR = os.path.join(PYTHON_DIR, 'results')

def predict_single_model(model_type, features, feature_names, scaler, le):
    try:
        model_map = {
            'svm': 'svm_model.pkl',
            'knn': 'knn_model.pkl',
            'dt': 'dt_model.pkl'
        }
        if model_type not in model_map:
            return {'success': False, 'error': f'Unknown model type: {model_type}'}

        model_path = os.path.join(MODELS_DIR, model_map[model_type])
        if not os.path.exists(model_path):
            return {'success': False, 'error': f'Model not found: {model_map[model_type]}'}

        model = joblib.load(model_path)
        
        # Scale features
        features_df = pd.DataFrame([features], columns=feature_names)
        features_scaled = scaler.transform(features_df)

        # Predict
        prediction_encoded = model.predict(features_scaled)[0]
        prediction_label = le.inverse_transform([prediction_encoded])[0]

        # Probabilities
        probabilities = model.predict_proba(features_scaled)[0]
        prob_dict = {cls: round(float(prob), 4) for cls, prob in zip(le.classes_, probabilities)}

        model_names = {
            'svm': 'Support Vector Machine (SVM)',
            'knn': 'K-Nearest Neighbors (KNN)',
            'dt': 'Decision Tree'
        }

        return {
            'success': True,
            'prediction': prediction_label,
            'probabilities': prob_dict,
            'model_type': model_type,
            'model_name': model_names[model_type],
            'input_features': dict(zip(feature_names, features))
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        model_type = data.get('model', 'all')
        features_dict = data.get('features', {})
        
        # Load scaler and label encoder
        scaler = joblib.load(os.path.join(MODELS_DIR, 'scaler.pkl'))
        le = joblib.load(os.path.join(MODELS_DIR, 'label_encoder.pkl'))

        # Load feature names
        with open(os.path.join(MODELS_DIR, 'feature_names.json'), 'r') as f:
            feature_names = json.load(f)

        # Extract features in the correct order
        features = []
        for name in feature_names:
            if name not in features_dict:
                return jsonify({'success': False, 'error': f'Missing feature: {name}'}), 400
            features.append(float(features_dict[name]))

        if model_type == 'all':
            results = {}
            for m in ['svm', 'knn', 'dt']:
                results[m] = predict_single_model(m, features, feature_names, scaler, le)
            return jsonify({'success': True, 'predictions': results})
        else:
            result = predict_single_model(model_type, features, feature_names, scaler, le)
            return jsonify(result)
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/comparison', methods=['GET'])
def comparison():
    try:
        comparison_file = os.path.join(RESULTS_DIR, 'model_comparison.json')
        if not os.path.exists(comparison_file):
            return jsonify({'success': False, 'error': 'Comparison data not found.'}), 404
            
        with open(comparison_file, 'r') as f:
            data = json.load(f)
            
        # We might also want to send the individual model results for per-class metrics
        all_results = []
        for model in ['svm', 'knn', 'dt']:
            result_file = os.path.join(RESULTS_DIR, f'{model}_results.json')
            if os.path.exists(result_file):
                with open(result_file, 'r') as f2:
                    all_results.append(json.load(f2))
                    
        return jsonify({
            'success': True,
            'comparison': data,
            'all_results': all_results
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Vercel entrypoint
if __name__ == '__main__':
    app.run(debug=True, port=5050)
