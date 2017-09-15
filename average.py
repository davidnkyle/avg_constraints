import numpy as np
import scipy.optimize as opt
import pandas as pd
import pickle

# read in linear_bounds data
with open('linear_bounds/bounds.txt', 'r') as fp:
    bounds = [tuple(map(float, x.split())) for x in fp]
A_ub = np.load('linear_bounds/A_ub.npy')
b_ub = np.load('linear_bounds/b_ub.npy')

number_of_variables = len(A_ub[1,:])

status = opt.linprog([1]*number_of_variables, A_ub, b_ub, bounds=bounds).status
if(status == 2):
    print('infeasible')
elif status == 0:
    cube_low = []
    cube_high = []
    for i in range(number_of_variables):
        c_min = [0 for i in range(number_of_variables)]
        c_max = [0 for i in range(number_of_variables)]
        c_min[i] = 1
        c_max[i] = -1
        cube_low.append(opt.linprog(c_min, A_ub, b_ub, bounds=bounds).x[i])
        cube_high.append(opt.linprog(c_max, A_ub, b_ub, bounds=bounds).x[i])

    def find_center(A_ub, b_ub, cube_low, cube_high, iterations):
        total = np.zeros(number_of_variables)
        success = 0
        for i in range(iterations):
            x = np.random.uniform(cube_low, cube_high, number_of_variables)
            if all(A_ub.dot(x) <= b_ub):
                total += x
                success += 1
        if success > 100:
            return total/success
        raise(Exception('not a big enough sample size'))

    center = find_center(A_ub, b_ub, cube_low, cube_high, 100000)
    np.save('center.npy', center)

    # savings files
    def write_csv_matrix2(importname, labelname, exportname):
        with open(labelname, 'rb') as f:
            lab = pickle.load(f)
        mx = np.load('solution_npy/'+importname + '.npy')
        mx = (mx.T * center[:mx.shape[0]]).T
        mx = np.vstack(([['sep', 'oct', 'nov', 'dec', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug']], mx))
        mx = np.vstack(([0] + lab, mx.T)).T
        df = pd.DataFrame(mx)
        df.to_csv('solution_csv/'+exportname + ".csv")

    write_csv_matrix2('evmx', 'evlabels', 'evmx')
    write_csv_matrix2('svmx', 'svlabels', 'svmx')


