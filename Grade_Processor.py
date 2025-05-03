import csv

def process_grades(file_path):
    results = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader): # Use enumerate to get row number for warning
            # Check if 'Name' key exists and is not None
            if 'Name' not in row or row['Name'] is None:
                print(f"Warning: Skipping row {i+1} due to missing or empty 'Name'.")
                continue # Skip this row

            name = row['Name']
            valid_marks = []
            # Iterate through subjects and marks for the current student
            for subj, mark_str in row.items():
                if subj != 'Name': # Exclude the 'Name' column
                    try:
                        # Attempt to convert mark to integer
                        mark_int = int(mark_str)
                        valid_marks.append(mark_int)
                    except ValueError:
                        # If conversion fails, ignore this mark and continue
                        pass # Mark is not a valid integer, skip it

            # Calculate total sum from valid marks only
            total = sum(valid_marks)

            # Calculate average, handling the case of zero valid marks
            if len(valid_marks) > 0:
                avg = total / len(valid_marks)
            else:
                avg = 0 # Set average to 0 if no valid marks were found

            # Determine grade based on average
            if avg >= 90:
                grade = 'A'
            elif avg >= 75:
                grade = 'B'
            elif avg >= 60:
                grade = 'C'
            else:
                grade = 'D'

            results.append({
                'Name': name,
                'Total': total,
                'Average': round(avg, 2),
                'Grade': grade
            })
    return results

def write_results(results, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Name', 'Total', 'Average', 'Grade']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    input_file = 'students.csv'
    output_file = 'graded_students.csv'
    # Assuming students.csv exists and is formatted correctly for the script to run
    try:
        results = process_grades(input_file)
        write_results(results, output_file)
        print(f"Results written to {output_file}")
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
