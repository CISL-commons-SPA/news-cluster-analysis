#!/bin/bash
python3 alternate_clustering_methods.py embedding_files/${1}.pkl clustering_data_labels/${1}_hdp_lda.pkl ${2}.pkl hdp-lda
python3 perform_visualization.py clustering_data_labels/${1}_hdp_lda.pkl y
python3 get_cluster_results.py clustering_data_labels/${1}_hdp_lda.pkl ${2}.pkl results_cluster/${1}_hdp_lda.jsonl