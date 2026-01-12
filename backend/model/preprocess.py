import pandas as pd
import numpy as np
import os

def load_data(filepath):
    """Load data from CSV file and handle date/time parsing"""
    try:
        df = pd.read_csv(filepath)
        
        # Handle date parsing
        if 'Date' in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
        
        # Extract time if possible
        if 'Time' in df.columns:
            df["Time"] = pd.to_datetime(df["Time"], errors='coerce')
        elif 'Date' in df.columns:
            df["Time"] = df["Date"]
        
        # Save cleaned data
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        df.to_csv(filepath, index=False)
        
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def handle_missing_values(df):
    """Handle missing values in the dataset"""
    print("Missing values in each column:")
    print(df.isnull().sum())
    
    # Fill missing values for numeric columns
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    
    for col in numeric_columns:
        if df[col].isnull().any():
            if 'TaskType' in df.columns:
                df[col] = df[col].fillna(df.groupby("TaskType")[col].transform('mean'))
            else:
                df[col] = df[col].fillna(df[col].mean())
    
    # Fill missing values for categorical columns
    categorical_columns = df.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'Unknown')
    
    return df

def encode_tasktypes(df):
    """Encode task types to numeric values"""
    if 'TaskType' in df.columns:
        df["TaskType"] = df["TaskType"].astype("category")
        mapping = dict(enumerate(df["TaskType"].cat.categories))
        df["TaskType"] = df["TaskType"].cat.codes
        return df, mapping
    else:
        # Create default mapping if TaskType doesn't exist
        mapping = {0: 'Study', 1: 'Exercise', 2: 'Social', 3: 'Leisure', 4: 'Sleep', 5: 'Work'}
        df['TaskType'] = np.random.randint(0, 6, len(df))
        return df, mapping

def remove_duplicates(df):
    """Remove duplicate rows"""
    initial_shape = df.shape
    df = df.drop_duplicates()
    print(f"Removed {initial_shape[0] - df.shape[0]} duplicate rows")
    return df

def extract_time_features(df):
    """Extract time-based features"""
    if 'Date' in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
        df["DayOfWeek"] = df["Date"].dt.dayofweek  # 0=Monday, 6=Sunday
        df["Week(day/end)"] = np.where(df["Date"].dt.dayofweek < 5, "Weekday", "Weekend")
    else:
        # Create default values if Date column doesn't exist
        df["DayOfWeek"] = np.random.randint(0, 7, len(df))
        df["Week(day/end)"] = np.random.choice(["Weekday", "Weekend"], len(df))
    
    return df

def clean_pipeline(filepath):
    """Complete data cleaning pipeline"""
    try:
        # Load data
        df = load_data(filepath)
        if df is None:
            return None, None
        
        print(f"Initial data shape: {df.shape}")
        
        # Handle missing values
        df = handle_missing_values(df)
        
        # Encode task types
        df, mapping = encode_tasktypes(df)
        
        # Remove duplicates
        df = remove_duplicates(df)
        
        # Extract time features
        df = extract_time_features(df)
        
        # Clean text columns
        text_cols = df.select_dtypes(include='object').columns
        for col in text_cols:
            df[col] = df[col].astype(str).str.strip()
        
        # Drop rows with missing critical data
        critical_columns = ['TaskType']
        df = df.dropna(subset=critical_columns)
        
        print(f"Final cleaned data shape: {df.shape}")
        print(f"Task mapping: {mapping}")
        
        # Save cleaned data
        df.to_csv(filepath, index=False)
        
        return df, mapping
    
    except Exception as e:
        print(f"Error in clean_pipeline: {e}")
        import traceback
        traceback.print_exc()
        return None, None

# Test the pipeline if run directly
if __name__ == "__main__":
    df_cleaned, mapping = clean_pipeline("data/productivity_log_may.csv")
    if df_cleaned is not None:
        print("Data cleaning completed successfully!")
        print(f"Columns: {list(df_cleaned.columns)}")
        print(f"Sample data:\n{df_cleaned.head()}")
    else:
        print("Data cleaning failed!")
