 FastQCS3: Fast Quantitative Checking of 16S Gene Sequencing 

#### Main Repo for CHEM E 545/546 Final Project

## Overview/Purpose
The purpose of this software is to give users a tool to quickly run quality checking immediately after sequencing results become available. The software will be designed to be a python installable package that is run from the command line. Designed modularly, the user will have the chance to specify what kind of FastQCS3 they want to perform.

## Installing Dependencies
This package relies on [QIIME2](https://docs.qiime2.org/2020.11/about/), a previously published microbiome analysis package, to pre-process input data and provide sequencing quality metrics. FastQCS3 seeks to utilize QIIME2 data processing capabilities while focusing on building an interactive dashboard with more useful visualization tools than QIIME2's .qza formats. To be able to utilize FastQCS3, QIIME2 must also be installed. 

#### Installing Miniconda
You can follow the instructions [here](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) to install Miniconda. 

#### Updating Miniconda
`conda update conda`

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

## To activate your environment,

`conda activate qiime2-2020.11`

You can deactivate at any time with `conda deactivate`.

## From QIIME2 to FastQCS3
Include explanation of Nick's files that automate QIIME2 processing?
