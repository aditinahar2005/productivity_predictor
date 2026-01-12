import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pandas as pd
import joblib
import traceback
import numpy as np

from backend.visualizations.visualize_data import (
    plot_histogram,
    plot_bar,
    plot_scatter,
    plot_line,
    plot_heatmap
)

app = Flask(__name__)
CORS(app)

try:
    model_path = os.path.join(os.path.dirname(__file__), 'model', 'model.pkl')
    print(f"Attempting to load model from: {model_path}")
    print(f"Model file exists: {os.path.exists(model_path)}")
    
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        print("Model loaded successfully!")
        print(f"Model type: {type(model)}")
        
        # Test if model has required methods
        if hasattr(model, 'predict'):
            print("Model has predict method")
            # Test with dummy data to ensure model works
            try:
                dummy_data = pd.DataFrame([{
                    'Mood': 5, 'Hour': 14, 'Week(day/end)': 0, 'SleepHours': 7,
                    'Distractions': 2, 'ConfidenceScore': 6, 'Completed': 1, 'DayOfWeek': 2
                }])
                test_pred = model.predict(dummy_data)
                print(f"Model test prediction successful: {test_pred}")
            except Exception as test_e:
                print(f"Model test failed: {test_e}")
                
        else:
            print("WARNING: Model doesn't have predict method")
    else:
        print("ERROR: Model file does not exist!")
        print("Please run: python backend/model/train_tasktype_model.py")
        model = None
        
except Exception as e:
    print(f"Error loading model: {e}")
    traceback.print_exc()
    model = None

# Path to your cleaned CSV file
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "productivity_log_may.csv")
print(f"Data path: {DATA_PATH}")
print(f"Data file exists: {os.path.exists(DATA_PATH)}")

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'Productivity Predictor API is running',
        'model_status': 'loaded' if model is not None else 'not loaded',
        'endpoints': {
            '/predict': 'POST - Get productivity predictions',
            '/visualize': 'POST - Generate visualizations',
            '/health': 'GET - Check API health',
            '/test': 'GET - Test endpoint'
        }
    })

@app.route('/test', methods=['GET'])
def test():
    return jsonify({
        'message': 'Backend is working!', 
        'model_loaded': model is not None,
        'model_type': str(type(model)) if model else None
    })

@app.route('/predict', methods=['POST'])
def predict():
    print("=== PREDICT REQUEST RECEIVED ===")
    
    if model is None:
        print("ERROR: Model is None - model failed to load")
        return jsonify({
            'error': 'Model not loaded. Please train the model first.',
            'solution': 'Run: python backend/model/train_tasktype_model.py'
        }), 500
    
    print("Model is loaded successfully")
    
    try:
        data = request.json
        print(f"Received data: {data}")
        
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        # Create DataFrame with the expected features for the model
        df = pd.DataFrame([{
            'Mood': data.get('Mood', 5),
            'Hour': data.get('Hour', 14),
            'Week(day/end)': data.get('Week(day/end)', 0),
            'SleepHours': data.get('SleepHours', 7),
            'Distractions': data.get('Distractions', 2),
            'ConfidenceScore': data.get('ConfidenceScore', 6),
            'Completed': data.get('Completed', 1),
            'DayOfWeek': data.get('DayOfWeek', 2)
        }])
        
        print(f"DataFrame created: {df}")
        print(f"DataFrame columns: {list(df.columns)}")
        print(f"DataFrame shape: {df.shape}")
        print(f"DataFrame dtypes: {df.dtypes}")
        
        # Ensure all values are numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Check for NaN values
        if df.isnull().any().any():
            print("WARNING: DataFrame contains NaN values")
            df = df.fillna(0)
            print(f"DataFrame after filling NaN: {df}")
        
        # Try prediction
        print("Attempting prediction...")
        pred = model.predict(df)[0]
        print(f"Prediction successful: {pred}")
        
        # Ensure prediction is an integer
        prediction_int = int(pred)
        print(f"Prediction as integer: {prediction_int}")
        
        return jsonify({'prediction': prediction_int})
        
    except Exception as e:
        print(f"PREDICTION ERROR: {e}")
        traceback.print_exc()
        return jsonify({
            'error': f'Prediction failed: {str(e)}',
            'details': 'Check backend logs for more information'
        }), 500

