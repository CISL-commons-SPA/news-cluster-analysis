#!/bin/bash
python3 alternate_clustering_methods.py embedding_files/${1}.pkl clustering_data_labels/${1}_lda_${2}.pkl ${3}.pkl lda ${2}
python3 perform_visualization.py clustering_data_labels/${1}_lda_${2}.pkl y
python3 get_cluster_results.py clustering_data_labels/${1}_lda_${2}.pkl ${3}.pkl results_cluster/${1}_lda_${2}.jsonl