import os
import sys
import pandas as bananas
import numpy as np
import argparse
import csv

def initialize():

	parser = argparse.ArgumentParser(
	             description='arguments',
	             prog='input arg')
	parser.add_argument('--gene_counts_file', type=str, help='name of file')
	parser.add_argument('--sample_atributes_file', type=str, help='da groups')
	parser.add_argument('--gene', type=str, help='name of gene')
	parser.add_argument('--output_file', type=str, help='name of output_file')

	args = parser.parse_args()
	return args

def pull_gene_reads(gene_counts_file, gene):
    df = bananas.read_table(gene_counts_file, header=2)
    df1 = df.drop('Name', axis=1)
    df2 = df1.set_index('Description')
    gene_counts = df2.loc[[gene]]
    return gene_counts

def pull_tissue_type(sample_atributes_file,tissue_group):
    df = bananas.read_table(sample_atributes_file, header=0)
    tissues = df[tissue_group]
    sampIDs = df['SAMPID']
    arrayconc = bananas.concat([tissues,sampIDs],axis=1)
    grouped = arrayconc.groupby(tissue_group)['SAMPID']
    unique_tissues = tissues.unique()
    df_array = bananas.DataFrame()
    for i in range(0, len(unique_tissues)):
        current_sample_IDs = grouped.get_group(unique_tissues[i])
        current_sample_IDs_list = current_sample_IDs.to_list()
        current_headder = unique_tissues[i]
        current_df = bananas.DataFrame({current_headder: current_sample_IDs})
        df_array = df_array.append(current_df)
    return df_array

	#test = arrayconc.groupby(tissue_group)['SAMPID']
	# test = arrayconc.groupby(['SMTS','SAMPID'])
	# test1 = df.groupby(['SMTS'])['SAMPID'].apply(list).groupby(level=0).apply(list)

	# list1 = test1
	# str1 = ''.join(str(e) for e in list1)
	# test2 = map(''.join, str1)

	# with open("testcase2.csv", "w", newline="") as f:
	# 	writer = csv.writer(f)
	# 	writer.writerows(test2)

	#wtr = csv.writer(open('test1.csv','w'),delimiter = ',',lineterminator='\n')
	#for x in test1 : wtr.writerow([x])


def main():
    args = initialize()
    df = pull_gene_reads(args.gene_counts_file, args.gene)
    df.to_csv(args.output_file)

    df1 = pull_tissue_type(args.sample_atributes_file, 'SMTS')

    df1.to_csv('testcase3.csv')

if __name__ == '__main__':
	main()