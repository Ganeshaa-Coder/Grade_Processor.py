import pandas as pd

def get_grade(average):
    """Assigns a grade based on the average mark."""
    if average >= 90:
        return 'A'
    elif average >= 75:
        return 'B'
    elif average >= 60:
        return 'C'
    else:
        return 'D'

def process_grades(file_path):
    """
    Processes student grades from a CSV file using pandas.

    Args:
        file_path (str): The path to the input CSV file.

    Returns:
        pandas.DataFrame or None: A DataFrame containing Name, Total, Average, 
                                   and Grade, or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

    # Check if 'Name' column exists
    if 'Name' not in df.columns:
        print("Error: 'Name' column not found in the CSV.")
        return None

    # Identify subject columns (all columns except 'Name')
    subject_columns = [col for col in df.columns if col != 'Name']
    if not subject_columns:
        print("Error: No subject columns found (excluding 'Name').")
        return None # Or return df[['Name']] if that's desired

    # Ensure subject columns are numeric, coercing errors to NaN
    for col in subject_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Option 1: Fill missing/non-numeric marks with 0
    df[subject_columns] = df[subject_columns].fillna(0)
    # Option 2: Drop rows with missing/non-numeric marks (alternative)
    # df = df.dropna(subset=subject_columns) 
    # if df.empty:
    #     print("Error: No valid numeric data found in subject columns after handling errors.")
    #     return None


    # Calculate Total marks
    df['Total'] = df[subject_columns].sum(axis=1)

    # Calculate Average marks
    num_subjects = len(subject_columns)
    # Avoid division by zero if num_subjects is 0 (already checked, but good practice)
    if num_subjects > 0:
        df['Average'] = df['Total'] / num_subjects
        # Round average to 2 decimal places for consistency
        df['Average'] = df['Average'].round(2) 
    else:
        # Should not happen due to earlier check, but handle defensively
        df['Average'] = 0.0 

    # Determine Grade using the helper function
    df['Grade'] = df['Average'].apply(get_grade)

    # Select and return only the required columns
    results_df = df[['Name', 'Total', 'Average', 'Grade']]
    return results_df

def write_results(results_df, output_file):
    """Writes the results DataFrame to a CSV file."""
    if results_df is not None and not results_df.empty:
        try:
            results_df.to_csv(output_file, index=False)
            print(f"Processed grades saved to {output_file}")
        except Exception as e:
            print(f"Error writing results to CSV '{output_file}': {e}")
    elif results_df is not None and results_df.empty:
         print("Warning: The results DataFrame is empty. Nothing written.")
    else:
        # This case means process_grades returned None
        print("Grade processing failed. No results to write.")


if __name__ == "__main__":
    # Ensure the input filename matches the actual file case ('Students.csv')
    input_file = 'Students.csv' 
    output_file = 'graded_students.csv'
    
    print(f"Processing grades from {input_file}...")
    results_dataframe = process_grades(input_file)

    # write_results handles the case where results_dataframe might be None or empty
    write_results(results_dataframe, output_file)
