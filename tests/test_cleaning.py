import unittest
import pandas as pd
import numpy as np
from src.cleaning_campaign import limpiar_df_campana

class TestCleaningCampaign(unittest.TestCase):
    def setUp(self):
        """Create sample data for testing"""
        self.sample_data = pd.DataFrame({
            'age': [30, np.nan, 999],  # Test age cleaning and imputation
            'job': ['admin.', 'blue-collar', 'unknown'],
            'marital': ['married', 'single', 'divorced'],
            'education': ['university.degree', np.nan, 'basic.9y'],
            'default': ['no', 'unknown', 'yes'],
            'housing': ['yes', 'no', 'unknown'],
            'loan': ['no', 'yes', 'no'],
            'contact': ['cellular', 'telephone', 'cellular'],
            'month': ['may', 'jun', 'jul'],
            'day_of_week': ['mon', 'tue', 'wed'],
            'duration': [100, 200, 300],
            'campaign': [1, 2, 3],
            'pdays': [999, 5, 999],  # 999 should handle specially
            'previous': [0, 1, 0],
            'poutcome': ['nonexistent', 'failure', 'success'],
            'emp.var.rate': ['1.1', '-1.8', '1,4'],  # Test float conversion with comma
            'cons.price.idx': ['93.994', '92.893', '93,200'],
            'cons.conf.idx': ['-36.4', '-46.2', '-42,0'],
            'euribor3m': ['4.857', '1.299', '4,191'],
            'nr.employed': ['5191.0', '5099.1', '5195,8'],
            'y': ['no', 'yes', 'no'],
            'date': ['01-mayo-2012', '15-junio-2013', np.nan] # Test date parsing
        })

    def test_numeric_conversion_and_cleaning(self):
        """Test conversion of numeric columns with commas"""
        df_clean = limpiar_df_campana(self.sample_data.copy())
        
        # Check if commas were replaced and converted to float
        self.assertTrue(pd.api.types.is_float_dtype(df_clean['euribor3m']))
        self.assertAlmostEqual(df_clean.loc[2, 'euribor3m'], 4.191)
        
    def test_pdays_handling(self):
        """Test pdays 999 conversion to NaN and dummy creation"""
        df_clean = limpiar_df_campana(self.sample_data.copy())
        
        # 999 should be NaN
        self.assertTrue(np.isnan(df_clean.loc[0, 'pdays']))
        self.assertEqual(df_clean.loc[1, 'pdays'], 5)
        
        # previous_contact should be 1 if pdays < 999
        self.assertEqual(df_clean.loc[0, 'previous_contact'], 0)
        self.assertEqual(df_clean.loc[1, 'previous_contact'], 1)

    def test_target_encoding(self):
        """Test target variable binary encoding"""
        df_clean = limpiar_df_campana(self.sample_data.copy())
        
        self.assertEqual(df_clean.loc[0, 'y'], 0)
        self.assertEqual(df_clean.loc[1, 'y'], 1)

    def test_date_parsing(self):
        """Test spanish date parsing"""
        df_clean = limpiar_df_campana(self.sample_data.copy())
        
        # Check first date: 01-mayo-2012 -> 2012-05-01
        self.assertEqual(df_clean.loc[0, 'date'].year, 2012)
        self.assertEqual(df_clean.loc[0, 'date'].month, 5)
        self.assertEqual(df_clean.loc[0, 'contact_month'], 5)
        self.assertEqual(df_clean.loc[0, 'contact_year'], 2012)

    def test_imputation(self):
        """Test imputation logic"""
        df_clean = limpiar_df_campana(self.sample_data.copy())
        
        # Education mode imputation (mode of sample is university.degree/basic.9y? Wait, sample is small)
        # In sample: 'university.degree', NaN, 'basic.9y'. Mode is likely one of them.
        self.assertFalse(df_clean['education'].isnull().any())
        
        # Age should be int
        self.assertTrue(pd.api.types.is_integer_dtype(df_clean['age']))

if __name__ == '__main__':
    unittest.main()
