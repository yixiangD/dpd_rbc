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

    def gen_coord_rect(self,center,halflen, tp, nparticles = 0):
        ### center: 3D list coordinates for rectangular box
        ### halflen: 3D list length inputs for this box
        ### tp: type value for the particles
        i = self.idstart
        while i < self.idstart + nparticles + 1:
            rdn = list(random.uniform(-1,1,3))
            rescale = [a*b + c for a,b,c in zip(halflen,rdn,center)]
            i += 1
            self.myid.append(i)
            self.mymol.append(0)
            self.mytp.append(tp)
            self.myq.append(0)
            self.x.append(rescale[0])
            self.y.append(rescale[1])
            self.z.append(rescale[2])
        self.idstart += nparticles
        self.totalpart += nparticles

    def gen_coord_ball(self,center,radius,tp,nparticles = 0):
        ### center: 3D list  coordinate for sphere
        ### tp: type value for the particles
        i = self.idstart
        while i < self.idstart + nparticles + 1:
            rdn = list(random.uniform(-1,1,3))
            vnorm = math.sqrt(sum([a**2 for a in rdn]))
            if vnorm < 1:
                rescale = [radius*a/vnorm + b for a,b in zip(rdn, center)]
                i += 1
                self.myid.append(i)
                self.mymol.append(0)
                self.mytp.append(tp)
                self.myq.append(0)
                self.x.append(rescale[0])
                self.y.append(rescale[1])
                self.z.append(rescale[2])
        self.idstart += nparticles
        self.totalpart += nparticles

    def write2file(self, outfile):
        #self.gen_coord(self.wallreg, self.walltp, self.wallpar)
        #self.gen_coord(self.outerreg, self.outertp, self.outerpar)
        #self.gen_coord(self.innerreg, self.innertp, self.innerpar)
        center = [20, 2.5, 10]
        halflen = [2, 0.5, 1.0]
        radius = 0.2
        self.gen_coord_rect(center,halflen,self.innertp, self.innerpar)
        #self.gen_coord_ball(center,radius,self.innertp, self.innerpar)
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
