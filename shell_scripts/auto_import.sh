mkdir 'outputs'
mkdir 'data'

qiime tools import \
  --type 'SampleData[SequencesWithQuality]' \
  --input-path $1 \                    
  --input-format CasavaOneEightSingleLanePerSampleDirFmt \
  --output-path outputs/demux.qza

qiime demux summarize \                               
  --i-data outputs/demux.qza \                                               
  --o-visualization outputs/demux.qzv

qiime tools export \
   --input-path outputs/demux.qzv \
   --output-path data/exported_demux

qiime tools export \
   --input-path outputs/demux.qza \
   --output-path data/exported_demux
