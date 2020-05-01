#!/usr/bin/env python3
import argparse
import subprocess
import os
import numpy as np
import math
from scipy.special import comb

#parse args
parser = argparse.ArgumentParser(description="Given two phylogenetic trees, calculate the average squared error of the pairwise distances between leaves")
parser.add_argument("-t1", "--tree_1", required=True, help="Fist tree (newick)")
parser.add_argument("-t2", "--tree_2", required=True, help="Second tree (newick)")
parser.add_argument("-d", "--dists", action="store_true", default=False, help="save distance matrices as csv files in the current directory")
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

#remove temporary distance matrixes
if args.dists==False:
    os.remove("tree1dists.csv")
    os.remove("tree2dists.csv")

error = 0.0

#compute sum of squared error 
for strand1 in range(0, len(firstContents) - 1): 
    strand1Name = firstContents[strand1]
    for strand2 in range(strand1 + 1, len(firstContents)):
        strand2Name = firstContents[strand2]
        error += math.pow(firstMatrix[strand2][strand1] - secondMatrix[secondContents.index(strand2Name)][secondContents.index(strand1Name)], 2)

error = error/comb(len(firstContents), 2)
print("Mean Error Squared: ", end = "")
print(error)
