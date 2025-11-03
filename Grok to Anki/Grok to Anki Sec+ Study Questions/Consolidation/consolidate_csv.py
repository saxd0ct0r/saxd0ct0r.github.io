import csv
import sys

def consolidate_csv(output_file, input_files):
    """
    Consolidates multiple CSV files with the same schema into a single output CSV file.
    The header from the first input file is used, and headers from subsequent files are skipped.
    """
    if not input_files:
        print("No input files provided.")
        return

    with open(output_file, 'w', newline='') as outf:
        writer = csv.writer(outf)
        
        for i, infile in enumerate(input_files):
            try:
                with open(infile, 'r', newline='') as inf:
                    reader = csv.reader(inf)
                    
                    if i == 0:
                        # Write all rows including header
                        for row in reader:
                            writer.writerow(row)
                    else:
                        # Skip header
                        next(reader, None)
                        for row in reader:
                            writer.writerow(row)
            except FileNotFoundError:
                print(f"File not found: {infile}")
            except csv.Error as e:
                print(f"CSV error in file {infile}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python consolidate.py <output.csv> <input1.csv> <input2.csv> ...")
        sys.exit(1)
    
    output_file = sys.argv[1]
    input_files = sys.argv[2:]
    
    consolidate_csv(output_file, input_files)
    print(f"Consolidated CSV written to {output_file}")