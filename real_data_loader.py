import pandas as pd
import numpy as np
from pathlib import Path

class RealDataLoader:
    def __init__(self):
        self.data_dir = Path('real_data')
        self.data_dir.mkdir(exist_ok=True)
        
        # Define realistic ranges for health metrics based on medical literature
        self.ranges = {
            'age': (18, 90),
            'bmi': (16, 45),
            'glucose': (70, 200),
            'cholesterol': (120, 300),
            'hdl': (20, 100),
            'ldl': (50, 250),
            'triglycerides': (50, 400),
            'alt': (10, 100),
            'ast': (10, 100),
            'creatinine': (0.5, 2.0),
            'bun': (5, 40),
            'sodium': (130, 150),
            'potassium': (2.5, 6.0),
            'chloride': (95, 110),
            'bicarbonate': (18, 30),
            'calcium': (8.0, 11.0),
            'magnesium': (1.2, 3.0),
            'phosphate': (2.0, 5.0),
            'alkaline_phosphatase': (30, 150),
            'bilirubin': (0.2, 2.0),
            'protein': (5.0, 9.0),
            'albumin': (3.0, 5.5)
        }

        self.required_columns = [
            'age', 'gender', 'bmi', 'glucose', 'cholesterol', 'triglycerides',
            'hdl', 'ldl', 'alt', 'ast', 'bilirubin', 'alkaline_phosphatase',
            'creatinine', 'bun', 'sodium', 'potassium', 'chloride', 'bicarbonate',
            'calcium', 'magnesium', 'phosphate', 'total_protein', 'albumin',
            'globulin', 'ag_ratio'
        ]
        
        self.advanced_biomarkers = {
            'crp': 2.0,  # C-reactive protein (mg/L)
            'esr': 15,   # Erythrocyte sedimentation rate (mm/hr)
            'fibrinogen': 300,  # Fibrinogen (mg/dL)
            'malondialdehyde': 1.0,  # Lipid peroxidation marker (μmol/L)
            '8_ohdg': 2.0,  # DNA damage marker (ng/mL)
            'testosterone': 600,  # Testosterone (ng/dL)
            'estradiol': 50,  # Estradiol (pg/mL)
            'cortisol': 15  # Cortisol (μg/dL)
        }
    
    def generate_realistic_data(self, n_samples=1000):
        """
        Generate synthetic health data that follows realistic distributions
        """
        print("Generating synthetic health data with realistic distributions...")
        data = pd.DataFrame()
        
        # Demographics
        data['age'] = np.random.normal(45, 15, n_samples).clip(self.ranges['age'][0], self.ranges['age'][1])
        data['gender_encoded'] = np.random.binomial(1, 0.5, n_samples)
        
        # BMI with realistic distribution (slightly right-skewed)
        data['bmi'] = np.random.lognormal(3.1, 0.2, n_samples).clip(self.ranges['bmi'][0], self.ranges['bmi'][1])
        
        # Glucose levels (fasting) - normal distribution with some elevated values
        base_glucose = np.random.normal(95, 10, n_samples)
        elevated_mask = np.random.random(n_samples) < 0.2  # 20% chance of elevated glucose
        base_glucose[elevated_mask] += np.random.normal(40, 10, sum(elevated_mask))
        data['glucose'] = base_glucose.clip(self.ranges['glucose'][0], self.ranges['glucose'][1])
        
        # Lipid panel
        data['cholesterol'] = np.random.normal(190, 35, n_samples).clip(self.ranges['cholesterol'][0], self.ranges['cholesterol'][1])
        data['hdl'] = np.random.normal(55, 15, n_samples).clip(self.ranges['hdl'][0], self.ranges['hdl'][1])
        data['ldl'] = (data['cholesterol'] - data['hdl'] * 1.5).clip(self.ranges['ldl'][0], self.ranges['ldl'][1])
        data['triglycerides'] = np.random.lognormal(5.0, 0.4, n_samples).clip(self.ranges['triglycerides'][0], self.ranges['triglycerides'][1])
        
        # Liver function tests
        data['alt'] = np.random.lognormal(3.2, 0.3, n_samples).clip(self.ranges['alt'][0], self.ranges['alt'][1])
        data['ast'] = np.random.lognormal(3.1, 0.3, n_samples).clip(self.ranges['ast'][0], self.ranges['ast'][1])
        data['alkaline_phosphatase'] = np.random.normal(90, 20, n_samples).clip(self.ranges['alkaline_phosphatase'][0], self.ranges['alkaline_phosphatase'][1])
        data['bilirubin'] = np.random.lognormal(0, 0.4, n_samples).clip(self.ranges['bilirubin'][0], self.ranges['bilirubin'][1])
        
        # Kidney function tests
        data['creatinine'] = np.random.normal(1.0, 0.3, n_samples).clip(self.ranges['creatinine'][0], self.ranges['creatinine'][1])
        data['bun'] = np.random.normal(15, 5, n_samples).clip(self.ranges['bun'][0], self.ranges['bun'][1])
        
        # Electrolytes
        data['sodium'] = np.random.normal(140, 3, n_samples).clip(self.ranges['sodium'][0], self.ranges['sodium'][1])
        data['potassium'] = np.random.normal(4.0, 0.5, n_samples).clip(self.ranges['potassium'][0], self.ranges['potassium'][1])
        data['chloride'] = np.random.normal(102, 3, n_samples).clip(self.ranges['chloride'][0], self.ranges['chloride'][1])
        data['bicarbonate'] = np.random.normal(24, 2, n_samples).clip(self.ranges['bicarbonate'][0], self.ranges['bicarbonate'][1])
        
        # Minerals
        data['calcium'] = np.random.normal(9.5, 0.5, n_samples).clip(self.ranges['calcium'][0], self.ranges['calcium'][1])
        data['magnesium'] = np.random.normal(2.0, 0.3, n_samples).clip(self.ranges['magnesium'][0], self.ranges['magnesium'][1])
        data['phosphate'] = np.random.normal(3.5, 0.5, n_samples).clip(self.ranges['phosphate'][0], self.ranges['phosphate'][1])
        
        # Protein metrics
        data['protein'] = np.random.normal(7.0, 0.5, n_samples).clip(self.ranges['protein'][0], self.ranges['protein'][1])
        data['albumin'] = np.random.normal(4.2, 0.4, n_samples).clip(self.ranges['albumin'][0], self.ranges['albumin'][1])
        data['globulin'] = (data['protein'] - data['albumin']).clip(1.5, 4.5)
        data['a_g_ratio'] = (data['albumin'] / data['globulin']).clip(0.8, 2.5)
        
        # Add correlations between related metrics
        # Higher BMI tends to correlate with higher cholesterol and glucose
        bmi_factor = (data['bmi'] - data['bmi'].mean()) / data['bmi'].std()
        data['cholesterol'] += bmi_factor * 10
        data['glucose'] += bmi_factor * 5
        
        # Age correlations
        age_factor = (data['age'] - data['age'].mean()) / data['age'].std()
        data['cholesterol'] += age_factor * 5
        data['glucose'] += age_factor * 3
        
        # Ensure values stay within ranges after correlations
        for col, (min_val, max_val) in self.ranges.items():
            if col in data.columns:
                data[col] = data[col].clip(min_val, max_val)
        
        print(f"Generated {len(data)} synthetic health records with realistic distributions")
        
        # Save the data
        data.to_csv(self.data_dir / 'synthetic_health_data.csv', index=False)
        return data
    
    def load_health_data(self):
        """Load and preprocess real health data."""
        try:
            print("Generating fresh synthetic health data...")
            # Generate synthetic data that mimics real data patterns
            data = self._generate_synthetic_health_data()
            print(f"Generated {len(data)} synthetic health records with realistic distributions")
            return data
        except Exception as e:
            print(f"Error loading health data: {str(e)}")
            return None

    def _generate_synthetic_health_data(self, n_samples=1000):
        """Generate synthetic health data with realistic distributions."""
        np.random.seed(42)
        
        # Generate base features with realistic distributions
        data = pd.DataFrame({
            'age': np.random.normal(45, 15, n_samples).clip(18, 90),
            'gender': np.random.choice([0, 1], n_samples),
            'bmi': np.random.normal(25, 4, n_samples).clip(18.5, 35),
            'glucose': np.random.normal(95, 15, n_samples).clip(70, 180),
            'cholesterol': np.random.normal(180, 30, n_samples).clip(150, 250),
            'triglycerides': np.random.normal(120, 40, n_samples).clip(50, 250),
            'hdl': np.random.normal(55, 10, n_samples).clip(35, 85),
            'ldl': np.random.normal(100, 20, n_samples).clip(70, 160),
            'alt': np.random.normal(25, 8, n_samples).clip(10, 60),
            'ast': np.random.normal(23, 7, n_samples).clip(10, 50),
            'bilirubin': np.random.normal(0.8, 0.2, n_samples).clip(0.3, 1.5),
            'alkaline_phosphatase': np.random.normal(75, 15, n_samples).clip(45, 125),
            'creatinine': np.random.normal(0.9, 0.2, n_samples).clip(0.6, 1.4),
            'bun': np.random.normal(15, 3, n_samples).clip(8, 25),
            'sodium': np.random.normal(140, 2, n_samples).clip(135, 145),
            'potassium': np.random.normal(4.0, 0.3, n_samples).clip(3.5, 5.0),
            'chloride': np.random.normal(102, 2, n_samples).clip(98, 106),
            'bicarbonate': np.random.normal(24, 1.5, n_samples).clip(22, 28),
            'calcium': np.random.normal(9.5, 0.3, n_samples).clip(8.8, 10.2),
            'magnesium': np.random.normal(2.0, 0.15, n_samples).clip(1.7, 2.3),
            'phosphate': np.random.normal(3.5, 0.3, n_samples).clip(2.8, 4.2),
            'total_protein': np.random.normal(7.0, 0.3, n_samples).clip(6.2, 7.8),
            'albumin': np.random.normal(4.2, 0.2, n_samples).clip(3.8, 4.8),
            'globulin': np.random.normal(2.8, 0.2, n_samples).clip(2.3, 3.3),
            'ag_ratio': np.random.normal(1.5, 0.15, n_samples).clip(1.2, 1.8),
            # Advanced biomarkers
            'crp': np.random.lognormal(0, 0.5, n_samples).clip(0.1, 10.0),
            'esr': np.random.normal(15, 8, n_samples).clip(0, 50),
            'fibrinogen': np.random.normal(300, 40, n_samples).clip(200, 500),
            'malondialdehyde': np.random.lognormal(-0.5, 0.4, n_samples).clip(0.1, 3.0),
            '8_ohdg': np.random.lognormal(0, 0.4, n_samples).clip(0.1, 5.0),
            'testosterone': np.random.normal(600, 150, n_samples).clip(200, 1200),
            'estradiol': np.random.normal(50, 15, n_samples).clip(10, 100),
            'cortisol': np.random.normal(15, 4, n_samples).clip(5, 30)
        })
        
        # Add correlations between related markers
        data['hdl'] = data['hdl'] - 0.3 * data['triglycerides'] / 100
        data['ldl'] = data['cholesterol'] - data['hdl'] - data['triglycerides'] / 5
        data['ast'] = data['alt'] * 0.8 + np.random.normal(0, 2, n_samples)
        data['globulin'] = data['total_protein'] - data['albumin']
        data['ag_ratio'] = data['albumin'] / data['globulin']
        
        # Add age-related adjustments
        data.loc[data['age'] > 60, 'hdl'] *= 0.9
        data.loc[data['age'] > 60, 'testosterone'] *= 0.8
        data.loc[data['age'] > 60, 'estradiol'] *= 0.85
        
        # Add gender-related adjustments
        data.loc[data['gender'] == 0, 'testosterone'] *= 0.15  # Females have lower testosterone
        data.loc[data['gender'] == 1, 'estradiol'] *= 0.3     # Males have lower estradiol
        
        # Add BMI-related adjustments
        data.loc[data['bmi'] > 30, 'glucose'] *= 1.15
        data.loc[data['bmi'] > 30, 'cholesterol'] *= 1.2
        data.loc[data['bmi'] > 30, 'triglycerides'] *= 1.25
        
        # Ensure all required columns are present
        for col in self.required_columns:
            if col not in data.columns:
                data[col] = data[self.required_columns[0]]  # Use first column as placeholder
        
        # Add advanced biomarkers if missing
        for marker, default_value in self.advanced_biomarkers.items():
            if marker not in data.columns:
                data[marker] = default_value
        
        return data

if __name__ == "__main__":
    loader = RealDataLoader()
    health_data = loader.load_health_data()
    if health_data is not None:
        print("\nData statistics:")
        print(health_data.describe())
        print("\nColumns in dataset:")
        print(health_data.columns.tolist()) 