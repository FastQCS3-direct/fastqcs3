 FastQCS3: Fast Quantitative Checking of 16S Sequencing results Summary

#### Main Repo for CHEM E 545/546 Final Project


## Overview/Purpose
The purpose of this software is to give users a tool to quickly run some quality checking immediately after sequencing results become available. The software will be designed to be a python installable package that is run from the command line. Designed modularly, the user will have the chance to specify what kind of FastQCS3 they want to perform.

## Installing Dependencies
This package relies on QIIME2, a previously published microbiome analysis package, to pre-process input data and focus on sequencing quality metrics. To be able to utilize FastQCS3, QIIME2 must be installed first. 

#### Installing Miniconda
You can follow the instructions here to install Miniconda: https://conda.io/projects/conda/en/latest/user-guide/install/index.html

#### Updating Miniconda
conda update conda

#### Installing wget
conda install wget

### If you have a Mac OS...
wget https://data.qiime2.org/distro/core/qiime2-2020.11-py36-osx-conda.yml
conda env create -n qiime2-2020.11 --file qiime2-2020.11-py36-osx-conda.yml
rm qiime2-2020.11-py36-osx-conda.yml

### If you have a Windows OS on Linux...
wget https://data.qiime2.org/distro/core/qiime2-2020.11-py36-linux-conda.yml
conda env create -n qiime2-2020.11 --file qiime2-2020.11-py36-linux-conda.yml
rm qiime2-2020.11-py36-linux-conda.yml

### If you have a Windows OS...
the process to install wget will be a little more complicated--you'll have to download wget and move the correct exe files into your correct system directories. This can be complicated if you don't already have administrator privileges--we recommend using the Mac OS or Windows Subsystem for Linux.

## To activate your environment,

"conda activate qiime2-2020.11"

You can deactivate at any time with conda deactivate.

