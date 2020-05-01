#!/usr/bin/env python3
import argparse
import subprocess
import os
import numpy as np
import math
from scipy.special import comb
from skbio.stats.distance import mantel

#parse args
parser = argparse.ArgumentParser(description="Given two phylogenetic trees, calculate a mantel correlation between their two pairwise distance matrices")
parser.add_argument("-t1", "--tree_1", required=True, help="Fist tree (newick)")
parser.add_argument("-t2", "--tree_2", required=True, help="Second tree (newick)")
parser.add_argument("-p", "--pearson", required=False, action="store_true",default=False, help="use pearson coefficient (uses spearman by default)")
parser.add_argument("-d", "--dists", required=False, action="store_true", default=False, help="save distance matrices as csv files in the current directory")
args = parser.parse_args()

#compute pairwise distances matrices of trees
subprocess.call(["./patristic_distances.py", 
    "-t", args.tree_1,
    "-o", "tree1dists.csv"])

subprocess.call(["./patristic_distances.py", 
    "-t", args.tree_2,
    "-o", "tree2dists.csv"])

distances1 = "tree1dists.csv"
distances2 = "tree2dists.csv"

#convert distance matrices into arrays
def intoArray(location):
    with open(location) as f:
        names = f.readline().split(",")
        ncols = len(names)
        return np.loadtxt(f, delimiter=",", usecols=range(1,ncols))

firstMatrix = intoArray(distances1)
firstContents = open(distances1).readline().split(",")
firstContents[len(firstContents) - 1] = firstContents[len(firstContents) - 1].strip()
del firstContents[0]

secondMatrix = intoArray(distances2)
secondContents = open(distances2).readline().split(",")
secondContents[len(secondContents) - 1] = secondContents[len(secondContents) - 1].strip()
del secondContents[0]

secondReordered = np.empty([len(secondContents) - 1,len(secondContents) - 1])

#reorder second matrix to be in the same order as first
for strand1 in range(0, len(firstContents)): 
    strand1Name = firstContents[strand1]
    for strand2 in range(0, len(firstContents)):
        strand2Name = firstContents[strand2]
        secondReordered[strand2][strand1] = secondMatrix[secondContents.index(strand2Name)][secondContents.index(strand1Name)]

#remove temporary distance matrixes
if args.dists==False:
    os.remove("tree1dists.csv")
    os.remove("tree2dists.csv")

#calculate mantel correlation
if args.pearson == True:
    coeff, p_value, n = mantel(firstMatrix, secondReordered, method="pearson", permutations=0)
    print("Pearson Correlation: %f" % coeff)
else:
    coeff, p_value, n = mantel(firstMatrix, secondReordered, method="spearman", permutations=0)
    print("Spearman Correlation: %f" % coeff)

print("p-Value: %f" % p_value)

