"""

"""
from devices.base_device import base_device
import system
from cvxopt.base import matrix, spmatrix, cos, sin, sparse, mul,exp
import cvxopt.blas
import math
import numpy as np


class line(base_device):
    def __init__(self):
        base_device.__init__(self)
        self._data.update({'fn': 50, 'f_bus': None, 'to_bus': None, 'l': 0,  'kT': 1, 'r': 2, 'x': 1.1, 'b': 1, 'tap_ratio': 1.1, 'theta': 0.1,
                           'Imax': 0, 'Pmax': 0, 'Smax': 0})
        self._type = 'Line'
        self._name = 'Line'
        self._bus = {'f_bus': ['af', 'vf'], 'to_bus': ['at', 'vt']}
        self._params.extend(['fn', 'kT', 'r', 'x', 'tap_ratio', 'theta', 'Imax', 'Pmax', 'Smax'])
        self.z = ['r', 'x']

    def adbus(self):

        for i in range(system.Sssc.n):
            if self.__dict__['f_bus'][int(system.Sssc.L[i])] == system.Sssc.bus[i]:
                self.__dict__['f_bus'][int(system.Sssc.L[i])] = 'Bus_' + str(system.Bus.n - system.Sssc.n + i + 1)
            if self.__dict__['to_bus'][int(system.Sssc.L[i])] == system.Sssc.bus[i]:
                self.__dict__['to_bus'][int(system.Sssc.L[i])] = 'Bus_' + str(system.Bus.n + i)

    def _bus_index(self):

        idx = []

        for index in self._bus.keys():

            for item in self.__dict__[index]:
                if not item in system.Bus.int:
                    continue
                    # self.message('Bus index <%s> does not exist', data_tuple = item, level = self.ERROR)
                else:
                    idx = system.Bus.int[item]
                    self.__dict__[self._bus[index][0]].append(system.Bus.a[idx])
                    self.__dict__[self._bus[index][1]].append(system.Bus.a[idx]+system.Bus.n)

    def build_y(self):

        for i in range(len(self.tap_ratio)):
            if self.tap_ratio[i] == 0:
                self.tap_ratio[i] = 1
        # print(self.tap_ratio)

        # chrg = np.mat(self.b) * 0.5
        # chrg = chrg.T
        #
        # print(chrg)
        chrg = np.array(np.zeros((len(self.b), 1), complex))
        for i in range(len(self.x)):
            chrg[i] = complex(0.0, self.b[i] * 0.5)

        #print(chrg)
        #zeros = [0] * len(self.x)
        #y = matrix(zeros, (len(self.x), 1, complex))
        y = np.array(np.zeros((len(self.x), 1), complex))
        for i in range(len(self.x)):
            y[i] = 1.0 / complex(self.r[i], self.x[i])
        #print(y)

        ts = np.array(np.zeros((len(self.theta), 1), complex))
        for i in range(len(self.theta)):
            ts[i] = complex(self.tap_ratio[i]*cos(self.theta[i]*math.pi/180), self.tap_ratio[i]*sin(self.theta[i]*math.pi/180))
        #print(ts)

        ts2 = ts * ts.conj()
        #print(ts2)

        y1 = -y / ts.conj()
        #print(y1)

        self.Y = spmatrix(y1, self.af, self.at, (system.Bus.n, system.Bus.n)) +\
            spmatrix(y1, self.at, self.af, (system.Bus.n, system.Bus.n)) +\
            spmatrix(y/ts2 + chrg, self.af, self.af, (system.Bus.n, system.Bus.n)) +\
            spmatrix(y + chrg, self.at, self.at, (system.Bus.n, system.Bus.n))
        system.DAE.Y = self.Y

        system.DAE.Y_G = self.Y.real()

        system.DAE.Y_B = self.Y.imag()
        print(system.DAE.Y_G)
        print(system.DAE.Y_B)




        # print(self.Y)
        # print(self.Y.V)

    def gcall(self):

        zeros = [0] * system.Bus.n
        Vn = zeros[:]
        Vc = zeros[:]
        for item1, item2 in zip(system.Bus.a, system.Bus.v):
            Vn[item1] = exp(system.DAE.y[item1] * 1j)
            Vc[item1] = (system.DAE.y[item2] + 0j) * Vn[item1]
        # system.DAE.y = matrix(system.DAE.y)
        # Vn = exp(system.DAE.y[system.Bus.a] * 1j)
        # Vc = mul(system.DAE.y[system.Bus.v] + 0j, Vn)
        Vc = matrix(Vc)
        Ic = self.Y * Vc
        S = mul(Vc, Ic.H.T)

        self.p = S.real()

        self.q = S.imag()

        for i in range(system.Bus.n):
             system.DAE.g[i] = self.p[i]
             system.DAE.g[i+system.Bus.n] = self.q[i]




    def Gycall(self):
        system.DAE.y=matrix(system.DAE.y)
        U=exp(system.DAE.y[system.Bus.a]*1j)
        V = mul(system.DAE.y[system.Bus.v] + 0j, U)
        I = self.Y * V
        nb=len(system.Bus.a)
        diagU=spmatrix(U,system.Bus.a,system.Bus.a,(nb,nb),'z')
        diagV = spmatrix(V, system.Bus.a, system.Bus.a, (nb, nb), 'z')
        diagI = spmatrix(I, system.Bus.a, system.Bus.a, (nb, nb), 'z')
        dS=self.Y*diagU

        dS=diagV*dS.H.T


        dS+=diagI.H.T*diagU
        dR=diagI
        dR=dR-self.Y*diagV

        dR=diagV.H.T*dR

        # system.DAE.Gy = matrix(0.0, (system.DAE.ny, system.DAE.ny))
        #
        # system.DAE._list2matrix()
        # system.DAE.Gy = spmatrix(dR.imag().V, dR.imag().I, dR.imag().J, (system.DAE.ny, system.DAE.ny)) \
        #                 + spmatrix(dR.real().V, dR.real().I, dR.real().J+system.Bus.n, (system.DAE.ny, system.DAE.ny)) \
        #                 + spmatrix(dS.real().V, dS.real().I+system.Bus.n, dS.real().J, (system.DAE.ny, system.DAE.ny)) \
        #                 + spmatrix(dS.imag().V, dS.imag().I+system.Bus.n, dS.imag().J+system.Bus.n, (system.DAE.ny, system.DAE.ny))


        Gy=sparse([[dR.imag(),dR.real()],[dS.real(),dS.imag()]])
        # system.DAE.Gy = zeros([system.DAE.ny,system.DAE.ny])
        system.DAE.Gy = spmatrix(Gy.V, Gy.I, Gy.J, (system.DAE.ny, system.DAE.ny))

        system.DAE.Gy = matrix(system.DAE.Gy)
        # print(Gy[0,0])



