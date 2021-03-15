import pandas as pd

def reduce_taxonomy_df(taxonomy_table):
    taxonomy_red = taxonomy_table.drop(['Taxon', 'Confidence'], axis=1)
    return taxonomy_red

def make_taxon_list(taxonomy_red):
    """creates list of lists of each unique kingdom, phylum, class (etc) seen in the samples"""
    taxon_list = [[] for x in range(7)]
    for seq, row in taxonomy_red.iterrows():
        for i in range(0, 7) :
            if row.iloc[i] in taxon_list[i] :
                pass
            else:
                taxon_list[i].append(row.iloc[i])
    # returns list of lists
    # each list contains the unique families, phylums, etc (respectively) found in the data
    return taxon_list

def make_tax_dfs(taxon_list, feature_table):
    """creates empty dataframes with appropriate indexes and column names to fill for stacked taxonomy bar graphs"""
    kingdom_df =pd.DataFrame(0.0, columns=taxon_list[0], index=feature_table.index)
    phylum_df =pd.DataFrame(0.0, columns=taxon_list[1], index=feature_table.index)
    class_df =pd.DataFrame(0.0, columns=taxon_list[2], index=feature_table.index)
    order_df =pd.DataFrame(0.0, columns=taxon_list[3], index=feature_table.index)
    family_df =pd.DataFrame(0.0, columns=taxon_list[4], index=feature_table.index)
    genus_df =pd.DataFrame(0.0, columns=taxon_list[5], index=feature_table.index)
    species_df =pd.DataFrame(0.0, columns=taxon_list[6], index=feature_table.index)
    # returns empty (full of 0.0) dataframes for each taxonomy level, 
    # columns are different categories within each taxonomy level found in the data, indexes are the samples
    return kingdom_df, phylum_df, class_df, order_df, family_df, genus_df, species_df

# def fill_tax_dfs(kingdom_df, phylum_df, class_df, order_df, family_df, genus_df, species_df, feature_table, taxonomy_red):
#     """fills dataframes for each taxonomy level for creating stacked bar graph"""
#     for sample, row in feature_table.iterrows():
#         # iterate over feature table rows 
#         for featid in row.index:
#             # iterate over each feature id (sequence) in a sample and add appropriate prevalence to each taxonomy df
            
#             tax_list = taxonomy_red.loc[featid] # gets a list of the corresponding kingdom, phylum, etc for the feature id
#             kingdom_df[tax_list[0]][sample] += feature_table.loc[sample][featid] / 100
#             phylum_df.loc[sample][tax_list[1]] += feature_table.loc[sample][featid] / 100
#             class_df.loc[sample][tax_list[2]] += feature_table.loc[sample][featid] / 100
#             order_df.loc[sample][tax_list[3]] += feature_table.loc[sample][featid] / 100
#             family_df.loc[sample][tax_list[4]] += feature_table.loc[sample][featid] / 100
#             genus_df.loc[sample][tax_list[5]] += feature_table.loc[sample][featid] / 100
#             species_df.loc[sample][tax_list[6]] += feature_table.loc[sample][featid] / 100
#     # return the filled dataframes for each taxonomy level
#     return kingdom_df, phylum_df, class_df, order_df, family_df, genus_df, species_df

def fill_tax_dfs(kingdom_df, phylum_df, class_df, order_df, family_df, genus_df, species_df, feature_table, taxonomy_red):
    """fills dataframes for each taxonomy level for creating stacked bar graph"""
    for sample, row in feature_table.iterrows():
        # iterate over feature table rows 
        for featid in row.index:
            # iterate over each feature id (sequence) in a sample and add appropriate prevalence to each taxonomy df
            if featid in taxonomy_red.index:
                tax_list = taxonomy_red.loc[featid] # gets a list of the corresponding kingdom, phylum, etc for the feature id
                kingdom_df[tax_list[0]][sample] += feature_table.loc[sample][featid] / 100
                phylum_df.loc[sample][tax_list[1]] += feature_table.loc[sample][featid] / 100
                class_df.loc[sample][tax_list[2]] += feature_table.loc[sample][featid] / 100
                order_df.loc[sample][tax_list[3]] += feature_table.loc[sample][featid] / 100
                family_df.loc[sample][tax_list[4]] += feature_table.loc[sample][featid] / 100
                genus_df.loc[sample][tax_list[5]] += feature_table.loc[sample][featid] / 100
                species_df.loc[sample][tax_list[6]] += feature_table.loc[sample][featid] / 100
            else:
                pass
    # return the filled dataframes for each taxonomy level
    return kingdom_df, phylum_df, class_df, order_df, family_df, genus_df, species_df

def prepare_data_stacked_barplots(feature_table, taxonomy_table):
    taxonomy_red = reduce_taxonomy_df(taxonomy_table)
    taxon_list = make_taxon_list(taxonomy_red)
    kingdom_df_0, phylum_df_0, class_df_0, order_df_0, family_df_0, genus_df_0, species_df_0 = make_tax_dfs(taxon_list, feature_table)
    kingdom_df, phylum_df, class_df, order_df, family_df, genus_df, species_df = fill_tax_dfs(kingdom_df_0, phylum_df_0, class_df_0, order_df_0, 
                                                                                              family_df_0, genus_df_0, species_df_0, feature_table, taxonomy_red)
    return kingdom_df, phylum_df, class_df, order_df, family_df, genus_df, species_df 
