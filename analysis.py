import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Define file paths
nyc_file = "data/nyc_inspection_100.csv"
chicago_file = "data/chicago_inspection_100.csv"

# Create dummy data directory and files if they don't exist for testing
if not os.path.exists("data"):
    os.makedirs("data")
if not os.path.exists(nyc_file):
    # Create a minimal dummy CSV for NYC if file is missing
    print(f"Warning: {nyc_file} not found. Creating a dummy file.")
    dummy_nyc_data = {'CAMIS': [1, 2, 3], 'ACTION': ['Violations were cited in the following area(s).', 'No violations were recorded at the time of this inspection.', 'Establishment Closed by DOHMH. Violations were cited in the following area(s) and those requiring immediate action were addressed.'], 'GRADE': ['A', '', '']}
    pd.DataFrame(dummy_nyc_data).to_csv(nyc_file, index=False)
if not os.path.exists(chicago_file):
     # Create a minimal dummy CSV for Chicago if file is missing
    print(f"Warning: {chicago_file} not found. Creating a dummy file.")
    dummy_chi_data = {'Inspection ID': [101, 102, 103, 104, 105], 'Results': ['Pass', 'Pass w/ Conditions', 'Fail', 'Out of Business', 'No Entry']}
    pd.DataFrame(dummy_chi_data).to_csv(chicago_file, index=False)

# --- Load Data ---
try:
    nyc_df = pd.read_csv(nyc_file)
    chi_df = pd.read_csv(chicago_file)
    print("Datasets loaded successfully.")
except FileNotFoundError as e:
    print(f"Error loading file: {e}")
    print("Please ensure 'nyc_inspection_100.csv' and 'chicago_inspection_100.csv' are in the 'data' directory.")
    exit()
except Exception as e:
    print(f"An error occurred during file loading: {e}")
    exit()


# --- Data Cleaning and Standardization ---

# Standardize NYC Outcomes
def standardize_nyc_outcome(row):
    action = str(row['ACTION']).lower()
    grade = str(row['GRADE'])
    if 'no violations' in action:
        return 'Pass' # Clear pass
    elif 'closed' in action or 're-closed' in action:
        return 'Fail/Closed'
    elif 'violations were cited' in action:
         # Graded A, B, C or even ungraded/pending are still considered 'Pass' in the sense the business remains open
         # We could differentiate further, but let's keep it simple for comparison
         return 'Pass'
    else:
        # Handle NaN or other unexpected values if necessary
         return 'Other/Unknown' # Catch-all for unexpected values or blank actions

nyc_df['Standardized_Outcome'] = nyc_df.apply(standardize_nyc_outcome, axis=1)

# Standardize Chicago Outcomes
def standardize_chicago_outcome(result):
    result_str = str(result).lower()
    if 'pass w/ conditions' in result_str or result_str == 'pass':
        return 'Pass'
    elif 'fail' in result_str:
        return 'Fail/Closed'
    elif 'out of business' in result_str:
         # Grouping OOB with Fail/Closed for simplicity in this comparison context
         return 'Fail/Closed'
    elif 'no entry' in result_str or 'not ready' in result_str:
        return 'Other/Inconclusive'
    else:
        return 'Other/Unknown' # Catch-all

# Need to handle potential BOM (Byte Order Mark) in Chicago header if present
chi_df.columns = chi_df.columns.str.replace('\ufeff', '', regex=True) # Remove BOM if exists
if 'Results' not in chi_df.columns:
     print("Error: 'Results' column not found in Chicago data. Columns found:", chi_df.columns)
     exit()

chi_df['Standardized_Outcome'] = chi_df['Results'].apply(standardize_chicago_outcome)

# --- Calculate Outcome Percentages ---
nyc_outcomes = nyc_df['Standardized_Outcome'].value_counts(normalize=True) * 100
chi_outcomes = chi_df['Standardized_Outcome'].value_counts(normalize=True) * 100

# Combine results for plotting
nyc_outcomes_df = nyc_outcomes.reset_index()
nyc_outcomes_df.columns = ['Standardized_Outcome', 'Percentage']
nyc_outcomes_df['City'] = 'NYC'

chi_outcomes_df = chi_outcomes.reset_index()
chi_outcomes_df.columns = ['Standardized_Outcome', 'Percentage']
chi_outcomes_df['City'] = 'Chicago'

combined_outcomes = pd.concat([nyc_outcomes_df, chi_outcomes_df], ignore_index=True)

# --- Visualization ---
plt.figure(figsize=(10, 6))
sns.barplot(data=combined_outcomes, x='City', y='Percentage', hue='Standardized_Outcome', palette='viridis')

plt.title('Comparison of Standardized Inspection Outcomes (NYC vs. Chicago)')
plt.ylabel('Percentage of Inspections (%)')
plt.xlabel('City')
plt.ylim(0, 100) # Ensure y-axis goes up to 100%

# Format y-axis ticks as percentages
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0f}%'.format(y)))

plt.legend(title='Outcome', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout(rect=[0, 0, 0.85, 1]) # Adjust layout to make space for legend
plt.show()

# --- Interpretation ---
print("\n--- Interpretation ---")
print("The bar chart compares the distribution of standardized inspection outcomes between NYC and Chicago based on the provided sample datasets.")
print("Categories were simplified for comparison:")
print("  - 'Pass': Includes inspections resulting in continued operation (NYC: No violations, Graded A/B/C, Violations cited but not closed; Chicago: Pass, Pass w/ Conditions).")
print("  - 'Fail/Closed': Includes inspections resulting in closure or the business being out of operation (NYC: Closed/Re-closed; Chicago: Fail, Out of Business).")
print("  - 'Other/Inconclusive': Includes inspections where entry wasn't possible or the facility wasn't ready (Chicago data only in this sample).")
print("  - 'Other/Unknown': Catches any unexpected or missing data.")
print("\nNote:")
print("- This analysis uses simplified categories due to differences in grading/reporting systems.")
print("- The results are based on potentially small sample datasets ('_100.csv') and may not represent the overall distribution for each city.")
print("- NYC uses letter grades (A, B, C) which indicate compliance levels within the 'Pass' category, a nuance not fully captured in this simplified comparison.")
print("- Chicago's 'Pass w/ Conditions' implies violations were found but corrected or not severe enough for failure, similar to NYC's 'Violations Cited' without closure.")