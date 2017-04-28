#!/bin/python3

''' a script used to generate random particles' coordinate given
number of density at 3'''
from numpy import random
from numpy import genfromtxt
import re
import math

class dpd_fluid:
    nden = 3

    def __init__(self):
        # primary for dpd/full: id mol type q x y z
        self.walltp = 4
        self.outertp = 5
        self.innertp = 7
        self.idstart = 2000 # the starting value of id
        self.totalpart = 0
        self.x, self.y, self.z = [], [], []
        self.myid, self.mymol, self.mytp, self.myq =  [], [], [], []
        self.wallreg = [0,40,0,1,0,20]
        self.outerreg = [0,40,5,12,0,20]
        self.innerreg = [19.5,21.5,2.2,2.3,7.5,9.5]
        # volume section can be further improved
        self.boxv = 40*12*20
        self.wallv = 40*20
        self.rbcv = 94 # which is fixed
        self.outerpar = dpd_fluid.nden*(self.boxv - self.wallv - self.rbcv)
        self.innerpar = dpd_fluid.nden*self.rbcv
        self.wallpar = dpd_fluid.nden*self.wallv

    def gen_coord(self,arr,tp,nparticles = 0):
        # a function used to generate coordinates
        if nparticles == 0:
            nparticles = int(abs((arr[1]-arr[0])*(arr[3]-arr[2])*(arr[5]\
                    -arr[4]))*dpd_fluid.nden)
        for i in range(self.idstart + 1,self.idstart + nparticles + 1):
            self.myid.append(i)
            self.mymol.append(0)
            self.mytp.append(tp)
            self.myq.append(0)
            self.x.append(random.uniform(arr[0],arr[1],1)[0])
            self.y.append(random.uniform(arr[2],arr[3],1)[0])
            self.z.append(random.uniform(arr[4],arr[5],1)[0])
        self.idstart += nparticles
        self.totalpart += nparticles

    def write2file(self, outfile):
        self.gen_coord(self.wallreg, self.walltp, self.wallpar)
        self.gen_coord(self.outerreg, self.outertp, self.outerpar)
        self.gen_coord(self.innerreg, self.innertp, self.innerpar)
        print(self.totalpart)
        for i in range(self.totalpart):
            arr = ' '.join(map(str,[self.myid[i], self.mymol[i], self.mytp[i],\
                    self.myq[i], self.x[i],self.y[i],self.z[i]]))
            arr += '\n'
            outfile.write(arr)

def main():
    of = open('../data/output/test.txt','w')
    fluid = dpd_fluid()
    fluid.write2file(of)
    of.close()
#    ifile = 'coord.txt'
#    read_file(ifile)

def read_file(infile):
    data = genfromtxt(infile,dtype = None)
    for i in range(len(data)):
        data[i][0] += 8000
        data[i][2] = 3
    of = open('newfluid.data','w')
    for item in data:
        arr = ' '.join(map(str,item))
        arr += '\n'
        of.write(arr)
    of.close()

if __name__ == '__main__':
    main()
