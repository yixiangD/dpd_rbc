#!/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import xlrd
import sys
import math

def read_xlsx(path):
    workbook = xlrd.open_workbook(path)
    second_sheet = workbook.sheet_by_index(1)
    row_start = 3
    koff0, sigma, steps, force, cate = [], [], [], [], []
    n_rows = second_sheet.nrows
    while row_start < n_rows:
        cells = second_sheet.row_slice(row_start, start_colx = 0, end_colx = 7)
        row_start += 1
        koff0.append(cells[0].value)
        sigma.append(cells[1].value)
        steps.append(cells[-2].value)
        if cells[-1].value > 0.5:
            cate.append('h')
        elif cells[-1].value > 0.2:
            cate.append('m')
        else:
            cate.append('l')
        force.append(cells[-1].value)
    return koff0, sigma, steps, force, cate

def plot():
    path = str(sys.argv[1])
    koff0, sigma, steps, force, cate = read_xlsx(path)

    fig1 = plt.figure()
    plt.hist(steps)
    plt.title('RBC detach histogram')
    plt.xlabel('steps')
    plt.ylabel('# of RBCs')
    plt.show()

    logkf = [math.log10(a) for a in koff0]
    df = pd.DataFrame(dict(logkf=logkf, sigma=sigma, cate=cate))
    colors = {'h': 'red', 'm': 'blue', 'l': 'green'}
    fig2, ax = plt.subplots()
    ax.scatter(df['logkf'],df['sigma'],c=df['cate'].apply(lambda x: colors[x]))
    plt.show()

def main():
    plot()

if __name__ == '__main__':
    main()
