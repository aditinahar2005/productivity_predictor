import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

# Set style
plt.style.use('default')
sns.set_palette("husl")

# Define the task mapping - this is crucial!
TASK_MAPPING = {
    0: 'Study', 
    1: 'Exercise', 
    2: 'Social', 
    3: 'Leisure', 
    4: 'Sleep', 
    5: 'Work'
}

DAY_MAPPING = {
    0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'
}

def apply_mappings(df):
    """Apply task type and day mappings to dataframe"""
    df_plot = df.copy()
    
    # Map TaskType to meaningful names
    if 'TaskType' in df_plot.columns:
        if df_plot['TaskType'].dtype in ['int64', 'float64']:
            df_plot['TaskType'] = df_plot['TaskType'].map(TASK_MAPPING).fillna('Unknown')
    
    # Map DayOfWeek to day names
    if 'DayOfWeek' in df_plot.columns:
        if df_plot['DayOfWeek'].dtype in ['int64', 'float64']:
            df_plot['DayOfWeek'] = df_plot['DayOfWeek'].map(DAY_MAPPING).fillna('Unknown')
    
    return df_plot

def plot_scatter(df, x, y, save_path):
    """Create scatter plot"""
    try:
        plt.figure(figsize=(14, 10))
        
        # Apply mappings
        df_plot = apply_mappings(df)
        
        if 'TaskType' in df_plot.columns and x != 'TaskType' and y != 'TaskType':
            sns.scatterplot(data=df_plot, x=x, y=y, hue='TaskType', palette='viridis', s=80, alpha=0.7)
        else:
            sns.scatterplot(data=df_plot, x=x, y=y, s=80, alpha=0.7)
        
        plt.title(f'Scatter Plot: {y} vs {x}', fontsize=20, fontweight='bold')
        plt.xlabel(x, fontsize=16)
        plt.ylabel(y, fontsize=16)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        return save_path
    except Exception as e:
        plt.close()
        raise Exception(f"Error creating scatter plot: {str(e)}")

def plot_histogram(df, column, save_path):
    """Create histogram"""
    try:
        plt.figure(figsize=(14, 10))
        
        # Apply mappings
        df_plot = apply_mappings(df)
        
        if column == 'TaskType' or df_plot[column].dtype == 'object':
            # For categorical data, create a count plot
            value_counts = df_plot[column].value_counts()
            
            # Create a beautiful bar chart
            colors = plt.cm.viridis(np.linspace(0, 1, len(value_counts)))
            bars = plt.bar(range(len(value_counts)), value_counts.values, color=colors, alpha=0.8)
            
            # Set labels
            plt.xticks(range(len(value_counts)), value_counts.index, rotation=45, fontsize=14, ha='right')
            plt.title(f'Distribution of {column}', fontsize=20, fontweight='bold')
            plt.xlabel(column, fontsize=16)
            plt.ylabel('Count', fontsize=16)
            
            # Add value labels on bars
            for bar, value in zip(bars, value_counts.values):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(value_counts.values) * 0.01, 
                        str(value), ha='center', va='bottom', fontsize=12, fontweight='bold')
        else:
            # For numeric data, create histogram
            sns.histplot(df_plot[column], bins=20, kde=True, color='skyblue', alpha=0.7)
            plt.title(f'Distribution of {column}', fontsize=20, fontweight='bold')
            plt.xlabel(column, fontsize=16)
            plt.ylabel('Frequency', fontsize=16)
        
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        return save_path
    except Exception as e:
        plt.close()
        raise Exception(f"Error creating histogram: {str(e)}")

