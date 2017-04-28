from ReadLmp import ReadLammpsInData
import math
import numpy as np
import time

class ComposeData():
    #matoms,mbonds,mangles,mdihedrals = 500,1494,996,1494
    matoms,mbonds,mangles,mdihedrals = 2000,5994,3996,5994

    def __init__(self, infile):
        print('Make sure your input data file start with "LAMMPS" and a blank line')
        self.fname = infile
        self.atoms, self.bonds, self.angles,\
                self.dihedrals, self.nums, self.types, self.box =\
                ReadLammpsInData(infile)
        self.nrbc = 0
        self.newbox = [0,40,0,12,0,20]
        self.sort = 0
        #self.newbox = [-15,15,-12,12,-12,12]

    # change atoms's order, bonds and dihedrals!
    def AddRBC(self,RBC):
        self.nrbc += 1
        print(self.nrbc)
        for i in RBC.atoms:
            i[0] += self.nums['atoms']
            i[1] += self.nrbc
            self.atoms.append(i)
        for i in RBC.bonds:
            i[0] += self.nums['bonds']
            i[2] += self.nums['atoms']
            i[3] += self.nums['atoms']
            self.bonds.append(i)
        for i in RBC.angles:
            i[0] += self.nums['angles']
            i[2] += self.nums['atoms']
            i[3] += self.nums['atoms']
            i[4] += self.nums['atoms']
            self.angles.append(i)
        for i in RBC.dihedrals:
            i[0] += self.nums['dihedrals']
            i[2] += self.nums['atoms']
            i[3] += self.nums['atoms']
            i[4] += self.nums['atoms']
            i[5] += self.nums['atoms']
            self.dihedrals.append(i)
        for items in self.nums:
            self.nums[items] += RBC.nums[items]
        for items in self.types:
            self.types[items] = max(self.types[items], RBC.types[items])

    def Rotate(self, direct, theta = math.pi * 0.5):
        """ start with a single direction x, and then extend to other direction"""
        dic = {'x': -3, 'y': -2, 'z': -1}
        R = [[math.cos(theta), -math.sin(theta)],\
                [math.sin(theta),math.cos(theta)]]
        for items in R:
            print(items[0],'\t', items[1])
        #print('Rotation matrix:',R)
        if direct == 'x':
            d1, d2 = dic['y'], dic['z']
        elif direct == 'y':
            d1, d2 = dic['x'], dic['z']
        elif direct == 'z':
            d1, d2 = dic['x'], dic['y']
        for i in self.atoms:
            temp1, temp2 = i[d1], i[d2]
            i[d1], i[d2] = R[0][0]*temp1 + R[0][1]*temp2, R[1][0]*temp1 + \
                    R[1][1]*temp2

    def Translate(self, x = 0, y = 0, z = 0):
        coord = [x,y,z]
        for items in self.atoms:
            for i in range(-1,-4,-1):
                items[i] = float(items[i]) + coord[i]

    def SortAtoms(self):
        self.sort = 1
        self.atoms = sorted(self.atoms, key = lambda l:l[0])

    def UpdateBonds(self):
        if self.sort == 0:
            self.SortAtoms()
        for x in self.bonds:
            i1 = x[2]
            i2 = x[3]
            x1 = self.atoms[i1 - 1][1:]
            x2 = self.atoms[i2 - 1][1:]
            dxsq = sum([(a - b)**2 for a,b in zip(x1,x2)])
            dx = math.sqrt(dxsq)
            x[-1] = dx

    def UpdateAngles(self):
        if self.sort == 0:
            SortAtoms()
        for items in self.angles:
            i1 = items[2]
            i2 = items[3]
            i3 = items[4]
            x1 = self.atoms[i1 - 1][1:]
            x2 = self.atoms[i2 - 1][1:]
            x3 = self.atoms[i3 - 1][1:]
            dx21 = [a - b for a,b in zip(x1,x2)]
            dx23 = [a - b for a,b in zip(x3,x2)]
            dx13 = [a - b for a,b in zip(x3,x1)]
            ldx21 = math.sqrt(sum([i**2 for i in dx21]))
            ldx23 = math.sqrt(sum([i**2 for i in dx23]))
            ldx13 = math.sqrt(sum([i**2 for i in dx13]))
            p = 0.5*(ldx21 + ldx23 + ldx13)
            S = math.sqrt(p*(p-ldx21)*(p-ldx13)*(p-ldx23))
            items[-1] = S

    def Write2File(self, outfile):
        out = open(outfile,'w')
        out.write('LAMMPS\n\n')
        out.write(str(self.nums['atoms']) + ' atoms\n')
        out.write(str(self.nums['bonds']) + ' bonds\n')
        out.write(str(self.nums['angles']) + ' angles\n')
        out.write(str(self.nums['dihedrals']) + ' dihedrals\n')
        out.write(str(self.nums['impropers']) + ' impropers\n\n')

        out.write(str(self.types['atom_types']) + ' atom types\n')
        out.write(str(self.types['bond_types']) + ' bond types\n')
        out.write(str(self.types['angle_types']) + ' angle types\n')
        out.write(str(self.types['dihedral_types']) + ' dihedral types\n\n')

        out.write(str(self.newbox[0]) + ' ' + \
                str(self.newbox[1]) + ' xlo xhi\n')
        out.write(str(self.newbox[2]) + ' ' + \
                str(self.newbox[3]) + ' ylo yhi\n')
        out.write(str(self.newbox[4]) + ' ' + \
                str(self.newbox[5]) + ' zlo zhi\n\n')

        out.write('Masses\n\n')
        for i in range(self.types['atom_types']):
            out.write(str(i+1) + ' 1.0\n')
        out.write('\n')

        out.write('Atoms\n\n')
        self.SecWrite(out,self.atoms)
        out.write('Bonds\n\n')
        self.SecWrite(out,self.bonds)
        out.write('Angles\n\n')
        self.SecWrite(out,self.angles)
        out.write('Dihedrals\n\n')
        self.SecWrite(out,self.dihedrals)

    def SecWrite(self,out,section):
        for i in section:
            string = ' '.join([str(terms) for terms in i]) + '\n'
            out.write(string)
        out.write('\n')

    def GetID(self, n = 1, d = 'x', opt = 0):
        # the dimension here denotes the dimension of the column, usually use
        # -3: x, -2: y, -1: z
        dic = {'x':-3, 'y':-2, 'z':-1}
        dim = dic[d]
        if opt == 0:
            atom_dir = sorted(self.atoms, key=lambda x:x[dim])
        else:
            atom_dir = sorted(self.atoms, key=lambda x:x[dim], reverse = True)
        return atom_dir[:n]

def main():
    file1 = '../data/input/2000_centered/healthy.data'
    #file2 = '../data/input/2000_centered/granular.data'
    #f = '../data/input/500_centered/xelongated.data'
    #rbc = ComposeData(f)
    rbc = ComposeData(file1)
    rbc.SortAtoms()
    rbc.UpdateBonds()
    rbc.UpdateAngles()
    rbc.Translate(20,2.5,10)

    #rbc.nums['atoms'] = 29300
    #rbc.nums['atoms'] = 30800
    outfile = '../data/output/test.data'
    rbc.Write2File(outfile)

if __name__ == '__main__':
    main()
