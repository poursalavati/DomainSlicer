# DomainSlicer
A Python utility to automate the extraction of specific domain sequences from FASTA files based on NCBI Conserved Domain Search (CD-Search) results.

## Overview

NCBI's Conserved Domain Search identifies functional domains within protein sequences, but it doesn't provide an easy way to batch-download the specific sequences of those identified domains. 

**DomainSlicer** bridges this gap. It parses the `.txt` (tab-delimited) output from a CD-Search, identifies the coordinates of your domain of interest, and uses `seqkit` to cut those regions from your original sequence file.

## Features

- **Automated Parsing**: Reads tab-delimited CD-Search result files.
- **Precision Extraction**: Uses start/end coordinates to extract exact domain regions.
- **Flexible Output**: Choose between:
  - A single multi-FASTA file containing all extracted domains.
  - Individual FASTA files for every query.
- **Clean Workflow**: Automatically manages and removes temporary files and indices.
- **User-Friendly Interface**: Simple prompts guide users through the process.

## Prerequisites

To use this script, you must have the following installed:

1.  **Python 3.x**
2.  **SeqKit**: The script relies on `seqkit` for high-performance sequence manipulation.
    - Install via Conda: `conda install -c bioconda seqkit`
    - Install via Homebrew (macOS): `brew install seqkit`
    - Or download from [Shenweiyan's SeqKit GitHub](https://github.com/shenweiyan/seqkit).

## Installation

```bash
# Clone the repository
git clone https://github.com/poursalavati/DomainSlicer.git

# Navigate to the directory
cd DomainSlicer

# Make the script executable (optional)
chmod +x domainslicer.py
```

## Usage

1.  **Run CD-Search**: Submit your sequences to the [NCBI CD-Search Tool](https://www.ncbi.nlm.nih.gov/Structure/bwrpsb/bwrpsb.cgi).
2.  **Download Results**: Once finished, download the **Hit List** as a tab-delimited file.
3.  **Run the Script**:

```bash
python domainslicer.py
```

### Interactive Prompts:
The script will ask for:
- **CD Search Result File**: The path to the tab-delimited file from NCBI.
- **Sequence File**: The path to your original FASTA/FAA file.
- **Domain Name**: The "Short Name" of the domain you want to extract (e.g., `Endornaviridae_RdRp`, `Mononeg_RNA_pol`).
- **Output Format**: Whether to merge results into one file or keep them separate.

## Example

Suppose you have a file `hitdata.txt` and you want to extract all `Trypsin` domains from `proteins.fasta`:

```text
Enter the path to the CD search result file: hitdata.txt
Enter the path to the sequence file: proteins.fasta
Enter the domain name to extract: Trypsin
Do you want separate output files for each query? (yes/no): no
```

**Output:** A file named `extracted_Trypsin.faa` containing all matched regions.

## How it Works

1.  **Parsing**: It filters the CD-Search results for the specific `Short name` you provided.
2.  **Grep**: It uses `seqkit grep` to isolate the specific parent sequence from your large FASTA file.
3.  **Subseq**: It uses `seqkit subseq` with the coordinates (`From` and `To`) found in the CD-Search results.
4.  **Cleanup**: It removes the temporary `.fai` indices and temporary sequence fragments created during the process.

## Contributing

Contributions are welcome! If you have suggestions for new features or find bugs, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
