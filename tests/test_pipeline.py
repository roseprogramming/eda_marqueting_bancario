import unittest
import pandas as pd
import os
from unittest.mock import patch, MagicMock
from src.pipeline import project_root

class TestPipeline(unittest.TestCase):
    def test_project_root_exists(self):
        """Test that project root is correctly identified and exists"""
        self.assertTrue(os.path.exists(project_root))
        self.assertTrue(os.path.isdir(project_root))

    @patch('src.pipeline.pd.read_csv')
    @patch('src.pipeline.pd.read_excel')
    @patch('src.pipeline.limpiar_df_campana')
    @patch('src.pipeline.limpiar_nombres_columnas')
    def test_pipeline_imports(self, mock_limpiar_cols, mock_limpiar_campana, mock_read_excel, mock_read_csv):
        """Test that pipeline modules can be imported and functions mocked"""
        # This test mainly verifies that imports in pipeline.py are correct
        # after our refactoring of cleaning_campaign.py
        import src.pipeline as pipeline
        
        # Verify functions exist in the module
        self.assertTrue(hasattr(pipeline, 'limpiar_df_campana'))
        self.assertTrue(hasattr(pipeline, 'main'))

if __name__ == '__main__':
    unittest.main()
