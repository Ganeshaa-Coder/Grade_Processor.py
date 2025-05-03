import csv

def process_grades(file_path):
    results = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['Name']
            marks = [int(row[subj]) for subj in row if subj != 'Name']
            total = sum(marks)
            avg = total / len(marks)

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
    results = process_grades(input_file)
    write_results(results, output_file)
    print(f"Results written to {output_file}")