def plot_line(df, y, save_path):
    """Create line plot"""
    try:
        plt.figure(figsize=(16, 10))
        
        # Apply mappings
        df_plot = apply_mappings(df)
        
        if 'Date' in df_plot.columns:
            df_sorted = df_plot.sort_values("Date")
            df_sorted['Date'] = pd.to_datetime(df_sorted['Date'], errors='coerce')
            
            if 'TaskType' in df_plot.columns and y != 'TaskType':
                sns.lineplot(data=df_sorted, x='Date', y=y, hue='TaskType', marker='o', linewidth=2)
            else:
                sns.lineplot(data=df_sorted, x='Date', y=y, marker='o', linewidth=2)
        else:
            if 'TaskType' in df_plot.columns and y != 'TaskType':
                sns.lineplot(data=df_plot, x=df_plot.index, y=y, hue='TaskType', marker='o', linewidth=2)
            else:
                sns.lineplot(data=df_plot, x=df_plot.index, y=y, marker='o', linewidth=2)
        
        plt.title(f'Time Series: {y}', fontsize=20, fontweight='bold')
        plt.xlabel('Date' if 'Date' in df_plot.columns else 'Index', fontsize=16)
        plt.ylabel(y, fontsize=16)
        plt.xticks(rotation=45, fontsize=12)
        plt.yticks(fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        return save_path
    except Exception as e:
        plt.close()
        raise Exception(f"Error creating line plot: {str(e)}")

def plot_bar(df, x, y, save_path):
    """Create bar plot with intelligent handling"""
    try:
        plt.figure(figsize=(16, 10))
        
        # Apply mappings
        df_plot = apply_mappings(df)
        
        # Handle different combinations intelligently
        if df_plot[y].dtype in ['object', 'category'] or y == 'TaskType':
            # If y is categorical, create a count plot
            if x == y:
                # If x and y are the same, just show distribution
                value_counts = df_plot[x].value_counts()
                colors = plt.cm.viridis(np.linspace(0, 1, len(value_counts)))
                bars = plt.bar(range(len(value_counts)), value_counts.values, color=colors, alpha=0.8)
                plt.xticks(range(len(value_counts)), value_counts.index, rotation=45, fontsize=14, ha='right')
                plt.title(f'Distribution of {x}', fontsize=20, fontweight='bold')
                plt.ylabel('Count', fontsize=16)
                
                # Add value labels
                for bar, value in zip(bars, value_counts.values):
                    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(value_counts.values) * 0.01, 
                            str(value), ha='center', va='bottom', fontsize=12, fontweight='bold')
            else:
                # Cross tabulation for two categorical variables
                cross_tab = pd.crosstab(df_plot[x], df_plot[y])
                cross_tab.plot(kind='bar', stacked=False, colormap='viridis', figsize=(16, 10), alpha=0.8)
                plt.title(f'Count of {y} by {x}', fontsize=20, fontweight='bold')
                plt.ylabel('Count', fontsize=16)
                plt.legend(title=y, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
        else:
            # If y is numeric, calculate mean
            avg_data = df_plot.groupby(x)[y].mean().reset_index()
            
            # Create bar plot
            bars = plt.bar(avg_data[x], avg_data[y], color=plt.cm.viridis(np.linspace(0, 1, len(avg_data))), alpha=0.8)
            
            plt.title(f'Average {y} by {x}', fontsize=20, fontweight='bold')
            plt.ylabel(f'Average {y}', fontsize=16)
            
            # Add value labels on bars
            for bar, value in zip(bars, avg_data[y]):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(avg_data[y]) * 0.01, 
                        f'{value:.2f}', ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        plt.xlabel(x, fontsize=16)
        plt.xticks(rotation=45, fontsize=12, ha='right')
        plt.yticks(fontsize=12)
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        return save_path
    except Exception as e:
        plt.close()
        raise Exception(f"Error creating bar plot: {str(e)}")

def plot_heatmap(df, save_path):
    """Create correlation heatmap"""
    try:
        plt.figure(figsize=(16, 14))
        
        # Select only numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            raise Exception("Not enough numeric columns for correlation heatmap")
        
        numeric_data = df[numeric_cols]
        numeric_data = numeric_data.loc[:, numeric_data.var() != 0]
        
        if numeric_data.shape[1] < 2:
            raise Exception("Not enough varying numeric columns for correlation")
        
        corr = numeric_data.corr()
        
        # Create heatmap with better formatting
        mask = np.triu(np.ones_like(corr, dtype=bool))  # Mask upper triangle
        sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap='coolwarm', square=True,
                   linewidths=0.5, cbar_kws={"shrink": .8}, center=0, 
                   annot_kws={'fontsize': 12})
        
        plt.title('Correlation Heatmap (Lower Triangle)', fontsize=20, fontweight='bold')
        plt.xticks(fontsize=12, rotation=45)
        plt.yticks(fontsize=12)
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        return save_path
    except Exception as e:
        plt.close()
        raise Exception(f"Error creating heatmap: {str(e)}")

