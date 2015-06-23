import sys
import itertools
from operator import itemgetter

def main(infile, outfile, limit):
    fo = open(outfile, "w")
    probs, chars = read_data(infile)
    
    n = len(probs)

    top = []
    candidates = []
    soon = dict()

    first = [0]*n
    top.append((first,prob_product(probs,first)))

    for i in range(n):
        can = [0]*n
        if len(probs[i]) > 1:
            can[i] = 1
            candidates.append((can,prob_product(probs,can)))

    fo.write("Rank,Inds,Seq,Prob\n")

    for i in range(1,limit):
        next = max(candidates,key=itemgetter(1))
        candidates.remove(next)
        top.append(next)
        (candidates,soon) = update(candidates,soon,probs,next)
    for ind,dup in enumerate(top):
        fo.write(str(ind+1)+','+str(dup[0])+','+get_sequence(dup[0],chars)+','+str(dup[1])+'\n')
    fo.close()

def prob_product(probs,inds):
    out = 1
    for ind,i in enumerate(inds):
    	node = probs[ind]
    	prob = node[i]
        out = out*prob
    return out

def update(candidates,soon,probs,next):
    inds = next[0]
    for i in range(len(inds)):
        soon_inds = list(inds)
        soon_inds[i] += 1
        key = str(soon_inds)
        if key in soon:
            parents = soon[key]
            parents[i] = True
            soon[key] =  parents
        else:
            parents = [False]*len(inds)
            parents[i] = True
            for j,ind in enumerate(soon_inds):
                if ind == 0:
                    parents[j] = True
            soon[key] =  parents
        if parents.count(False) == 0:
                candidates.append((soon_inds,prob_product(probs,soon_inds)))
                del soon[key]
    return (candidates,soon)

def get_sequence(nums,chars):
    size = len(nums)
    seq = chars[0][nums[0]]
    for i in range(1,size):
        j = nums[i]
        seq = seq.replace('&',chars[i][j])
    seq = seq.replace('&','')
    return seq

def read_data(filename):
    with open(filename, 'r') as raw:
        lines = raw.readlines()
        probs = []
        chars = []
        for line in lines:
            parts = line.split('\t')
            node = int(parts[0])
            prob = float(parts[3].strip())
            if len(probs) >= node:
                probs[node-1].append(prob)
                chars[node-1].append(parts[1] + '&' + parts[2])
            else:
                probs.append([prob])
                chars.append([parts[1] + '&' + parts[2]])
        return (probs,chars)

if __name__ == "__main__": 
    infile = sys.argv[1]
    outfile = sys.argv[2]
    limit = int(sys.argv[3])
    main(infile,outfile,limit)