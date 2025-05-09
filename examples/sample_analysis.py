import sys, os
import pandas as pd

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.core import descriptive_stats

def main():
    data_path = os.path.join(os.path.dirname(__file__), 'sample_data', 'grades.csv')
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Error: Sample data file not found at {data_path}."); return

    print("--- Sample Data Head ---")
    print(df.head())

    math_scores = df['Math_Score'].dropna()
    if not math_scores.empty:
        print("\n--- Descriptive Statistics for Math Scores ---")
        stats_results = descriptive_stats.calculate_descriptive_stats(math_scores)
        for key, value in stats_results.items():
            print(f"  {key}: {value:.2f}" if isinstance(value, float) else f"  {key}: {value}")
    else:
        print("\nMath scores column is empty or all NaN after cleaning.")

if __name__ == '__main__':
    main()
