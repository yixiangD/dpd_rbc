#!/bin/Python3

import re
import math

def ReadLammpsInData(filename):
    """
       1st arg: filename in string format
       2nd arg: entity to be checked out, available: Atoms,Bonds,
       Angles, Dihedrals, Types, Boxinfo
    """
    mylist = ['Atoms','Bonds','Angles', 'Dihedrals', 'Types', 'Boxinfo']
    #if entity not in mylist:
    #    raise ValueError('Invalid input')
    with open(filename) as infile:
        text = infile.readlines()
        n = 0
        Total, Boxinfo= [], []
        Types, Nums = {}, {}
        for x in text:
            newx = x.strip('\n')
            if newx:
                n += 1
                arr = re.split(r'[\t,\s]',newx)
                arr = list(filter(bool,arr))  # to filter empty strins
                Total.append(arr)
                if len(arr) == 2 and arr[1].isalpha() and not arr[0].isalpha():
                    name = str(arr[1])
                    Nums[name] = int(arr[0])
                if len(arr) > 2 and arr[1].isalpha() and not arr[0].isalpha():
                    name = '_'.join(arr[1:])
                    Types[name] = int(arr[0])
                if len(arr) == 4 and arr[-1].isalpha():
                    Boxinfo.append(float(arr[0]))
                    Boxinfo.append(float(arr[1]))
                if arr[0].isalpha():
                    if arr[0] == 'Atoms':
                        a = Total.index(arr)
                    if arr[0] == 'Bonds':
                        b = Total.index(arr)
                    if arr[0] == 'Angles':
                        c = Total.index(arr)
                    if arr[0] == 'Dihedrals':
                        d = Total.index(arr)
        Atoms, Bonds, Angles, Dihedrals = [], [], [], []
        mymap(Total[a+1:a+1+Nums['atoms']],Atoms)
        mymap(Total[b+1:b+1+Nums['bonds']],Bonds)
        mymap(Total[c+1:c+1+Nums['angles']],Angles)
        mymap(Total[d+1:d+1+Nums['dihedrals']],Dihedrals)
        return Atoms, Bonds, Angles, Dihedrals, Nums, Types, Boxinfo

#below function under construction
def ReadDumpFile(filename):
    with open(filename) as infile:
        test = infile.readlines()
    for things in test:
        newthings = things.strip('\n')
        arr = re.split('\s',newthings)
        print(arr)

def mymap(oldarray,newarray):
    for items in oldarray:
        f1 = map(int,filter(lambda x: type(eval(x)) == int, items))
        f2 = map(float,filter(lambda x: type(eval(x)) == float, items))
        newarray.append(list(f1) + list(f2))

def main():
    f = '../data/input/500cells/Nv500_elongated.cell'
    #f = '../data/input/2000_centered/elongated.data'
    filename = '../data/input/temp/dump_rbc.lammpstrj'
    ReadDumpFile(filename)

if __name__ == "__main__":
    main()

    #file1 = '../data/input/2000_centered/healthy.data'
    #print(ReadLammpsInData.__doc__)
    #atoms = ReadLammpsInData(file1, 1, 1)
    #print(atoms)

