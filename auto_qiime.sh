
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

qiime dada2 denoise-single \
  --i-demultiplexed-seqs outputs/demux.qza \
  --p-trim-left 0 \
  --p-trunc-len $2 \
  --o-representative-sequences outputs/rep-seqs-dada2.qza \
  --o-table outputs/table-dada2.qza \
  --o-denoising-stats outputs/stats-dada2.qza

qiime metadata tabulate \
  --m-input-file outputs/stats-dada2.qza \
  --o-visualization outputs/stats-dada2.qzv

mv outputs/rep-seqs-dada2.qza outputs/rep-seqs.qza
mv outputs/table-dada2.qza outputs/table.qza

qiime feature-classifier classify-sklearn \
  --i-classifier gg-13-8-99-515-806-nb-classifier.qza \
  --i-reads outputs/rep-seqs.qza \
  --o-classification outputs/taxonomy.qza

qiime metadata tabulate \
  --m-input-file outputs/taxonomy.qza \
  --o-visualization outputs/taxonomy.qzv

qiime phylogeny align-to-tree-mafft-fasttree \
  --i-sequences outputs/rep-seqs.qza \
  --o-alignment outputs/aligned-rep-seqs.qza \
  --o-masked-alignment outputs/masked-aligned-rep-seqs.qza \
  --o-tree outputs/unrooted-tree.qza \
  --o-rooted-tree outputs/rooted-tree.qza

qiime diversity core-metrics-phylogenetic \
  --i-phylogeny outputs/rooted-tree.qza \
  --i-table outputs/table.qza \
  --p-sampling-depth 1103 \
  --m-metadata-file sample-metadata.tsv \
  --output-dir outputs/core-metrics-results

unzip outputs/taxonomy.qza -d newpath
cp newpath/*/data/taxonomy.tsv data/taxonomy.tsv
rm -r newpath

unzip outputs/table.qza -d newpath
cp newpath/*/data/feature-table.biom data/feature-table.biom
rm -r newpath

qiime tools export \
   --input-path outputs/demux.qzv \
   --output-path data/exported_demux

qiime tools export \
   --input-path outputs/demux.qza \
   --output-path data/exported_demux

unzip outputs/deblur-stats.qza -d newpath
cp newpath/*/data/stats.csv  data/stats.csv
rm -r newpath
