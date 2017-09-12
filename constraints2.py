import numpy as np
import pickle

def m2i(m1, m2= None):
    if m2 == None:
        return [(m1 - 9)%12]
    return range((m1 - 9)%12, (m2 - 9)%12 + 1)

##
# initial balance fixed
#
ibfd = {'emilys checking and savings account': 10000,
        'davids checking and savings account': 5000,
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
svlabels = []
svvalues = []
for element in svd:
    svlabels.append(element)
    svvalues.append(svd[element])
with open('labels/svlabels', 'wb') as fp:
    pickle.dump(svlabels, fp)

##
# income fixed
#
ifd = {'northrop fall': [640, m2i(9,11)],
       'northrop spring': [800, m2i(1,8)]
       }
iflabels = []
ifvalues = []
for element in ifd:
    iflabels.append(element)
    ifvalues.append(ifd[element])
with open('labels/iflabels', 'wb') as fp:
    pickle.dump(iflabels, fp)

# income variable (YAGNI)

##
# expenses fixed
#
efd = {'gas and grocery': [1200, range(12)],
       'UCSB tuition': [4000, m2i(9) + m2i(1) + m2i(5)]
       }
eflabels = []
efvalues = []
for element in efd:
    eflabels.append(element)
    efvalues.append(efd[element])
with open('labels/eflabels', 'wb') as fp:
    pickle.dump(eflabels, fp)

##
# expenses variable
#
evd = {'rent': [1300, m2i(11, 8)],
       'student loans': [0, range(12)],
       'vacation': [0, m2i(6) + m2i(8)],
       'eating out': [200, range(12)]
       }
evlabels = []
evvalues = []
for element in evd:
    evlabels.append(element)
    evvalues.append(evd[element])
with open('labels/evlabels', 'wb') as fp:
    pickle.dump(evlabels, fp)

##
# A_ub
#

def i2b(ls, n):
    x = np.zeros(12)
    for index in ls:
        x[index] = 1
    for i in range(1, 12):
        x[i] = n*x[i-1] + x[i]
    return x

A_ub = np.array(i2b(evvalues[0][1], 1))
for x in evvalues[1:]:
    A_ub = np.vstack((A_ub, i2b(x[1], 1)))
for x in svvalues:
    A_ub = np.vstack((A_ub, i2b(x[1], 0)))
A_ub = A_ub.T
# write the file
np.save('linear_bounds/A_ub.npy', A_ub)

##
# b_ub
#

b_ub = np.full(12, init_bal, dtype=float)

for x in ifvalues:
    b_ub += x[0]*i2b(x[1], 1)
for x in efvalues:
    b_ub -= x[0]*i2b(x[1], 1)
# write the file
np.save('linear_bounds/b_ub.npy', b_ub)

##
# bounds
#
bounds = []
for x in evvalues + svvalues:
    bounds.append((x[0], float('inf')))
# write the file
with open('linear_bounds/bounds.txt', 'w') as fp:
    fp.write('\n'.join('%s %s' % x for x in bounds))