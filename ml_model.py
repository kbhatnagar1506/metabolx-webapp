import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
import joblib
import os
import json

class HealthAnalysisModel:
    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(__file__), 'models')
        os.makedirs(self.model_path, exist_ok=True)
        
        self.classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.regressor = MultiOutputRegressor(GradientBoostingRegressor(random_state=42))
        self.scaler = StandardScaler()
        self.is_trained = False
        
        # Define base features
        self.base_features = [
            'age', 'gender', 'bmi', 'glucose', 'cholesterol', 'triglycerides',
            'hdl', 'ldl', 'alt', 'ast', 'bilirubin', 'alkaline_phosphatase',
            'creatinine', 'bun', 'sodium', 'potassium', 'chloride', 'bicarbonate',
            'calcium', 'magnesium', 'phosphate', 'total_protein', 'albumin',
            'globulin', 'ag_ratio'
        ]
        
        # Define advanced features
        self.advanced_features = [
            'insulin_resistance_index',
            'metabolic_syndrome_score',
            'inflammation_index',
            'oxidative_stress_score',
            'hormone_balance_index',
            'cardiovascular_risk_index',
            'liver_health_index',
            'kidney_function_index',
            'metabolic_efficiency_score',
            'immune_system_score',
            'endocrine_balance_score',
            'digestive_health_score',
            'bone_health_index',
            'muscle_mass_index',
            'vascular_health_score'
        ]
        
        # Define system-specific scores
        self.system_scores = {
            'liver': ['alt', 'ast', 'bilirubin', 'alkaline_phosphatase', 'albumin'],
            'kidney': ['creatinine', 'bun', 'sodium', 'potassium', 'chloride'],
            'cardio': ['cholesterol', 'triglycerides', 'hdl', 'ldl', 'glucose'],
            'endocrine': ['glucose', 'calcium', 'magnesium', 'phosphate'],
            'immune': ['total_protein', 'albumin', 'globulin', 'ag_ratio'],
            'digestive': ['albumin', 'total_protein', 'bilirubin', 'alkaline_phosphatase']
        }
        
        # Combined feature columns
        self.feature_columns = self.base_features + self.advanced_features
        
        # Define target columns for regression
        self.regression_targets = [
            'health_score',
            'metabolite_score',
            'comprehensive_score',
            'liver_score',
            'kidney_score',
            'cardio_score',
            'endocrine_score',
            'immune_score',
            'digestive_score'
        ]
        
        # Load or train models
        self.load_or_train_models()

    def generate_training_data(self, n_samples=1000):
        """Generate synthetic training data with realistic medical values."""
        np.random.seed(42)
        
        # Generate base features
        data = {
            'age': np.random.normal(45, 15, n_samples).clip(18, 90),
            'gender': np.random.choice([0, 1], n_samples),
            'bmi': np.random.normal(25, 5, n_samples).clip(15, 40),
            'glucose': np.random.normal(95, 15, n_samples).clip(60, 200),
            'cholesterol': np.random.normal(180, 30, n_samples).clip(100, 300),
            'triglycerides': np.random.normal(150, 50, n_samples).clip(50, 400),
            'hdl': np.random.normal(50, 10, n_samples).clip(30, 100),
            'ldl': np.random.normal(100, 25, n_samples).clip(50, 200),
            'alt': np.random.normal(25, 10, n_samples).clip(5, 100),
            'ast': np.random.normal(25, 8, n_samples).clip(5, 80),
            'bilirubin': np.random.normal(0.8, 0.3, n_samples).clip(0.2, 2.0),
            'alkaline_phosphatase': np.random.normal(70, 20, n_samples).clip(30, 150),
            'creatinine': np.random.normal(0.9, 0.3, n_samples).clip(0.5, 2.0),
            'bun': np.random.normal(15, 5, n_samples).clip(5, 40),
            'sodium': np.random.normal(140, 3, n_samples).clip(130, 150),
            'potassium': np.random.normal(4.0, 0.5, n_samples).clip(3.0, 5.5),
            'chloride': np.random.normal(102, 3, n_samples).clip(95, 110),
            'bicarbonate': np.random.normal(24, 2, n_samples).clip(20, 30),
            'calcium': np.random.normal(9.5, 0.5, n_samples).clip(8.0, 11.0),
            'magnesium': np.random.normal(2.0, 0.2, n_samples).clip(1.5, 2.5),
            'phosphate': np.random.normal(3.5, 0.5, n_samples).clip(2.5, 5.0),
            'total_protein': np.random.normal(7.0, 0.5, n_samples).clip(6.0, 8.5),
            'albumin': np.random.normal(4.0, 0.3, n_samples).clip(3.0, 5.0),
            'globulin': np.random.normal(3.0, 0.4, n_samples).clip(2.0, 4.0),
            'ag_ratio': np.random.normal(1.5, 0.2, n_samples).clip(1.0, 2.0),
            # New biomarkers
            'crp': np.random.normal(2.0, 2.0, n_samples).clip(0.1, 10.0),  # C-reactive protein
            'esr': np.random.normal(15, 10, n_samples).clip(0, 50),  # Erythrocyte sedimentation rate
            'fibrinogen': np.random.normal(300, 50, n_samples).clip(200, 500),  # Fibrinogen
            'malondialdehyde': np.random.normal(1.0, 0.5, n_samples).clip(0.1, 3.0),  # Lipid peroxidation marker
            '8_ohdg': np.random.normal(2.0, 1.0, n_samples).clip(0.1, 5.0),  # DNA damage marker
            'testosterone': np.random.normal(600, 200, n_samples).clip(200, 1200),  # Testosterone
            'estradiol': np.random.normal(50, 20, n_samples).clip(10, 100),  # Estradiol
            'cortisol': np.random.normal(15, 5, n_samples).clip(5, 30)  # Cortisol
        }
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Calculate advanced features
        advanced_features = self.calculate_advanced_features(df)
        for key, value in advanced_features.items():
            df[key] = value
        
        # Generate target variables
        df['health_status'] = np.random.choice(['healthy', 'at_risk', 'unhealthy'], n_samples, p=[0.6, 0.3, 0.1])
        
        # Generate regression targets
        df['predicted_glucose'] = df['glucose'] + np.random.normal(0, 5, n_samples)
        df['predicted_cholesterol'] = df['cholesterol'] + np.random.normal(0, 10, n_samples)
        df['predicted_bmi'] = df['bmi'] + np.random.normal(0, 1, n_samples)
        
        return df

    def load_or_train_models(self):
        """Load existing models or train new ones"""
        try:
            # Generate synthetic training data
            print("Generating synthetic training data...")
            synthetic_data = self.generate_training_data(n_samples=1000)
            
            # Load real data if available
            print("Loading real health data...")
            from real_data_loader import RealDataLoader
            loader = RealDataLoader()
            real_data = loader.load_health_data()
            
            if real_data is not None:
                print("Combining synthetic and real data...")
                # Calculate advanced features for real data
                real_data = pd.DataFrame(real_data)
                real_data = self.calculate_advanced_features(real_data)
                
                # Generate target variables for real data
                real_data = self.generate_target_variables(real_data)
                
                # Combine datasets
                training_data = pd.concat([synthetic_data, real_data], ignore_index=True)
                print(f"Total training samples: {len(training_data)}")
            else:
                print("Using synthetic data only...")
                training_data = synthetic_data
            
            # Handle missing values
            print("Handling missing values...")
            for col in training_data.columns:
                if training_data[col].dtype in ['float64', 'int64']:
                    # Fill numeric columns with median
                    training_data[col] = training_data[col].fillna(training_data[col].median())
                else:
                    # Fill categorical columns with mode
                    training_data[col] = training_data[col].fillna(training_data[col].mode()[0])
            
            # Split features and targets
            X = training_data[self.feature_columns]
            y_health = (training_data['health_score'] >= 70).astype(int)  # Binary classification
            y_regression = training_data[self.regression_targets]
            
            # Scale features
            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(X)
            
            # Train classifier
            print("Training classifier...")
            self.classifier.fit(X_scaled, y_health)
            
            # Train regressor
            print("Training regressor...")
            self.regressor.fit(X_scaled, y_regression)
            
            print("Model training completed successfully!")
            
            # Save training data statistics
            stats = {
                'total_samples': len(training_data),
                'synthetic_samples': len(synthetic_data),
                'real_samples': len(real_data) if real_data is not None else 0,
                'feature_importance': self.get_feature_importance().to_dict()
            }
            
            with open('training_stats.json', 'w') as f:
                json.dump(stats, f, indent=2)
            
        except Exception as e:
            print(f"Error in model training: {str(e)}")
            raise

    def generate_target_variables(self, data):
        """Generate target variables for the dataset"""
        if isinstance(data, dict):
            data = pd.DataFrame(data)
        
        # Ensure all required columns are present
        required_columns = [
            'glucose', 'cholesterol', 'hdl', 'bmi', 'total_protein',
            'triglycerides', 'liver_health_index', 'kidney_function_index',
            'cardiovascular_risk_index', 'metabolic_efficiency_score',
            'inflammation_index'
        ]
        
        for col in required_columns:
            if col not in data.columns:
                if col == 'glucose':
                    data[col] = 90  # Default normal glucose level
                elif col == 'cholesterol':
                    data[col] = 180  # Default normal cholesterol level
                elif col == 'hdl':
                    data[col] = 50  # Default normal HDL level
                elif col == 'bmi':
                    data[col] = 25  # Default normal BMI
                elif col == 'total_protein':
                    data[col] = 7.0  # Default normal total protein level
                elif col == 'triglycerides':
                    data[col] = 150  # Default normal triglycerides level
                elif col == 'liver_health_index':
                    data[col] = 70  # Default normal liver health index
                elif col == 'kidney_function_index':
                    data[col] = 70  # Default normal kidney function index
                elif col == 'cardiovascular_risk_index':
                    data[col] = 30  # Default low cardiovascular risk
                elif col == 'metabolic_efficiency_score':
                    data[col] = 70  # Default good metabolic efficiency
                elif col == 'inflammation_index':
                    data[col] = 30  # Default low inflammation
        
        # Calculate health scores
        health_scores = []
        metabolite_scores = []
        comprehensive_scores = []
        system_scores = []
        
        for _, row in data.iterrows():
            # Calculate base health score
            base_health = (
                (100 - abs(row['glucose'] - 90) / 2) * 0.2 +
                (100 - row['cholesterol'] / 200 * 100) * 0.2 +
                (row['hdl'] / 60 * 100) * 0.2 +
                (100 - row['bmi'] / 30 * 100) * 0.2 +
                (100 - abs(row['total_protein'] - 7.0) * 20) * 0.2
            ).clip(0, 100)
            
            # Add influence from advanced features
            health_score = (
                base_health * 0.6 +
                (100 - row['cardiovascular_risk_index']) * 0.1 +
                row['liver_health_index'] * 0.1 +
                row['kidney_function_index'] * 0.1 +
                row['metabolic_efficiency_score'] * 0.1
            ).clip(0, 100)
            
            # Calculate metabolite score
            metabolite_score = (
                (100 - abs(row['glucose'] - 90)) * 0.2 +
                (100 - row['cholesterol'] / 200 * 100) * 0.2 +
                (row['hdl'] / 60 * 100) * 0.2 +
                (100 - row['triglycerides'] / 150 * 100) * 0.2 +
                (100 - abs(row['total_protein'] - 7.0) * 20) * 0.2
            ).clip(0, 100)
            
            # Calculate comprehensive score
            comprehensive_score = (
                health_score * 0.4 +
                metabolite_score * 0.3 +
                row['metabolic_efficiency_score'] * 0.3
            ).clip(0, 100)
            
            # Calculate system-specific scores
            liver_score = row['liver_health_index']
            kidney_score = row['kidney_function_index']
            cardio_score = 100 - row['cardiovascular_risk_index']
            endocrine_score = (
                (100 - abs(row['glucose'] - 90)) * 0.4 +
                row['metabolic_efficiency_score'] * 0.6
            ).clip(0, 100)
            immune_score = (
                (100 - row['inflammation_index']) * 0.5 +
                (row['total_protein'] / 7.0 * 100) * 0.5
            ).clip(0, 100)
            digestive_score = (
                row['liver_health_index'] * 0.3 +
                (100 - abs(row['total_protein'] - 7.0) * 20) * 0.4 +
                (100 - row['inflammation_index']) * 0.3
            ).clip(0, 100)
            
            health_scores.append(health_score)
            metabolite_scores.append(metabolite_score)
            comprehensive_scores.append(comprehensive_score)
            system_scores.append([
                liver_score, kidney_score, cardio_score,
                endocrine_score, immune_score, digestive_score
            ])
        
        # Add scores to dataframe
        data['health_score'] = health_scores
        data['metabolite_score'] = metabolite_scores
        data['comprehensive_score'] = comprehensive_scores
        system_scores = np.array(system_scores)
        data['liver_score'] = system_scores[:, 0]
        data['kidney_score'] = system_scores[:, 1]
        data['cardio_score'] = system_scores[:, 2]
        data['endocrine_score'] = system_scores[:, 3]
        data['immune_score'] = system_scores[:, 4]
        data['digestive_score'] = system_scores[:, 5]
        
        return data

    def generate_synthetic_data(self, n_samples=1000):
        """Generate synthetic but realistic medical data"""
        np.random.seed(42)
        data = {}
        
        # Generate age (18-90 years)
        data['age'] = np.random.normal(45, 15, n_samples).clip(18, 90)
        
        # Generate gender (0: Female, 1: Male)
        data['gender_encoded'] = np.random.binomial(1, 0.5, n_samples)
        
        # Generate BMI (18.5-35)
        data['bmi'] = np.random.normal(25, 4, n_samples).clip(18.5, 35)
        
        # Generate glucose levels (70-200 mg/dL)
        data['glucose'] = np.random.normal(100, 25, n_samples).clip(70, 200)
        
        # Generate cholesterol (150-300 mg/dL)
        data['cholesterol'] = np.random.normal(200, 30, n_samples).clip(150, 300)
        
        # Generate triglycerides (50-300 mg/dL)
        data['triglycerides'] = np.random.normal(150, 50, n_samples).clip(50, 300)
        
        # Generate HDL (30-90 mg/dL)
        data['hdl'] = np.random.normal(50, 10, n_samples).clip(30, 90)
        
        # Generate LDL (70-200 mg/dL)
        data['ldl'] = np.random.normal(130, 25, n_samples).clip(70, 200)
        
        # Generate liver function tests
        data['alt'] = np.random.normal(30, 10, n_samples).clip(10, 100)
        data['ast'] = np.random.normal(25, 8, n_samples).clip(10, 80)
        
        # Generate kidney function tests
        data['creatinine'] = np.random.normal(1.0, 0.3, n_samples).clip(0.5, 2.0)
        data['bun'] = np.random.normal(15, 5, n_samples).clip(7, 30)
        
        # Generate electrolytes
        data['sodium'] = np.random.normal(140, 3, n_samples).clip(135, 145)
        data['potassium'] = np.random.normal(4.0, 0.4, n_samples).clip(3.5, 5.0)
        data['chloride'] = np.random.normal(102, 3, n_samples).clip(96, 106)
        data['bicarbonate'] = np.random.normal(24, 2, n_samples).clip(22, 29)
        
        # Generate minerals
        data['calcium'] = np.random.normal(9.5, 0.5, n_samples).clip(8.5, 10.5)
        data['magnesium'] = np.random.normal(2.0, 0.3, n_samples).clip(1.7, 2.4)
        data['phosphate'] = np.random.normal(3.5, 0.5, n_samples).clip(2.5, 4.5)
        
        # Generate proteins
        data['protein'] = np.random.normal(7.0, 0.5, n_samples).clip(6.0, 8.0)
        data['albumin'] = np.random.normal(4.3, 0.3, n_samples).clip(3.5, 5.0)
        data['globulin'] = np.random.normal(2.7, 0.3, n_samples).clip(2.0, 3.5)
        data['a_g_ratio'] = data['albumin'] / data['globulin']
        
        # Generate other liver function tests
        data['bilirubin'] = np.random.normal(0.8, 0.3, n_samples).clip(0.3, 1.5)
        data['alkaline_phosphatase'] = np.random.normal(80, 20, n_samples).clip(40, 120)
        
        # Generate health scores based on the biomarkers
        df = pd.DataFrame(data)
        
        # Calculate health scores using realistic formulas
        health_scores = self.calculate_health_scores(df)
        df = pd.concat([df, health_scores], axis=1)
        
        return df

    def calculate_health_scores(self, df):
        """Calculate realistic health scores based on biomarkers"""
        scores = pd.DataFrame()
        
        # Overall health score
        scores['health_score'] = 100 - (
            (df['glucose'] - 90).abs() / 2 +
            (df['cholesterol'] - 180).abs() / 4 +
            (df['bmi'] - 22).abs() * 2
        ).clip(0, 100)
        
        # Metabolite score
        scores['metabolite_score'] = 100 - (
            (df['glucose'] - 90).abs() / 2 +
            (df['triglycerides'] - 150).abs() / 4 +
            (df['hdl'] - 60).abs()
        ).clip(0, 100)
        
        # Comprehensive score
        scores['comprehensive_score'] = (
            scores['health_score'] * 0.4 +
            scores['metabolite_score'] * 0.6
        )
        
        # System-specific scores
        scores['liver_score'] = 100 - (
            (df['alt'] - 25).abs() / 2 +
            (df['ast'] - 25).abs() / 2 +
            (df['bilirubin'] - 0.8).abs() * 10
        ).clip(0, 100)
        
        scores['kidney_score'] = 100 - (
            (df['creatinine'] - 1.0).abs() * 20 +
            (df['bun'] - 15).abs()
        ).clip(0, 100)
        
        scores['cardio_score'] = 100 - (
            (df['cholesterol'] - 180).abs() / 4 +
            (df['hdl'] - 60).abs() +
            (df['ldl'] - 100).abs() / 2
        ).clip(0, 100)
        
        scores['endocrine_score'] = 100 - (
            (df['glucose'] - 90).abs() / 2 +
            (df['calcium'] - 9.5).abs() * 10
        ).clip(0, 100)
        
        scores['immune_score'] = 100 - (
            (df['protein'] - 7.0).abs() * 10 +
            (df['globulin'] - 2.7).abs() * 20
        ).clip(0, 100)
        
        scores['digestive_score'] = 100 - (
            (df['albumin'] - 4.3).abs() * 20 +
            (df['alkaline_phosphatase'] - 80).abs() / 4
        ).clip(0, 100)
        
        return scores

    def calculate_advanced_features(self, data):
        """Calculate advanced health metrics and indices."""
        features = {}
        
        # Insulin Resistance Index
        features['insulin_resistance_index'] = (data['glucose'] * data['triglycerides'] / (data['hdl'] + 1)).clip(0, 100)
        
        # Metabolic Syndrome Score
        features['metabolic_syndrome_score'] = (
            (data['bmi'] > 30).astype(int) +
            (data['glucose'] > 100).astype(int) +
            (data['triglycerides'] > 150).astype(int) +
            (data['hdl'] < 40).astype(int)
        ) * 25
        
        # Inflammation Index
        features['inflammation_index'] = (
            (data['crp'] / 10) +  # C-reactive protein
            (data['esr'] / 20) +  # Erythrocyte sedimentation rate
            (data['fibrinogen'] / 400)  # Fibrinogen
        ).clip(0, 100)
        
        # Oxidative Stress Score
        features['oxidative_stress_score'] = (
            (data['malondialdehyde'] / 2) +  # Lipid peroxidation marker
            (data['8_ohdg'] / 5)  # DNA damage marker
        ).clip(0, 100)
        
        # Hormone Balance Index
        features['hormone_balance_index'] = (
            (data['testosterone'] / 800) +  # Testosterone
            (data['estradiol'] / 100) +     # Estradiol
            (data['cortisol'] / 20)         # Cortisol
        ).clip(0, 100)
        
        # Cardiovascular Risk Index
        features['cardiovascular_risk_index'] = (
            (data['cholesterol'] / 200) +
            (data['triglycerides'] / 150) +
            (data['ldl'] / 100) +
            (data['hdl'] / 40)
        ).clip(0, 100)
        
        # Liver Health Index
        features['liver_health_index'] = (
            (data['alt'] / 40) +
            (data['ast'] / 40) +
            (data['bilirubin'] / 1.2) +
            (data['alkaline_phosphatase'] / 120)
        ).clip(0, 100)
        
        # Kidney Function Index
        features['kidney_function_index'] = (
            (data['creatinine'] / 1.2) +
            (data['bun'] / 20) +
            (data['sodium'] / 140) +
            (data['potassium'] / 4.0)
        ).clip(0, 100)
        
        # Metabolic Efficiency Score
        features['metabolic_efficiency_score'] = (
            (data['glucose'] / 100) +
            (data['triglycerides'] / 150) +
            (data['hdl'] / 40)
        ).clip(0, 100)
        
        # Immune System Score
        features['immune_system_score'] = (
            (data['total_protein'] / 7.0) +
            (data['albumin'] / 4.0) +
            (data['globulin'] / 3.0) +
            (data['ag_ratio'] / 1.5)
        ).clip(0, 100)
        
        # Endocrine Balance Score
        features['endocrine_balance_score'] = (
            (data['glucose'] / 100) +
            (data['calcium'] / 10) +
            (data['magnesium'] / 2.0) +
            (data['phosphate'] / 3.5)
        ).clip(0, 100)
        
        # Digestive Health Score
        features['digestive_health_score'] = (
            (data['albumin'] / 4.0) +
            (data['total_protein'] / 7.0) +
            (data['bilirubin'] / 1.2) +
            (data['alkaline_phosphatase'] / 120)
        ).clip(0, 100)
        
        # Bone Health Index
        features['bone_health_index'] = (
            (data['calcium'] / 10) +
            (data['magnesium'] / 2.0) +
            (data['phosphate'] / 3.5) +
            (data['alkaline_phosphatase'] / 120)
        ).clip(0, 100)
        
        # Muscle Mass Index
        features['muscle_mass_index'] = (
            (data['creatinine'] / 1.2) +
            (data['total_protein'] / 7.0) +
            (data['albumin'] / 4.0)
        ).clip(0, 100)
        
        # Vascular Health Score
        features['vascular_health_score'] = (
            (data['cholesterol'] / 200) +
            (data['triglycerides'] / 150) +
            (data['hdl'] / 40) +
            (data['ldl'] / 100)
        ).clip(0, 100)
        
        return features

    def calculate_system_scores(self, data):
        """Calculate health scores for different body systems."""
        scores = {}
        
        for system, markers in self.system_scores.items():
            # Calculate weighted average of markers
            weights = {
                'liver': {'alt': 0.3, 'ast': 0.3, 'bilirubin': 0.2, 'alkaline_phosphatase': 0.2},
                'kidney': {'creatinine': 0.3, 'bun': 0.2, 'sodium': 0.2, 'potassium': 0.15, 'chloride': 0.15},
                'cardio': {'cholesterol': 0.25, 'triglycerides': 0.25, 'hdl': 0.2, 'ldl': 0.2, 'glucose': 0.1},
                'endocrine': {'glucose': 0.4, 'calcium': 0.2, 'magnesium': 0.2, 'phosphate': 0.2},
                'immune': {'total_protein': 0.3, 'albumin': 0.3, 'globulin': 0.2, 'ag_ratio': 0.2},
                'digestive': {'albumin': 0.3, 'total_protein': 0.3, 'bilirubin': 0.2, 'alkaline_phosphatase': 0.2}
            }
            
            score = 0
            for marker in markers:
                if marker in data and marker in weights[system]:
                    normalized_value = self.normalize_marker(marker, data[marker])
                    score += normalized_value * weights[system][marker]
            
            scores[system] = score * 100
        
        return scores

    def normalize_marker(self, marker, value):
        """Normalize a biomarker value to a 0-1 scale based on reference ranges."""
        reference_ranges = {
            'glucose': (70, 100),
            'cholesterol': (125, 200),
            'triglycerides': (0, 150),
            'hdl': (40, 60),
            'ldl': (0, 100),
            'alt': (7, 56),
            'ast': (10, 40),
            'bilirubin': (0.3, 1.2),
            'alkaline_phosphatase': (44, 147),
            'creatinine': (0.6, 1.2),
            'bun': (7, 20),
            'sodium': (135, 145),
            'potassium': (3.5, 5.0),
            'chloride': (96, 106),
            'bicarbonate': (23, 29),
            'calcium': (8.5, 10.5),
            'magnesium': (1.7, 2.3),
            'phosphate': (2.5, 4.5),
            'total_protein': (6.0, 8.0),
            'albumin': (3.5, 5.0),
            'globulin': (2.0, 3.5),
            'ag_ratio': (1.1, 2.5)
        }
        
        if marker in reference_ranges:
            min_val, max_val = reference_ranges[marker]
            return max(0, min(1, (value - min_val) / (max_val - min_val)))
        return 0.5  # Default to middle value if no reference range

    def analyze_health(self, data):
        """Perform comprehensive health analysis."""
        # Calculate advanced features
        advanced_features = self.calculate_advanced_features(data)
        
        # Calculate system scores
        system_scores = self.calculate_system_scores(data)
        
        # Calculate base health score
        base_health = (
            (100 - abs(data['glucose'] - 90) / 2) * 0.2 +
            (100 - data['cholesterol'] / 200 * 100) * 0.2 +
            (data['hdl'] / 60 * 100) * 0.2 +
            (100 - data['bmi'] / 30 * 100) * 0.2 +
            (100 - abs(data['total_protein'] - 7.0) * 20) * 0.2
        ).clip(0, 100)
        
        # Calculate comprehensive score
        comprehensive_score = (
            base_health * 0.3 +
            np.mean(list(advanced_features.values())) * 0.4 +
            np.mean(list(system_scores.values())) * 0.3
        ).clip(0, 100)
        
        # Calculate metabolite score
        metabolite_score = (
            (100 - abs(data['glucose'] - 90) / 2) * 0.25 +
            (100 - data['cholesterol'] / 200 * 100) * 0.25 +
            (data['hdl'] / 60 * 100) * 0.25 +
            (100 - data['triglycerides'] / 150 * 100) * 0.25
        ).clip(0, 100)
        
        # Generate health insights
        insights = self.generate_health_insights(data, advanced_features, system_scores)
        
        # Generate recommendations
        recommendations = self.generate_recommendations(data, advanced_features, system_scores)
        
        return {
            'healthScore': base_health,
            'metaboliteScore': metabolite_score,
            'comprehensiveScore': comprehensive_score,
            'advancedFeatures': advanced_features,
            'systemScores': system_scores,
            'insights': insights,
            'recommendations': recommendations
        }

    def generate_health_insights(self, data, advanced_features, system_scores):
        """Generate detailed health insights based on analysis."""
        insights = []
        
        # Analyze metabolic health
        if advanced_features['metabolic_syndrome_score'] > 50:
            insights.append("High risk of metabolic syndrome detected")
        elif advanced_features['metabolic_syndrome_score'] > 25:
            insights.append("Moderate risk of metabolic syndrome")
        
        # Analyze cardiovascular health
        if advanced_features['cardiovascular_risk_index'] > 70:
            insights.append("High cardiovascular risk detected")
        elif advanced_features['cardiovascular_risk_index'] > 50:
            insights.append("Moderate cardiovascular risk")
        
        # Analyze liver health
        if advanced_features['liver_health_index'] < 30:
            insights.append("Significant liver function impairment")
        elif advanced_features['liver_health_index'] < 50:
            insights.append("Mild liver function impairment")
        
        # Analyze kidney health
        if advanced_features['kidney_function_index'] < 30:
            insights.append("Significant kidney function impairment")
        elif advanced_features['kidney_function_index'] < 50:
            insights.append("Mild kidney function impairment")
        
        # Analyze immune system
        if advanced_features['immune_system_score'] < 30:
            insights.append("Weakened immune system detected")
        elif advanced_features['immune_system_score'] < 50:
            insights.append("Moderate immune system function")
        
        # Analyze endocrine balance
        if advanced_features['hormone_balance_index'] < 30:
            insights.append("Significant hormonal imbalance detected")
        elif advanced_features['hormone_balance_index'] < 50:
            insights.append("Mild hormonal imbalance")
        
        # Analyze oxidative stress
        if advanced_features['oxidative_stress_score'] > 70:
            insights.append("High oxidative stress levels detected")
        elif advanced_features['oxidative_stress_score'] > 50:
            insights.append("Moderate oxidative stress levels")
        
        return insights

    def generate_recommendations(self, data, advanced_features, system_scores):
        """Generate personalized health recommendations."""
        recommendations = {
            'lifestyle': [],
            'diet': [],
            'supplements': [],
            'monitoring': []
        }
        
        # Lifestyle recommendations based on scores
        if advanced_features['metabolic_syndrome_score'] > 25:
            recommendations['lifestyle'].append("Increase physical activity to at least 150 minutes per week")
            recommendations['lifestyle'].append("Implement stress management techniques")
        
        if advanced_features['cardiovascular_risk_index'] > 50:
            recommendations['lifestyle'].append("Regular cardiovascular exercise")
            recommendations['lifestyle'].append("Monitor blood pressure regularly")
        
        # Dietary recommendations
        if advanced_features['metabolic_efficiency_score'] < 50:
            recommendations['diet'].append("Reduce refined carbohydrate intake")
            recommendations['diet'].append("Increase fiber-rich foods")
        
        if advanced_features['liver_health_index'] < 50:
            recommendations['diet'].append("Reduce alcohol consumption")
            recommendations['diet'].append("Increase antioxidant-rich foods")
        
        # Supplement recommendations
        if advanced_features['oxidative_stress_score'] > 50:
            recommendations['supplements'].append("Consider antioxidant supplements")
            recommendations['supplements'].append("Vitamin C and E supplementation")
        
        if advanced_features['bone_health_index'] < 50:
            recommendations['supplements'].append("Calcium and Vitamin D supplementation")
            recommendations['supplements'].append("Magnesium supplementation")
        
        # Monitoring recommendations
        if advanced_features['kidney_function_index'] < 50:
            recommendations['monitoring'].append("Regular kidney function tests")
            recommendations['monitoring'].append("Monitor fluid intake")
        
        if advanced_features['endocrine_balance_score'] < 50:
            recommendations['monitoring'].append("Regular hormone level checks")
            recommendations['monitoring'].append("Monitor blood sugar levels")
        
        return recommendations

    def predict(self, patient_data):
        """Make predictions for a single patient"""
        # Prepare input data
        input_data = pd.DataFrame([patient_data])
        
        # Ensure all required features are present
        for col in self.feature_columns:
            if col not in input_data.columns:
                input_data[col] = 0  # Use default value
        
        # Scale features
        input_scaled = self.scaler.transform(input_data[self.feature_columns])
        
        # Make predictions
        health_risk = self.classifier.predict(input_scaled)[0]
        scores = self.regressor.predict(input_scaled)[0]
        
        # Prepare results
        results = {
            'health_risk': bool(health_risk),
            'health_score': scores[0],
            'metabolite_score': scores[1],
            'comprehensive_score': scores[2],
            'system_scores': {
                'liver': scores[3],
                'kidney': scores[4],
                'cardiovascular': scores[5],
                'endocrine': scores[6],
                'immune': scores[7],
                'digestive': scores[8]
            }
        }
        
        return results

    def predict_future_trends(self, current_data, prediction_weeks=12):
        """Predict future health trends based on current data"""
        try:
            # Prepare input data
            input_data = pd.DataFrame([current_data])
            input_data = self.calculate_advanced_features(input_data)
            
            # Scale features
            input_scaled = self.scaler.transform(input_data[self.feature_columns])
            
            # Get base predictions
            base_predictions = self.regressor.predict(input_scaled)[0]
            
            # Generate time series predictions
            future_trends = {
                'health_score': [],
                'metabolite_score': [],
                'risk_level': [],
                'biomarker_predictions': {}
            }
            
            # Simulate weekly changes based on current health indicators
            base_health = base_predictions[0]  # health_score
            base_metabolite = base_predictions[1]  # metabolite_score
            
            for week in range(prediction_weeks):
                # Calculate predicted changes based on current metrics
                health_change = self._calculate_weekly_change(base_health, input_data)
                metabolite_change = self._calculate_weekly_change(base_metabolite, input_data)
                
                # Update predictions
                base_health = max(0, min(100, base_health + health_change))
                base_metabolite = max(0, min(100, base_metabolite + metabolite_change))
                
                # Store predictions
                future_trends['health_score'].append(round(base_health, 1))
                future_trends['metabolite_score'].append(round(base_metabolite, 1))
                future_trends['risk_level'].append(
                    round(100 - ((base_health + base_metabolite) / 2), 1)
                )
            
            # Predict key biomarker trends
            biomarkers = ['glucose', 'cholesterol', 'triglycerides', 'hdl', 'ldl']
            for biomarker in biomarkers:
                if biomarker in input_data.columns:
                    base_value = input_data[biomarker].iloc[0]
                    future_trends['biomarker_predictions'][biomarker] = [
                        round(self._predict_biomarker_change(base_value, week, input_data), 1)
                        for week in range(prediction_weeks)
                    ]
            
            return future_trends
            
        except Exception as e:
            print(f"Error in future trend prediction: {str(e)}")
            return None

    def _calculate_weekly_change(self, base_value, patient_data):
        """Calculate predicted weekly changes based on health indicators"""
        # Implement sophisticated change calculation based on multiple factors
        metabolic_factor = (patient_data['metabolic_efficiency_score'].iloc[0] - 50) / 100
        risk_factor = (patient_data['cardiovascular_risk_index'].iloc[0] - 50) / 100
        health_factor = (patient_data['liver_health_index'].iloc[0] + 
                        patient_data['kidney_function_index'].iloc[0]) / 200
        
        # Calculate change with dampening factor
        max_weekly_change = 2.0  # Maximum 2% change per week
        change = (metabolic_factor + health_factor - risk_factor) * max_weekly_change
        
        # Add small random variation
        noise = np.random.normal(0, 0.2)
        
        return change + noise

    def _predict_biomarker_change(self, base_value, week, patient_data):
        """Predict changes in biomarker values over time"""
        # Calculate change factors based on patient metrics
        metabolic_health = patient_data['metabolic_efficiency_score'].iloc[0] / 100
        risk_level = patient_data['cardiovascular_risk_index'].iloc[0] / 100
        
        # Calculate target value based on normal ranges
        if 'glucose' in patient_data.columns:
            target = 90  # Ideal glucose level
        elif 'cholesterol' in patient_data.columns:
            target = 170  # Ideal cholesterol level
        else:
            target = base_value
        
        # Calculate weekly progression
        max_change = abs(target - base_value) * 0.1  # Maximum 10% movement toward target per week
        direction = 1 if target > base_value else -1
        
        change = max_change * (metabolic_health - risk_level) * direction
        
        # Add decay factor over time
        decay = np.exp(-0.1 * week)
        change *= decay
        
        # Add small random variation
        noise = np.random.normal(0, base_value * 0.01)  # 1% random variation
        
        return base_value + (change + noise)

    def get_feature_importance(self):
        """Get feature importance from both classifier and regressor"""
        importance_data = []
        
        # Get classifier feature importance
        if hasattr(self.classifier, 'feature_importances_'):
            clf_importance = pd.DataFrame({
                'feature': self.feature_columns,
                'importance': self.classifier.feature_importances_,
                'model': 'classifier'
            })
            importance_data.append(clf_importance)
        
        # Get regressor feature importance (for each target)
        if hasattr(self.regressor, 'estimators_'):
            for i, target in enumerate(self.regression_targets):
                reg_importance = pd.DataFrame({
                    'feature': self.feature_columns,
                    'importance': self.regressor.estimators_[i].feature_importances_,
                    'model': f'regressor_{target}'
                })
                importance_data.append(reg_importance)
        
        # Combine all importance data
        if importance_data:
            combined_importance = pd.concat(importance_data, ignore_index=True)
            return combined_importance.groupby('feature')['importance'].mean().sort_values(ascending=False)
        
        return pd.DataFrame() 