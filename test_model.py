import pandas as pd
import numpy as np
from ml_model import HealthAnalysisModel
import json
from pathlib import Path

def generate_test_patient():
    """Generate a test patient with realistic health metrics"""
    return {
        'age': np.random.normal(45, 15),
        'gender_encoded': np.random.binomial(1, 0.5),
        'bmi': np.random.normal(25, 4),
        'glucose': np.random.normal(95, 15),
        'cholesterol': np.random.normal(190, 30),
        'triglycerides': np.random.normal(150, 50),
        'hdl': np.random.normal(55, 15),
        'ldl': np.random.normal(120, 30),
        'alt': np.random.normal(30, 10),
        'ast': np.random.normal(25, 8),
        'creatinine': np.random.normal(1.0, 0.3),
        'bun': np.random.normal(15, 5),
        'sodium': np.random.normal(140, 3),
        'potassium': np.random.normal(4.0, 0.5),
        'chloride': np.random.normal(102, 3),
        'bicarbonate': np.random.normal(24, 2),
        'calcium': np.random.normal(9.5, 0.5),
        'magnesium': np.random.normal(2.0, 0.3),
        'phosphate': np.random.normal(3.5, 0.5),
        'protein': np.random.normal(7.0, 0.5),
        'albumin': np.random.normal(4.2, 0.4),
        'globulin': np.random.normal(2.8, 0.3),
        'a_g_ratio': np.random.normal(1.5, 0.3),
        'bilirubin': np.random.normal(0.8, 0.3),
        'alkaline_phosphatase': np.random.normal(80, 20)
    }

def main():
    # Initialize the model
    print("Initializing Health Analysis Model...")
    model = HealthAnalysisModel()
    
    # Generate test patient data
    print("\nGenerating test patient data...")
    test_patient = generate_test_patient()
    
    # Make predictions
    print("\nMaking predictions...")
    current_predictions = model.predict(test_patient)
    
    # Get future trends
    print("\nPredicting future trends...")
    future_trends = model.predict_future_trends(test_patient)
    
    # Combine results
    results = {
        'current_health_status': current_predictions,
        'future_trends': future_trends
    }
    
    # Save results
    print("\nSaving results...")
    output_dir = Path('test_results')
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / 'test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("\nTest Results Summary:")
    print(f"Current Health Risk: {current_predictions['health_risk']}")
    print(f"Health Score: {current_predictions['health_score']:.2f}")
    print(f"Metabolite Score: {current_predictions['metabolite_score']:.2f}")
    print("\nSystem Scores:")
    for system, score in current_predictions['system_scores'].items():
        print(f"{system.title()}: {score:.2f}")
    
    print("\nFuture Trends Summary:")
    print(f"Health Score (12 weeks): {future_trends['health_score'][-1]:.2f}")
    print(f"Risk Level (12 weeks): {future_trends['risk_level'][-1]:.2f}")
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    main() 