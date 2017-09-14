import numpy as np
import pickle
import pandas as pd

def m2i(m1, m2= None):
    if m2 == None:
        return [(m1 - 9)%12]
    return range((m1 - 9)%12, (m2 - 9)%12 + 1)

def i2b(ls, n):
    x = np.zeros(12)
    for index in ls:
        x[index] = 1
    for i in range(1, 12):
        x[i] = n*x[i-1] + x[i]
    return x

##
# initial balance fixed
#
ibfd = {'emilys checking and savings account': 10000,
        'davids checking and savings account': 10000,
        'mom and dad last semester fund':      4500
        }
init_bal = sum(ibfd.values())

# initial balance variable (YAGNI)

# savings fixed (YAGNI)

##
# savings variable
#
svd = {'two months rent': [4000, m2i(9,8)],
       'extra months rent': [2000, m2i(8)]
       }
with open('labels/svlabels', 'wb') as fp:
    pickle.dump(sorted(svd), fp)

def write_npy_matrix(filename, dictionary):
    matrix = np.matrix([i2b(dictionary[label][1], 0) for label in dictionary])
    np.save(filename + '.npy', matrix)

write_npy_matrix('svmx', svd)

##
# income fixed
#
ifd = {'northrop fall': [3000, m2i(9,11)],
       'northrop spring': [3000, m2i(1,8)]
       }
with open('labels/iflabels', 'wb') as fp:
    pickle.dump(sorted(svd), fp)

def write_csv_matrix(filename, dictionary):
    matrix = np.matrix([dictionary[label][0]*i2b(dictionary[label][1],0) for label in dictionary])
    matrix = np.vstack(([['sep','oct','nov','dec','jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug']], matrix))
    matrix = np.vstack(([init_bal]+sorted(dictionary),matrix.T)).T
    df = pd.DataFrame(matrix)
    df.to_csv(filename + ".csv")

write_csv_matrix('ifmx', ifd)

# income variable (YAGNI)

##
# expenses fixed
#
efd = {'gas and grocery': [1200, range(12)],
       'UCSB tuition': [4000, m2i(9) + m2i(1) + m2i(5)]
       }
with open('labels/eflabels', 'wb') as fp:
    pickle.dump(sorted(efd), fp)
write_csv_matrix('efmx', efd)

##
# expenses variable
#
evd = {'rent': [1300, m2i(11, 8)],
       'student loans': [0, range(12)],
       'vacation': [0, m2i(6) + m2i(8)],
       'eating out': [200, range(12)]
       }
with open('labels/evlabels', 'wb') as fp:
    pickle.dump(sorted(evd), fp)

write_npy_matrix('evmx', evd)

##
# A_ub
#

A_ub = np.array(i2b(evd[sorted(evd)[0]][1], 1))
for x in sorted(evd)[1:]:
    A_ub = np.vstack((A_ub, i2b(evd[x][1], 1)))
for x in sorted(svd):
    A_ub = np.vstack((A_ub, i2b(svd[x][1], 0)))
A_ub = A_ub.T
# write the file
np.save('linear_bounds/A_ub.npy', A_ub)

##
# b_ub
#

b_ub = np.full(12, init_bal, dtype=float)

for label in ifd:
    b_ub += ifd[label][0]*i2b(ifd[label][1], 1)
for label in efd:
    b_ub += efd[label][0] * i2b(efd[label][1], 1)
# write the file
np.save('linear_bounds/b_ub.npy', b_ub)

##
# bounds
#
bounds = [(evd[l][0], float('inf')) for l in sorted(evd)] + [(svd[l][0], float('inf')) for l in sorted(svd)]
# write the file
with open('linear_bounds/bounds.txt', 'w') as fp:
    fp.write('\n'.join('%s %s' % x for x in bounds))