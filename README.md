# fastqcs3
# Main Repo for CHEM E 545/546 Final Project

__Name:__ FastQCS3: Fast Quantitative Checking of 16S Sequencing results Summary. 

__Overview/Purpose:__ The purpose of this software is to give users a tool to quickly run some quality checking immediately after sequencing results become available. The software will be designed to be a python installable package that is run from the command line. Designed modularly, the user will have the chance to specify what kind of FastQCS3 they want to perform.

# Use Cases:
1. Who is the user: The user is any reseacher doing sequencing and/or sequencing analysis of microbial communities
2. What information does the user provide: Sequencing data, in `.fastq` or `.fastq.gz` file format and flags to specify desired output
3. What responses the system provides: Information on sequencing quality, visualization of sequencing results, summary statistics, all provided in graphical Dash interface. Note: this tool is especially useful for microbiome research
