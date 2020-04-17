require(treedater)
tree <- ape::read.tree('/home/colin/Desktop/NiemaLab/testingViReport/Analysis/PhyloTools/FastTree/intermediate_files/treedater/rooted_unzipped.tre')
seqlen <- 19328
times_tab <- read.csv('/home/colin/Desktop/NiemaLab/testingViReport/Analysis/PhyloTools/FastTree/intermediate_files/treedater/times_treedater.txt', header=FALSE)
times <- setNames(times_tab[,2], times_tab[,1])
out <- dater(tree, times, seqlen, clock='uncorrelated', omega0=0.000000, numStartConditions=0)
write.tree(out, '/home/colin/Desktop/NiemaLab/testingViReport/Analysis/PhyloTools/FastTree/intermediate_files/treedater/dated.tre')
