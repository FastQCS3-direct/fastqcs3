mkdir 'outputs'
mkdir 'data'

qiime tools import \
  --type EMPSingleEndSequences \
  --input-path $1 \
  --output-path outputs/emp-single-end-sequences.qza

qiime demux emp-single \
  --i-seqs outputs/emp-single-end-sequences.qza \
  --m-barcodes-file metadata/$2 \
  --m-barcodes-column barcode-sequence \
  --o-per-sample-sequences outputs/demux.qza \
  --o-error-correction-details outputs/demux-details.qza

qiime demux summarize \
  --i-data outputs/demux.qza \
  --o-visualization outputs/demux.qzv
  
qiime tools export \
   --input-path outputs/demux.qzv \
   --output-path data/exported_demux

qiime tools export \
   --input-path outputs/demux.qza \
   --output-path data/exported_demux
