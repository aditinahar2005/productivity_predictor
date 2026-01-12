import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
from backend.model.preprocess import clean_pipeline

def train_tasktype_model(filepath):
    try:
        # Load and clean the data
        df_cleaned, mapping = clean_pipeline(filepath)
        print("Data loaded and cleaned successfully!")
        print(f"Data shape: {df_cleaned.shape}")
        print(f"Columns: {list(df_cleaned.columns)}")

        # Convert 'Time' column to datetime if it exists
        if 'Time' in df_cleaned.columns:
            df_cleaned['Time'] = pd.to_datetime(df_cleaned['Time'], errors='coerce')
            df_cleaned['Hour'] = df_cleaned['Time'].apply(lambda x: x.hour if pd.notnull(x) else 14)
        else:
            # If Time column doesn't exist, create a default Hour column
            df_cleaned['Hour'] = 14

        # Convert 'Week(day/End)' to numeric: Weekday=0, Weekend=1
        if 'Week(day/end)' in df_cleaned.columns:
            df_cleaned['Week(day/end)'] = df_cleaned['Week(day/end)'].map({'Weekday': 0, 'Weekend': 1})
            df_cleaned['Week(day/end)'] = df_cleaned['Week(day/end)'].fillna(0)

        # Create DayOfWeek numeric encoding if it doesn't exist
        if 'DayOfWeek' not in df_cleaned.columns:
            df_cleaned['DayOfWeek'] = np.random.randint(0, 7, len(df_cleaned))

        # Ensure all required columns exist with default values
        required_columns = ['Mood', 'Hour', 'Week(day/end)', 'SleepHours', 'Distractions', 
                          'ConfidenceScore', 'Completed', 'DayOfWeek']
        
        for col in required_columns:
            if col not in df_cleaned.columns:
                if col == 'Mood':
                    df_cleaned[col] = np.random.randint(1, 11, len(df_cleaned))
                elif col == 'SleepHours':
                    df_cleaned[col] = np.random.randint(5, 11, len(df_cleaned))
                elif col == 'Distractions':
                    df_cleaned[col] = np.random.randint(0, 6, len(df_cleaned))
                elif col == 'ConfidenceScore':
                    df_cleaned[col] = np.random.randint(1, 11, len(df_cleaned))
                elif col == 'Completed':
                    df_cleaned[col] = np.random.randint(0, 2, len(df_cleaned))
                else:
                    df_cleaned[col] = 0

        # Define features (inputs) and target (output)
        X = df_cleaned[required_columns]
        y = df_cleaned['TaskType']

        print(f"Features shape: {X.shape}")
        print(f"Target shape: {y.shape}")
        print(f"Target distribution: {y.value_counts()}")

        # Split data: 80% for training and 20% for testing
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        # Initialize the Random Forest Classifier
        model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)

        # Train the model on the training data
        model.fit(X_train, y_train)

        # Predict task types on the test set
        y_pred = model.predict(X_test)

        # Print overall accuracy of the model on test data
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.4f}")

        # Print detailed classification report
        print("Classification Report:")
        print(classification_report(y_test, y_pred))

        # Save the trained model
        os.makedirs('model', exist_ok=True)
        model_path = 'model/model.pkl'
        joblib.dump(model, model_path)
        print(f"Model saved to {model_path}")

        # Save the mapping for reference
        mapping_path = 'model/task_mapping.pkl'
        joblib.dump(mapping, mapping_path)
        print(f"Task mapping saved to {mapping_path}")

        return model, mapping

    except Exception as e:
        print(f"Error in training: {e}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    # Create sample data if the file doesn't exist
    data_path = "data/productivity_log_may.csv"
    if not os.path.exists(data_path):
        print("Creating sample data...")
        os.makedirs('data', exist_ok=True)
        
        # Create sample dataset
        np.random.seed(42)
        n_samples = 1000
        
        sample_data = {
            'Date': pd.date_range('2024-05-01', periods=n_samples, freq='H'),
            'TaskType': np.random.choice(['Study', 'Exercise', 'Social', 'Leisure', 'Sleep', 'Work'], n_samples),
            'Mood': np.random.randint(1, 11, n_samples),
            'SleepHours': np.random.randint(5, 11, n_samples),
            'Distractions': np.random.randint(0, 6, n_samples),
            'ConfidenceScore': np.random.randint(1, 11, n_samples),
            'Completed': np.random.randint(0, 2, n_samples),
            'Week(day/end)': np.random.choice(['Weekday', 'Weekend'], n_samples)
        }
        
        df = pd.DataFrame(sample_data)
        df.to_csv(data_path, index=False)
        print(f"Sample data created at {data_path}")
    
    model, mapping = train_tasktype_model(data_path)
    if model:
        print("Model training completed successfully!")
    else:
        print("Model training failed!")
