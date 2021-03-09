import subprocess

def auto_qiime(directory,trimlength):
    subprocess.run(['bash','-c','bash auto_qiime.sh '+directory+' '+trimlength])

directory=input('Directory of .fastq files:')
trimlength=input('Sequencing trim length:')

auto_qiime(directory,trimlength)
