
mkdir 'outputs'
mkdir 'data'

qiime tools import \
  --type EMPSingleEndSequences \
  --input-path $1 \
  --output-path outputs/emp-single-end-sequences.qza

qiime demux emp-single \
  --i-seqs outputs/emp-single-end-sequences.qza \
  --m-barcodes-file sample-metadata.tsv \
  --m-barcodes-column barcode-sequence \
  --o-per-sample-sequences outputs/demux.qza \
  --o-error-correction-details outputs/demux-details.qza

qiime demux summarize \
  --i-data outputs/demux.qza \
  --o-visualization outputs/demux.qzv

qiime quality-filter q-score \
 --i-demux outputs/demux.qza \
 --o-filtered-sequences outputs/demux-filtered.qza \
 --o-filter-stats outputs/demux-filter-stats.qza

qiime deblur denoise-16S \
  --i-demultiplexed-seqs outputs/demux-filtered.qza \
  --p-trim-length $2 \
  --o-representative-sequences outputs/rep-seqs-deblur.qza \
  --o-table outputs/table-deblur.qza \
  --p-sample-stats \
  --o-stats outputs/deblur-stats.qza

qiime metadata tabulate \
  --m-input-file outputs/demux-filter-stats.qza \
  --o-visualization outputs/demux-filter-stats.qzv
qiime deblur visualize-stats \
  --i-deblur-stats outputs/deblur-stats.qza \
  --o-visualization outputs/deblur-stats.qzv
mv outputs/rep-seqs-deblur.qza outputs/rep-seqs.qza
mv outputs/table-deblur.qza outputs/table.qza

qiime feature-classifier classify-sklearn \
  --i-classifier gg-13-8-99-515-806-nb-classifier.qza \
  --i-reads outputs/rep-seqs.qza \
  --o-classification outputs/taxonomy.qza

qiime metadata tabulate \
  --m-input-file outputs/taxonomy.qza \
  --o-visualization outputs/taxonomy.qzv

unzip outputs/taxonomy.qza -d newpath
cp newpath/*/data/taxonomy.tsv data/taxonomy.tsv
rm -r newpath

unzip outputs/table.qza -d newpath
cp newpath/*/data/feature-table.biom data/feature-table.biom
rm -r newpath
