import numpy as np
import pickle
# import npy solutions
with open('evlabels', 'rb') as f:
    evlabel = pickle.load(f)
with open('svlabels', 'rb') as f:
    svlabel = pickle.load(f)
center = np.load('center.npy')

with open('linear_bounds/bounds.txt', 'r') as fp:
    bounds = [tuple(map(float, x.split())) for x in fp]

print()

print('epenses: \n')
for i in range(len(evlabel)):
    print('%-25s  $ %-6d: $ %-6d'%(evlabel[i], bounds[i][0], round(center[i],-1)))

print()

print('savings: \n')
for i in range(len(evlabel), len(evlabel) + len(svlabel)):
    print('%-25s  $ %-6d: $ %-6d' % (svlabel[i-len(evlabel)], bounds[i][0], round(center[i], -1)))