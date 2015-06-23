import sys
import itertools
from operator import itemgetter
import math

def main(allfiles, outfile, base):
    files = open(allfiles, 'r')
    lines = files.readlines()
    entropies = []
    for infile in lines:
        raw = open(infile.strip(),'r')
        lines = raw.readlines()
        probs = []
        for line in lines:  
            parts = line.split('\t')
            node = int(parts[0])
            prob = float(parts[3].strip())
            if len(probs) >= node:
                probs[node-1].append(prob)
            else:
                probs.append([prob])
        entropy = 0
        for node in probs:
            for prob in node:
                if prob > 0:
                    entropy = entropy - prob*math.log(prob,base)
        group = infile.strip().split('_')[0]+'_'+infile.strip().split('_')[1]
        entropies.append(group + ',' + str(entropy) + '\n')
    outfile = open(outfile, 'w')
    for line in entropies:
        outfile.write(line)


if __name__ == "__main__": 
    allfiles = sys.argv[1]
    outfile = sys.argv[2]
    base = int(sys.argv[3])
    main(allfiles,outfile,base)