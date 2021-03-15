 FastQCS3: Fast Quantitative Checking of 16S Gene Sequencing 

#### Main Repo for CHEM E 545/546 Final Project

## Overview/Purpose
The purpose of this software is to give users a tool to quickly run quality checking immediately after sequencing results become available. The software will be designed to be a python installable package that is run from the command line. Designed modularly, the user will have the chance to specify what kind of FastQCS3 they want to perform.

## Installing Dependencies
This package relies on [QIIME2](https://docs.qiime2.org/2020.11/about/), a previously published microbiome analysis package, to pre-process input data and [Biopython](https://biopython.org/) to extract sequencing quality metrics.
FastQCS3 seeks to utilize QIIME2 data processing capabilities while focusing on building an interactive dashboard with more useful visualization tools than QIIME2's .qza formats. To be able to utilize FastQCS3, QIIME2, Biopython, and Dash must all be installed in your working environment. QIIME2 only runs on Mac OS and on Windows Subsystem for Linux. Information on installing Windows Subsytem for Linux is found below.  

#### Installing Miniconda
You can follow the instructions [here](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) to install Miniconda. 

#### Updating Miniconda
`conda update conda`

#### Creating the FastQCS3 Environment from this Repo
Once you have Miniconda, you can create an environment using the provided environment.yml file contained in this repo and the following command. 

`conda env create -n fastqcs3 --file environment.yml`

Due to the size of the QIIME2 package, creating the environment can take awhile. Once it has finished, activate your environment through `conda activate fastqcs3`

You can deactivate at any time using `conda deactivate`.

### Creating an Environment from Scratch
To create an environment from scratch, you'll have to download QIIME2 using the following instructions and install Biopython and Dash as well.

#### Installing wget
`conda install wget`

If `conda install wget` doesn't work, you can also try using `pip install wget`, `sudo apt-get install wget`, or use package managers like [homebrew](https://brew.sh/) to `brew install wget`.

### If you have a Mac OS...
`wget https://data.qiime2.org/distro/core/qiime2-2020.11-py36-osx-conda.yml`

`conda env create -n qiime2-2020.11 --file qiime2-2020.11-py36-osx-conda.yml`

`rm qiime2-2020.11-py36-osx-conda.yml`

### If you have a Windows OS on Linux...
`wget https://data.qiime2.org/distro/core/qiime2-2020.11-py36-linux-conda.yml`

`conda env create -n qiime2-2020.11 --file qiime2-2020.11-py36-linux-conda.yml`

`rm qiime2-2020.11-py36-linux-conda.yml`

### If you have a Windows OS...
the process to install wget will be a more complicated. You'll have to download wget and move the correct exe files into your correct system directories as shown [here](https://builtvisible.com/download-your-website-with-wget/).

This can be complicated if you don't already have administrator privileges set up in these files on your machine; we recommend using the Mac OS or Windows Subsystem for Linux. Instructions on installing Windows subsystem for Linux can be found [here](https://docs.microsoft.com/en-us/windows/wsl/install-win10). 

### To activate your environment,

`conda activate qiime2-2020.11`

You can deactivate at any time with `conda deactivate`.

## Operating Instructions

After git cloning this repo, copy your directory of FastQ files to your local version of this repo and run `python fastQCS3_pkl.py`. This will begin the automated QIIME2 process of analyzing your data by asking you for your fastq directory name. Follow along with the prompts to save your results into a user-specified pkl file.

Run `python fastQCS3_dashboard.py` and follow along with those prompts to return your dashboard. The link to your dashboard can then be copied into your browser to visualize your data.

A demo video can be found [here](link to Ben's video?). We have provided two sets of demo data in `demo_data_v1`(from the QIIME2 "Moving Pictures" tutorial) and `demo_data_v2`(Evan's personal sequencing results that inspired this project) if you wish to practice.


#### Important Notes about Usage
	1. Your fastq files should be labelled with an alphabetical character in front:
		i.e. `A1_S1_L001_R1_001.fastq.gz` instead of `1_S1_LOO1_R1_001.fastq.gz`
		
	2. If running multiple datasets at once, you will have to change the host name on line 204 of
	the `fastQCS3_dashboard.py` file every time you run a new dataset to visualize all at the same time.
		i.e. `app.run_server(host='127.0.0.1', port='8050', debug=False)` followed by
		`app.run_server(host='128.0.0.1', port='8050', debug=False)`

#### Notes about CI
	CI can be difficult when running in such a large and complicated environment (like one containing QIIME2).
	Check back for updates about using continuous integration through Travis CI.
