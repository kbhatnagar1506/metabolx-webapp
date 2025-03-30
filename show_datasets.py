import pandas as pd
import numpy as np
from ml_model import HealthAnalysisModel
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_datasets():
    print("Generating 1000 training datasets...")
    model = HealthAnalysisModel()
    data = model.generate_training_data(n_samples=1000)
    
    # Save full dataset to CSV
    data.to_csv('training_data.csv', index=False)
    print("\nFull dataset saved to training_data.csv")
    
    # Display basic statistics
    print("\nDataset Overview:")
    print(f"Number of samples: {len(data)}")
    print(f"Number of features: {len(data.columns)}")
    
    print("\nBasic Statistics:")
    stats = data.describe()
    print(stats)
    
    # Create visualizations
    print("\nGenerating visualizations...")
    
    # Set up the plotting style
    plt.style.use('default')
    sns.set_theme()
    
    # 1. Distribution of Health Scores
    plt.figure(figsize=(15, 5))
    plt.subplot(131)
    sns.histplot(data['health_score'], bins=30)
    plt.title('Distribution of Health Scores')
    plt.xlabel('Health Score')
    
    plt.subplot(132)
    sns.histplot(data['metabolite_score'], bins=30)
    plt.title('Distribution of Metabolite Scores')
    plt.xlabel('Metabolite Score')
    
    plt.subplot(133)
    sns.histplot(data['comprehensive_score'], bins=30)
    plt.title('Distribution of Comprehensive Scores')
    plt.xlabel('Comprehensive Score')
    
    plt.tight_layout()
    plt.savefig('score_distributions.png')
    plt.close()
    
    # 2. System-specific scores boxplot
    plt.figure(figsize=(12, 6))
    system_scores = data[['liver_score', 'kidney_score', 'cardio_score', 
                         'endocrine_score', 'immune_score', 'digestive_score']]
    sns.boxplot(data=system_scores)
    plt.xticks(rotation=45)
    plt.title('Distribution of System-Specific Scores')
    plt.tight_layout()
    plt.savefig('system_scores.png')
    plt.close()
    
    # 3. Correlation matrix of key metrics
    plt.figure(figsize=(12, 10))
    key_metrics = ['glucose', 'cholesterol', 'triglycerides', 'hdl', 'ldl', 
                  'health_score', 'metabolite_score', 'comprehensive_score']
    correlation = data[key_metrics].corr()
    sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Matrix of Key Metrics')
    plt.tight_layout()
    plt.savefig('correlation_matrix.png')
    plt.close()
    
    # Print summary statistics for advanced features
    print("\nAdvanced Feature Statistics:")
    advanced_features = [
        'insulin_resistance_index',
        'metabolic_syndrome_score',
        'inflammation_index',
        'oxidative_stress_score',
        'hormone_balance_index',
        'cardiovascular_risk_index',
        'liver_health_index',
        'kidney_function_index',
        'metabolic_efficiency_score'
    ]
    print(data[advanced_features].describe())
    
    # Save advanced features to a separate CSV
    data[advanced_features].to_csv('advanced_features.csv', index=False)
    
    print("\nVisualizations have been saved as:")
    print("1. score_distributions.png")
    print("2. system_scores.png")
    print("3. correlation_matrix.png")
    print("\nDetailed data has been saved to:")
    print("1. training_data.csv (complete dataset)")
    print("2. advanced_features.csv (advanced features only)")

if __name__ == "__main__":
    analyze_datasets() 