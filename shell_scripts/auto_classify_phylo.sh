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
  --p-sampling-depth $1 \
  --m-metadata-file metadata/$2 \
  --output-dir outputs/core-metrics-results

unzip -q outputs/taxonomy.qza -d newpath
cp newpath/*/data/taxonomy.tsv data/taxonomy.tsv
rm -r newpath

unzip -q outputs/table.qza -d newpath
cp newpath/*/data/feature-table.biom data/feature-table.biom
rm -r newpath

unzip -q outputs/stats-dada2.qza -d newpath
cp newpath/*/data/stats.tsv  data/stats.tsv
rm -r newpath

unzip -q outputs/core-metrics-results/shannon_vector.qza -d newpath
mv newpath/*/data/alpha-diversity.tsv data/shannon-alpha-diversity.tsv
mv newpath/*/provenance/action/metadata.tsv data/metadata.tsv
rm -r newpath

unzip -q outputs/core-metrics-results/faith_pd_vector.qza -d newpath
mv newpath/*/data/alpha-diversity.tsv data/faith-alpha-diversity.tsv
rm -r newpath

unzip -q outputs/core-metrics-results/evenness_vector.qza -d newpath
mv newpath/*/data/alpha-diversity.tsv data/pielou-alpha-diversity.tsv
rm -r newpath

unzip -q outputs/core-metrics-results/observed_features_vector.qza -d newpath
mv newpath/*/data/alpha-diversity.tsv data/observed-features-alpha-diversity.tsv
rm -r newpath

unzip -q outputs/core-metrics-results/bray_curtis_distance_matrix.qza -d newpath
mv newpath/*/data/distance-matrix.tsv data/bray-distance-matrix.tsv
rm -r newpath

unzip -q outputs/core-metrics-results/weighted_unifrac_distance_matrix.qza -d newpath
mv newpath/*/data/distance-matrix.tsv data/unifrac_distance_matrix.tsv
rm -r newpath