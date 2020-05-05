#!/bin/bash

# 1. the embeddings produced, pkl file name without extension
# 2. eps: distance threshold, b/w 0 and 1
# 3. min_density: min pts to allow composition into a cluster within eps distance
# 4. article_text / headlines pkl, filename w/o extension
# 5. y / n OR perform TSNE? 
# 6. driver_file (text file) name w/o extension
# 7. option: average, frequency, union, intersect
# 8. max num drivers you want per cluster

# python3.7 read_and_cluster.py news_data/${1}.pkl embedding_files/${1}_${2}.pkl ${2}
python3.7 alternate_clustering_methods.py embedding_files/${1}_${2}.pkl clustering_data_labels/${1}_${2}_${3}_${4}_dbscan.pkl ${3} dbscan ${4}
python3.7 perform_visualization.py clustering_data_labels/${1}_${2}_${3}_${4}_dbscan.pkl ${6}
python3.7 get_cluster_results.py clustering_data_labels/${1}_${2}_${3}_${4}_dbscan.pkl ${5}.pkl results_cluster/${1}_${2}_${3}_${4}_dbscan.jsonl
python3.7 semantic_scoring.py clustering_data_labels/${1}_${2}_${3}_${4}_dbscan.pkl cluster_semantic_scores/${1}_${2}_${3}_${4}_dbscan.jsonl
python3.7 do_driver_calls.py results_cluster/${1}_${2}_${3}_${4}_dbscan.jsonl ${7}.txt driver_lookups/${1}_${2}_${3}_${4}_dbscan_${8}_${9}.jsonl ${8} ${9}
