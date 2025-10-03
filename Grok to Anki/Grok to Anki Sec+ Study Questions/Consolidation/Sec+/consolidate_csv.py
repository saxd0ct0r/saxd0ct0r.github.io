import csv
import sys

def consolidate_csv(output_file, input_files, encoding='utf-8'):
    """
    Consolidates multiple CSV files with the same schema into a single output CSV file.
    The header from the first input file is used, and headers from subsequent files are skipped.
    
    Args:
        output_file (str): Path to the output consolidated CSV file.
        input_files (list): List of paths to input CSV files.
        encoding (str): Encoding to use for reading and writing files (default: 'utf-8').
    """
    if not input_files:
        print("No input files provided.")
        return

    try:
        with open(output_file, 'w', newline='', encoding=encoding) as outf:
            writer = csv.writer(outf)
            
            for i, infile in enumerate(input_files):
                try:
                    with open(infile, 'r', newline='', encoding=encoding) as inf:
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
                except UnicodeDecodeError as e:
                    print(f"Encoding error in file {infile}: {e}")
                    print(f"Try using 'utf-8-sig' encoding or check the file for invalid characters.")
                except csv.Error as e:
                    print(f"CSV error in file {infile}: {e}")
    except Exception as e:
        print(f"Error writing to output file {output_file}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python consolidate.py <output.csv> <input1.csv> <input2.csv> ...")
        sys.exit(1)
    
    output_file = sys.argv[1]
    input_files = sys.argv[2:]
    
    # Try UTF-8 first, fall back to utf-8-sig if needed
    try:
        consolidate_csv(output_file, input_files, encoding='utf-8')
    except UnicodeDecodeError:
        print("UTF-8 encoding failed, attempting with utf-8-sig...")
        consolidate_csv(output_file, input_files, encoding='utf-8-sig')
    
    print(f"Consolidated CSV written to {output_file}")