#!/bin/bash

# 1. the embeddings produced, pkl file name without extension
# 2. linkage technique: average, single, complete
# 3. threshold distance: b/w 0 and 1
# 4. article_text / headlines pkl, filename w/o extension
# 5. y / n OR perform TSNE? 
# 6. driver_file (text file) name w/o extension
# 7. option: average, frequency, union, intersect
# 8. max num drivers you want per cluster

python3.7 alternate_clustering_methods.py embedding_files/${1}.pkl clustering_data_labels/${1}_${2}_${3}_heir.pkl ${2} heirarchy ${3}
python3.7 get_cluster_results.py clustering_data_labels/${1}_${2}_${3}_heir.pkl ${4}.pkl results_cluster/${1}_${2}_${3}_heir.jsonl
python3 semantic_scoring.py clustering_data_labels/${1}_${2}_${3}_heir.pkl cluster_semantic_scores/${1}_${2}_${3}_heir.jsonl
python3 do_driver_calls.py results_cluster/${1}_${2}_${3}_heir.jsonl ${6}.txt driver_lookups/${1}_${2}_${3}_heir_${7}_{8}.jsonl ${7} ${8}
python3.7 perform_visualization.py clustering_data_labels/${1}_${2}_${3}_heir.pkl ${5}