@app.route('/visualize', methods=['POST'])
def visualize():
    try:
        data = request.json
        graph_type = data.get("graphType")
        column1 = data.get("column1")
        column2 = data.get("column2")

        print(f"Visualization request: {graph_type}, {column1}, {column2}")

        # Validate inputs
        if not graph_type:
            return jsonify({"error": "Graph type is required"}), 400
        if not column1:
            return jsonify({"error": "Column1 is required"}), 400

        if not os.path.exists(DATA_PATH):
            return jsonify({"error": f"Data file not found at {DATA_PATH}"}), 404

        # Load and validate data
        df = pd.read_csv(DATA_PATH)
        print(f"Data loaded. Shape: {df.shape}, Columns: {list(df.columns)}")

        # Check if columns exist
        if column1 not in df.columns:
            return jsonify({"error": f"Column '{column1}' not found in data"}), 400
        
        if column2 and column2 not in df.columns:
            return jsonify({"error": f"Column '{column2}' not found in data"}), 400

        # Create plots directory
        plots_dir = os.path.join(os.path.dirname(__file__), "plots")
        os.makedirs(plots_dir, exist_ok=True)
        
        # Generate unique filename
        import time
        timestamp = str(int(time.time()))
        save_path = os.path.join(plots_dir, f"{graph_type}_{column1}_{timestamp}.png")
        print(f"Saving plot to: {save_path}")

        # Generate plot based on type
        try:
            if graph_type == "histogram":
                plot_histogram(df, column1, save_path)
            elif graph_type == "bar":
                if not column2:
                    return jsonify({"error": "Column2 is required for bar charts"}), 400
                plot_bar(df, column1, column2, save_path)
            elif graph_type == "scatter":
                if not column2:
                    return jsonify({"error": "Column2 is required for scatter plots"}), 400
                plot_scatter(df, column1, column2, save_path)
            elif graph_type == "line":
                plot_line(df, column1, save_path)
            elif graph_type == "heatmap":
                # Select only numeric columns for heatmap
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                df_numeric = df[numeric_cols]
                plot_heatmap(df_numeric, save_path)
            else:
                return jsonify({"error": f"Invalid graph type: {graph_type}"}), 400

        except Exception as plot_error:
            print(f"Plot generation error: {plot_error}")
            traceback.print_exc()
            return jsonify({"error": f"Failed to generate plot: {str(plot_error)}"}), 500

        # Check if file was created
        if os.path.exists(save_path):
            print(f"Plot saved successfully at: {save_path}")
            return send_file(save_path, mimetype='image/png', as_attachment=False)
        else:
            return jsonify({"error": "Plot file was not created"}), 500

    except Exception as e:
        print(f"Visualization error: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    health_info = {
        'status': 'healthy',
        'model_loaded': model is not None,
        'data_file_exists': os.path.exists(DATA_PATH),
        'model_file_path': os.path.join(os.path.dirname(__file__), 'model', 'model.pkl'),
        'data_file_path': DATA_PATH
    }
    
    if model is not None:
        health_info['model_type'] = str(type(model))
    
    return jsonify(health_info)

@app.route('/train-model', methods=['POST'])
def train_model():
    """Emergency endpoint to train model if it doesn't exist"""
    try:
        # Import and run training
        from backend.model.train_tasktype_model import train_tasktype_model
        
        # Check if data exists, if not create sample data
        if not os.path.exists(DATA_PATH):
            return jsonify({
                'error': 'Data file not found',
                'message': 'Please ensure data/productivity_log_may.csv exists'
            }), 404
        
        model_trained, mapping = train_tasktype_model(DATA_PATH)
        
        if model_trained:
            # Reload the model
            global model
            model_path = os.path.join(os.path.dirname(__file__), 'model', 'model.pkl')
            model = joblib.load(model_path)
            
            return jsonify({
                'message': 'Model trained and loaded successfully!',
                'model_loaded': True
            })
        else:
            return jsonify({'error': 'Model training failed'}), 500
            
    except Exception as e:
        print(f"Training error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("="*50)
    print("PRODUCTIVITY PREDICTOR API STARTING")
    print(f"Model loaded: {model is not None}")
    print(f"Data file exists: {os.path.exists(DATA_PATH)}")
    print("="*50)
    app.run(host="0.0.0.0", port=5000, debug=True)

