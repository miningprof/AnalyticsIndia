import pandas as pd

def load_data_from_file(file_path):
    if not file_path: raise ValueError("File path cannot be empty.")
    if file_path.endswith('.csv'):
        try: return pd.read_csv(file_path)
        except Exception as e: raise Exception(f"Error reading CSV file '{file_path}': {e}")
    elif file_path.endswith('.xlsx'):
        try: return pd.read_excel(file_path, engine='openpyxl')
        except Exception as e: raise Exception(f"Error reading XLSX file '{file_path}': {e}")
    elif file_path.endswith('.ods'):
        try: return pd.read_excel(file_path, engine='odf')
        except Exception as e: raise Exception(f"Error reading ODS file '{file_path}': {e}")
    else: raise ValueError(f"Unsupported file type: {file_path}.")
