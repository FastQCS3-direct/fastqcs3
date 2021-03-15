qiime dada2 denoise-single \
  --i-demultiplexed-seqs outputs/demux.qza \
  --p-trim-left 0 \
  --p-trunc-len $1 \
  --verbose \
  --o-representative-sequences outputs/rep-seqs-dada2.qza \
  --o-table outputs/table-dada2.qza \
  --o-denoising-stats outputs/stats-dada2.qza

qiime metadata tabulate \
  --m-input-file outputs/stats-dada2.qza \
  --o-visualization outputs/stats-dada2.qzv

mv outputs/rep-seqs-dada2.qza outputs/rep-seqs.qza
mv outputs/table-dada2.qza outputs/table.qza

qiime feature-table summarize \
  --i-table outputs/table.qza \
  --o-visualization outputs/table.qzv \
  --m-sample-metadata-file sample-metadata.tsv
  
qiime tools export \
  --input-path outputs/table.qzv \
  --output-path data/features