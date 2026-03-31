import subprocess
import csv
import os

def extract_domain_regions(cd_result_file, sequence_file, domain_name, single_output=False):
    domain_regions = []

    # Parse CD search results to find domains of the specified type
    with open(cd_result_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        headers = None
        
        for line in reader:
            if line and not line[0].startswith('#'):
                headers = line
                break

        if headers is None:
            raise ValueError("No headers found in the CD search result file")

        short_name_idx = headers.index('Short name')
        query_idx = headers.index('Query')
        start_idx = headers.index('From')
        end_idx = headers.index('To')

        for row in reader:
            if len(row) < max(short_name_idx, query_idx, start_idx, end_idx) + 1:
                continue
            query = row[query_idx].split('>')[1].split()[0]  # Get the query ID after 'Q#2 - >' and until the first space
            short_name = row[short_name_idx]
            if domain_name in short_name:
                start = int(row[start_idx])
                end = int(row[end_idx])
                domain_regions.append((query, start, end))

    print(f"Extracted {len(domain_regions)} regions")

    if single_output:
        output_file = f"extracted_{domain_name}.faa"
        with open(output_file, 'w') as out_f:
            for query, start, end in domain_regions:
                try:
                    # seqkit grep to get the full sequence by ID
                    grep_command = f"seqkit grep -r -p '{query}' {sequence_file}"
                    full_sequence = subprocess.check_output(grep_command, shell=True).decode('utf-8')

                    # full sequence temporarily
                    temp_seq_file = f"{query}.temp.faa"
                    with open(temp_seq_file, 'w') as temp_f:
                        temp_f.write(full_sequence)

                    # seqkit range to extract the specific region
                    range_command = f"seqkit subseq -r {start}:{end} {temp_seq_file}"
                    domain_sequence = subprocess.check_output(range_command, shell=True).decode('utf-8')

                    # the extracted domain sequence to the output file
                    out_f.write(domain_sequence)

                    print(f"Extracted {domain_name} domain for {query} from {start} to {end}")

                except subprocess.CalledProcessError as e:
                    print(f"Error processing {query}: {e}")

                # Clean up temporary files and fai files
                temp_seq_file = f"{query}.temp.faa"
                fai_file = f"{temp_seq_file}.seqkit.fai"
                if os.path.exists(temp_seq_file):
                    os.remove(temp_seq_file)
                if os.path.exists(fai_file):
                    os.remove(fai_file)

    else:
        for query, start, end in domain_regions:
            try:
                grep_command = f"seqkit grep -r -p '{query}' {sequence_file}"
                full_sequence = subprocess.check_output(grep_command, shell=True).decode('utf-8')

                temp_seq_file = f"{query}.temp.faa"
                with open(temp_seq_file, 'w') as temp_f:
                    temp_f.write(full_sequence)

                range_command = f"seqkit subseq -r {start}:{end} {temp_seq_file}"
                domain_sequence = subprocess.check_output(range_command, shell=True).decode('utf-8')

                output_file = f"{query}_{domain_name}.faa"
                with open(output_file, 'w') as out_f:
                    out_f.write(domain_sequence)

                print(f"Extracted {domain_name} domain for {query} from {start} to {end}")

            except subprocess.CalledProcessError as e:
                print(f"Error processing {query}: {e}")

            temp_seq_file = f"{query}.temp.faa"
            fai_file = f"{temp_seq_file}.seqkit.fai"
            if os.path.exists(temp_seq_file):
                os.remove(temp_seq_file)
            if os.path.exists(fai_file):
                os.remove(fai_file)

# Prompts
def prompt_output_format():
    while True:
        choice = input("Do you want separate output files for each query? (yes/no): ").strip().lower()
        if choice in {'yes', 'no'}:
            return choice == 'no'
        print("Invalid choice. Please enter 'yes' or 'no'.")

# Examples
cd_result_file = input("Enter the path to the CD search result file: ").strip()
sequence_file = input("Enter the path to the sequence file: ").strip()
domain_name = input("Enter the domain name to extract: ").strip()

single_output = prompt_output_format()
extract_domain_regions(cd_result_file, sequence_file, domain_name, single_output)
