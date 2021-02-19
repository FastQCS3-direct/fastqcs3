**Use Case 1:**
Validation of input data type 

User: Inputs sequencing data

Function: Parses data, determines if in correct .fastq format

Results: No errors/errors
__________________________________________________________________________
**Use Case 2:**
Module 1: Information on sequencing quality

User: Call function to examine quality of sequencing data

Function: Reads .fastq files, assesses for quality and app callback to Dash

Results: Plots of summary statistics, sequencing counts etc. 
__________________________________________________________________________
**Use Case 3:**
Module 3: Visualization of sequencing results

User: Call function to examine results of sequence mapping
 
Function: Maps sequences to database (NCBI) using dependent packages (FastQC, Qiime?)

Results: Plots of species abundance, diversity, proportion of mapped reads, clustering analysis (Scikit Bio) 


