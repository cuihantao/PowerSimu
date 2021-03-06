"""

"""
import system
from devices.base_device import base_device
from cvxopt.base import mul, matrix, exp, div, sin, cos, spmatrix
import numpy as np

class syn2():
    def __init__(self):
        return


class syn3():
    def __init__(self):
        return


class syn4():
    def __init__(self):
        return


class syn5a():
    def __init__(self):
        return


class syn5b():
    def __init__(self):
        return


class syn5c():
    def __init__(self):
        return


class syn5d():
    def __init__(self):
        return


class syn6a(base_device):
    def __init__(self):

        base_device.__init__(self)
        self._data.update({'bus': None, 'fn': 50, 'm_model': 6, 'xl': 0, 'ra': 0, 'xd': 0, 'xd1': 0, 'xd2': 0,
                          'Td01': 0, 'Td02': 0, 'xq': 0, 'xq1': 0, 'xq2': 0, 'Tq01': 0, 'Tq02': 0, 'M': 0, 'D': 0})
        self._type = 'Syn6'
        self._name = 'Syn6'
        self._bus = {'bus': ['a', 'v']}
        self._algebs = ['Va', 'V0']
        self._states = ['delta', 'omega', 'e1q', 'e1d', 'e2q', 'e2d']
        self._params.extend(['fn', 'xl', 'ra', 'xd', 'xd1', 'xd2', 'Td01', 'Td02',
                             'xq', 'xq1', 'xq2', 'Tq01', 'Tq02', 'M', 'D'])
        self._voltages = ['V0']  # 后续得修改
        self._powers = ['Pg']    # 后续得修改




class syn6b():
    def __init__(self):
        return

class syn6(base_device):
    def __init__(self):

        base_device.__init__(self)

        self._data.update(
            {'bus': None, 'fn': 50, 'm_model': 6, 'xl': 0, 'ra': 0, 'xd': 1.9, 'xd1': 0.302, 'xd2': 0,
             'Td01': 0, 'Td02': 0, 'xq': 0, 'xq1': 0, 'xq2': 0, 'Tq01': 0, 'Tq02': 0, 'M': 10,
             'D': 0, 'pm0': 0, 'vf0': 0, 'J11': 0, 'J12': 0, 'J21': 0, 'J22': 0, 'Komega': 0,
             'KP': 0, 'ganmaP': 1, 'ganmaQ': 1, 'Taa': 0, 'S10': 0, 'S12': 0, 'nCOI': 0})
        self._type = 'Syn6'
        self._name = 'Syn6'
        self._bus = {'bus': ['a', 'v']}
        self._algebs = ['vf', 'pm', 'p', 'q']
        self._states = ['delta', 'omega', 'e1q', 'e1d', 'e2q', 'e2d']
        self._params.extend(['fn', 'xl', 'ra', 'xd', 'xd1', 'xd2', 'Td01', 'Td02',
                             'xq', 'xq1', 'xq2', 'Tq01', 'Tq02', 'M', 'D', 'u', 'ganmaP', 'ganmaQ',
                             'Taa', 'S10', 'S12', 'pm0', 'vf0', 'J11', 'J12', 'J21', 'J22', 'Komega',
                             'KP', 'nCOI', 'vf'])
        self._z = ['xl', 'ra', 'xd', 'xd1', 'xd2', 'xq', 'xq1', 'xq2']
        self._powers = ['M', 'D']    # 后续得修改

    def setx0(self):


        # 常数
        self.c1 = [0] * self.n
        self.c2 = [0] * self.n
        self.c3 = [0] * self.n

        # 检查参数
        for i in range(self.n):
            # 检查惯性 M 和 x'd
            if self.M[i] <= 0:
                self.M[i] = 10
                print('%i 惯性M不能小于等于0，设置M = 10 [kWs/kVa]' % i)
            if self.xd1[i] <= 0:
                self.xd1[i] = 0.302
                print("%i x'd不能小于等于0，设置x'd = 0.302 [p.u.]" % i)

            # 检查 xd, T'd0
            if self.xd[i] <= 0:
                self.xd[i] = 1.9
                print("%i xd不能小于等于0，设置xd = 1.9 [p.u.]" % i)
            if self.Td01[i] <= 0:
                self.Td01[i] = 8
                print("%i T'd0不能小于等于0，设置T'd0 = 8 [s]" % i)

            # 检查 T''d0, x''d 和 x''q
            if self.Td02[i] <= 0:
                self.Td02[i] = 0.04
                print("%i T''d0不能小于等于0，设置T''d0 = 0.04 [s]" % i)
            if self.xd2[i] <= 0:
                self.xd2[i] = 0.204
                print("%i xd2不能小于等于0，设置xd2= 0.204 [p.u.]" % i)
            if self.xq2[i] <= 0:
                self.xq2[i] = 0.30
                print("%i xq2不能小于等于0，设置xq2= 0.30 [p.u.]" % i)

            # 检查 T'q0
            if self.Tq01[i] <= 0:
                self.Tq01[i] = 0.80
                print("%i T'q0不能小于等于0，设置T'q0 = 0.80 [s]" % i)

            # 检查 T''q0
            if self.Tq02[i] <= 0:
                self.Tq02[i] = 0.02
                print("%i T''q0不能小于等于0，设置T''q0 = 0.02 [s]" % i)

            # 检查 xq x'q
            if self.xq[i] <= 0:
                self.xq[i] = 1.70
                print("%i xq不能小于等于0，设置xq = 1.70 [p.u.]" % i)
            if self.xq1[i] <= 0:
                self.xq1[i] = 0.5
                print("%i xq1不能小于等于0，设置xq1 = 0.5 [p.u.]" % i)

            # 检查Taa和饱和因子

        # 转子速度



        system.DAE._list2matrix()

        system.DAE.x[self.omega] = self.u

        # 检查有功、无功比例
        # idx = []
        # for i in self.a:
        #     for index, j in enumerate(self.a):
        #         if j == i:
        #             idx.append(i)
        #     if len(idx) == 1:
        #         for i in range(self.n):
        #            if self.ganmaP[i] != 1:
        #                self.
        # 功率和转子角速度

        # print(mul(matrix(self.u), matrix(system.Bus.Pg[self.a])))
        system.DAE.y[self.p] = mul(mul(self.u, matrix(system.Bus.Pg[self.a])), self.ganmaP)
        system.DAE.y[self.q] = mul(mul(self.u, matrix(system.Bus.Qg[self.a])), self.ganmaQ)

        self.Pg0 = system.DAE.y[self.p]
        Vg = matrix(system.DAE.y[self.v] + 0j)
        ag = matrix(exp(system.DAE.y[self.a] * 1j))
        V = mul(Vg, ag)
        S = system.DAE.y[self.p] - system.DAE.y[self.q] * 1j
        I = div(S, V.H.T)

        delta = np.angle(V + mul((self.ra + self.xq * 1j), I))
        # print(mul(matrix(self.u), matrix(delta)))
        # a = mul(matrix(self.u), matrix(delta))
        # print(type(system.DAE.x[0]))
        system.DAE.x[self.delta] = mul(self.u, matrix(delta))

        # d、q轴电压和电流
        jpi2 = 1.5707963267948966j
        Vdq = mul(self.u + 0j, mul(V, exp(matrix(jpi2 - delta * 1j))))
        idq = mul(self.u + 0j, mul(I, exp(matrix(jpi2 - delta * 1j))))

        Vd = Vdq.real()
        Vq = Vdq.imag()
        Id = idq.real()
        Iq = idq.imag()

        # 机械转矩/功率

        self.pm0 = mul(Vq + mul(self.ra, Iq), Iq) + \
            mul(Vd + mul(self.ra, Id), Id)
        system.DAE.y[self.pm] = self.pm0

        # 剩余状态变量和场电压
        K = div(1, (self.ra ** 2 + mul(self.xq2, self.xd2)))
        self.c1 = mul(self.ra, K)
        self.c2 = mul(self.xd2, K)
        self.c3 = mul(self.xq2, K)

        system.DAE.x[self.e2q] = Vq +mul(self.ra, Iq) + mul(self.xd2, Id)
        system.DAE.x[self.e2d] = Vd + mul(self.ra, Id) - mul(self.xq2, Iq)
        system.DAE.x[self.e1d] = div(mul(mul(mul(self.xq-self.xq1-self.Tq02, self.xq2), self.xq-self.xq1), Iq), mul(self.Tq01, self.xq1))
        K1 = self.xd-self.xd1-div((mul(mul(self.Td02, self.xd2), (self.xd-self.xd1))), mul(self.Td01, self.xd1))
        K2 = self.xd1 - self.xd2 + div(mul(mul(self.Td02, self.xd2), self.xd - self.xd1), mul(self.Td01, self.xd1))
        system.DAE.x[self.e1q] = system.DAE.x[self.e2q] + mul(K2, Id) - div(mul(self.Taa, mul(K1+K2, Id)+system.DAE.x[self.e2q]), self.Td01)

        # print(type(system.Syn6.synsat()))
        # print(system.Syn6.synsat())
        self.vf0 = div(mul(K1, Id) + system.Syn6.synsat(), 1-div(self.Taa, self.Td01))
        system.DAE.y[self.vf] = self.vf0

        # !!! 移除静态发电机节点
        system.SW.remove(idx='SW_1')
        for i in range(system.PV.n):
            idx = 'PV_'+str(i+1)
            system.PV.remove(idx)





    def synsat(self):

        # print(type([0.8] * self.n))
        # print(matrix(0.8, (self.n, 1)))
        b = matrix([[matrix(0.8, (self.n, 1))], list([1.0-self.S10]), list([1.2 * (1.0 - self.S12)])])
        # print(matrix([12.5, -25, 12.5]))
        c2 = b * matrix([12.5, -25, 12.5])
        c1 = b * matrix([-27.5, 50, -22.5])
        c0 = b * matrix([15, -24, 10])

        output = system.DAE.x[self.e1q]

        for i in range(self.n):
            if system.DAE.x[self.e1q[i]] > 0.8:
                output[i] = mul(c2[i], system.DAE.x[self.e1q[i]] ** 2) + mul(c1[i], system.DAE.x[self.e1q[i]]) + c0[i]

        return output

    def gcall(self):
        system.DAE._list2matrix()
        delta = system.DAE.x[self.delta]
        omega = system.DAE.x[self.omega]
        e1q = system.DAE.x[self.e1q]
        e1d = system.DAE.x[self.e1d]
        e2q = system.DAE.x[self.e2q]
        e2d = system.DAE.x[self.e2d]

        ag = system.DAE.y[self.a]
        vg = mul(self.u, system.DAE.y[self.v])
        ss = sin(delta - ag)
        cc = cos(delta - ag)

        self.Id = mul(-vg, (mul(self.c1, ss)+mul(self.c3, cc)))
        self.Iq = mul(vg, (mul(self.c2, ss) - mul(self.c1, cc)))

        self.Id = self.Id + mul(self.c1, e2d) + mul(self.c3, e2q)
        self.Iq = self.Iq - mul(self.c2, e2d) + mul(self.c1, e2q)

        ones = [0] * self.n
        system.DAE.g = system.DAE.g -\
                       spmatrix(system.DAE.y[self.p], self.a, ones, (system.DAE.ny, 1)) - \
                       spmatrix(system.DAE.y[self.q], self.v, ones, (system.DAE.ny, 1)) + \
                       spmatrix(mul(vg, (mul(self.Id, ss)+mul(self.Iq, cc)))-system.DAE.y[self.p], self.p, ones, (system.DAE.ny, 1)) + \
                       spmatrix(mul(vg, (mul(self.Id, cc) - mul(self.Iq, ss)))-system.DAE.y[self.q], self.q, ones, (system.DAE.ny, 1)) + \
                       spmatrix(mul(self.u, (self.pm0 - system.DAE.y[self.pm])), self.pm, ones, (system.DAE.ny, 1)) + \
                       spmatrix(mul(self.u, (self.vf0 - system.DAE.y[self.vf])), self.vf, ones, (system.DAE.ny, 1))

    def Gycall(self):

        system.DAE._list2matrix()
        delta = system.DAE.x[self.delta]
        ag = system.DAE.y[self.a]
        vg = mul(self.u, system.DAE.y[self.v])
        ss = sin(delta - ag)
        cc = cos(delta - ag)

        M1 = mul(vg, (mul(self.c1, cc)-mul(self.c3, ss)))
        M2 = mul(-vg, (mul(self.c2, cc) + mul(self.c1, ss)))
        M3 = -(mul(self.c1, ss)+mul(self.c3, cc))
        M4 = (mul(self.c2, ss)-mul(self.c1, cc))

        self.J11 = mul(vg, (mul(self.Id - M2, cc)-mul(mul(M1+self.Iq, ss))))
        self.J12 = mul(-self.Id, ss)-mul(self.Iq, cc)-mul(vg, (mul(M3, ss)+mul(M4, cc)))
        self.J21 = mul(vg, mul(M2-self.Id, ss)-mul(M1+self.Iq, cc))
        self.J22 = mul(-self.Id, cc) + mul(self.Iq, ss) - mul(vg, mul(M3, cc)-mul(M4, ss))

        system.DAE.Gy = system.DAE.Gy -spmatrix(self.u, self.a, self.p, (system.DAE.ny, system.DAE.ny)) \
                        - spmatrix(self.u, self.v, self.q, (system.DAE.ny, system.DAE.ny)) \
                        - spmatrix([1]*self.n, self.p, self.p, (system.DAE.ny, system.DAE.ny)) \
                        - spmatrix([1] * self.n, self.q, self.q, (system.DAE.ny, system.DAE.ny)) \
                        - spmatrix(self.J11, self.p, self.a, (system.DAE.ny, system.DAE.ny)) \
                        - spmatrix(self.J12, self.p, self.v, (system.DAE.ny, system.DAE.ny)) \
                        - spmatrix(self.J21, self.q, self.a, (system.DAE.ny, system.DAE.ny)) \
                        - spmatrix(self.J22, self.q, self.v, (system.DAE.ny, system.DAE.ny)) \
                        - spmatrix([1] * self.n, self.pm, self.pm, (system.DAE.ny, system.DAE.ny)) \
                        - spmatrix([1] * self.n, self.vf, self.vf, (system.DAE.ny, system.DAE.ny)) \

    def fcall(self):

        rad = 2 * 3.1415926 * system.Settings.freq
        delta = system.DAE.x[self.delta]
        omega = system.DAE.x[self.omega]
        ag = system.DAE.y[self.a]
        vg = mul(self.u, system.DAE.y[self.v])
        ss = sin(delta - ag)
        cc = cos(delta - ag)

        e1q = system.DAE.x[self.e1q]
        e1d = system.DAE.x[self.e1d]
        e2q = system.DAE.x[self.e2q]
        e2d = system.DAE.x[self.e2d]
        iM = div(self.u, self.M)

        # 更新Vf 和Pm

        system.DAE.f = matrix(system.DAE.f)
        Vf = system.DAE.y[self.vf] + mul(self.Komega, omega-matrix(1, (self.n, 1))) - mul(self.KP, system.DAE.y[self.p]-self.Pg0)
        system.DAE.f[self.delta] = mul(rad, mul(self.u, omega - matrix(1, (self.n, 1))))
        system.DAE.f[self.omega] = mul(system.DAE.y[self.pm]-system.DAE.y[self.p]-mul(self.ra, mul(self.Id, self.Id)+mul(self.Iq, self.Iq))-mul(self.D, omega-1), iM)

        # print('sss')
        # print(mul(self.D, omega-1))
        # print(mul(system.DAE.y[self.pm]-system.DAE.y[self.p]-mul(self.ra, mul(self.Id, self.Id)+mul(self.Iq, self.Iq))-mul(self.D, omega-1), iM))
        gd = div(mul(mul(self.xd2, self.Td02), self.xd-self.xd1), mul(self.xd1, self.Td01))
        gq = div(mul(mul(self.xq2, self.Td02), self.xq - self.xq1), mul(self.xq1, self.Td01))
        a1 = div(self.u, self.Td02)
        a2 = mul(a1, self.xd1-self.xd2+gd)
        a3 = div(mul(self.u, self.Taa), mul(self.Td01, self.Td02))
        a4 = div(self.u, self.Td01)
        a5 = mul(a4, self.xd-self.xd1-gd)
        a6 = mul(a4, 1-div(self.Taa, self.Td01))
        b1 = div(self.u, self.Tq02)
        b2 = mul(b1, self.xq1-self.xq2+gq)
        b3 = div(self.u, self.Tq01)
        b4 = mul(b3, self.xq-self.xq1-gq)

        system.DAE.f[self.e1q] = -mul(a4, self.synsat()) - mul(a5, self.Id) + mul(a6, Vf)
        # print(self.synsat())
        system.DAE.f[self.e1d] = mul(-b3, e1d) + mul(b4, self.Iq)
        system.DAE.f[self.e2q] = mul(-a1, e2q) + mul(a1, e1q) - mul(a2, self.Id) + mul(a3, Vf)
        system.DAE.f[self.e2d] = mul(-b1, e2d) + mul(b1, e1d) + mul(b2, self.Iq)


    def Fxcall(self):

        delta = system.DAE.x[self.delta]
        omega = system.DAE.x[self.omega]
        ag = system.DAE.y[self.a]
        vg = mul(self.u, system.DAE.y[self.v])
        ss = sin(delta - ag)
        cc = cos(delta - ag)

        e1q = system.DAE.x[self.e1q]
        e1d = system.DAE.x[self.e1d]
        e2q = system.DAE.x[self.e2q]
        e2d = system.DAE.x[self.e2d]

        iM = div(self.u, self.M)

        M1 = mul(vg, (mul(self.c1, cc) - mul(self.c3, ss)))
        M2 = mul(-vg, (mul(self.c2, cc) + mul(self.c1, ss)))
        M3 = -(mul(self.c1, ss) + mul(self.c3, cc))
        M4 = (mul(self.c2, ss) - mul(self.c1, cc))

        rad = 2 * 3.1415926 * system.Settings.freq
        Wn = self.u * rad  # print(Wn)

        # print(mul(iM, self.D)+matrix(1, (self.n, 1))-self.u)
        system.DAE.Fx = system.DAE.Fx - spmatrix(matrix(1, (self.n, 1))-self.u, self.delta, self.delta, (system.DAE.nx, system.DAE.nx)) \
                        + spmatrix(Wn, self.delta, self.omega, (system.DAE.nx, system.DAE.nx)) \
                        - spmatrix(mul(iM, self.D)+matrix(1, (self.n, 1))-self.u, self.omega, self.omega, (system.DAE.nx, system.DAE.nx)) \
                        + spmatrix(mul(mul(2*self.ra, mul(self.Id, M1)+mul(self.Iq, M2)), iM), self.omega, self.delta, (system.DAE.nx, system.DAE.nx))
        system.DAE.Fy = system.DAE.Fy \
                        - spmatrix(mul(mul(2 * self.ra, mul(self.Id, M1) + mul(self.Iq, M2)), iM), self.omega, self.a, (system.DAE.nx, system.DAE.ny)) \
                        - spmatrix(mul(mul(2 * self.ra, mul(self.Id, M3) + mul(self.Iq, M4)), iM), self.omega, self.v, (system.DAE.nx, system.DAE.ny)) \
                        - spmatrix(iM, self.omega, self.p, (system.DAE.nx, system.DAE.ny)) \
                        + spmatrix(iM, self.omega, self.pm, (system.DAE.nx, system.DAE.ny))
        system.DAE.Gx = system.DAE.Gx + spmatrix(self.J11, self.p, self.delta,(system.DAE.ny, system.DAE.nx)) \
                        + spmatrix(self.J21, self.q, self.delta, (system.DAE.ny, system.DAE.nx))

        Gp1 = mul(vg, (mul(self.c3, ss) + mul(self.c1, cc)))
        Gp2 = mul(vg, (mul(self.c1, ss) - mul(self.c2, cc)))
        Gq1 = mul(vg, (mul(self.c3, cc) - mul(self.c1, ss)))
        Gq2 = mul(vg, (mul(self.c1, cc) + mul(self.c2, ss)))

        N1 = mul(mul(-2 * self.ra, mul(self.Id, self.c3) + mul(self.Iq, self.c1)), iM)
        N2 = mul(mul(-2 * self.ra, mul(self.Id, self.c1) - mul(self.Iq, self.c2)), iM)

        gd = div(mul(mul(self.xd2, self.Td02), self.xd - self.xd1), mul(self.xd1, self.Td01))
        gq = div(mul(mul(self.xq2, self.Td02), self.xq - self.xq1), mul(self.xq1, self.Td01))
        a1 = div(self.u, self.Td02)
        a2 = mul(a1, self.xd1 - self.xd2 + gd)
        a3 = div(mul(self.u, self.Taa), mul(self.Td01, self.Td02))
        a4 = div(self.u, self.Td01)
        a5 = mul(a4, self.xd - self.xd1 - gd)
        a6 = mul(a4, 1 - div(self.Taa, self.Td01))
        b1 = div(self.u, self.Tq02)
        b2 = mul(b1, self.xq1 - self.xq2 + gq)
        b3 = div(self.u, self.Tq01)
        b4 = mul(b3, self.xq - self.xq1 - gq)

        a = []
        for i in range(self.n):
            if self.u[i] == 1:
                a.append(0)
            else:
                a.append(1)
        a = matrix(a)

        system.DAE.Fx = system.DAE.Fx + spmatrix(N1, self.omega, self.e2q, (system.DAE.nx, system.DAE.nx)) \
                        + spmatrix(N2, self.omega, self.e2d, (system.DAE.nx, system.DAE.nx)) \
                        + spmatrix(mul(a5, M1), self.e1q, self.delta, (system.DAE.nx, system.DAE.nx)) \
                        + spmatrix(mul(a6, self.Komega), self.e1q, self.omega, (system.DAE.nx, system.DAE.nx)) \
                        - spmatrix(mul(a4, self.synsat2())+a, self.e1q, self.e1q, (system.DAE.nx, system.DAE.nx)) \
                        - spmatrix(mul(a5, self.c3), self.e1q, self.e2q, (system.DAE.nx, system.DAE.nx)) \
                        - spmatrix(mul(a5, self.c1), self.e1q, self.e2d, (system.DAE.nx, system.DAE.nx)) \
                        - spmatrix(mul(b4, M2), self.e1d, self.delta, (system.DAE.nx, system.DAE.nx)) \
                        - spmatrix(b3+a, self.e1d, self.e1d, (system.DAE.nx, system.DAE.nx)) \
                        + spmatrix(mul(b4, self.c1), self.e1d, self.e2q, (system.DAE.nx, system.DAE.nx)) \
                        - spmatrix(mul(b4, self.c2), self.e1d, self.e2d, (system.DAE.nx, system.DAE.nx)) \
                        + spmatrix(mul(a2, M1), self.e2q, self.delta, (system.DAE.nx, system.DAE.nx)) \
                        + spmatrix(mul(a3, self.Komega), self.e2q, self.omega, (system.DAE.nx, system.DAE.nx)) \
                        + spmatrix(a1, self.e2q, self.e1q, (system.DAE.nx, system.DAE.nx)) \
                        - spmatrix(a1+mul(a2, self.c3)+a, self.e2q, self.e2q, (system.DAE.nx, system.DAE.nx)) \
                        - spmatrix(mul(a2, self.c1), self.e2q, self.e2d, (system.DAE.nx, system.DAE.nx)) \
                        - spmatrix(mul(b2, M2), self.e2d, self.delta, (system.DAE.nx, system.DAE.nx)) \
                        + spmatrix(b1, self.e2d, self.e1d, (system.DAE.nx, system.DAE.nx)) \
                        + spmatrix(mul(b2, self.c1), self.e2d, self.e2q, (system.DAE.nx, system.DAE.nx)) \
                        - spmatrix(b1+mul(b2, self.c2)+a, self.e2d, self.e2d, (system.DAE.nx, system.DAE.nx))

        system.DAE.Fy = system.DAE.Fy \
                        + spmatrix(a6, self.e1q, self.vf, (system.DAE.nx, system.DAE.ny)) \
                        + spmatrix(a3, self.e2q, self.vf, (system.DAE.nx, system.DAE.ny)) \
                        - spmatrix(mul(a5, M1), self.e1q, self.a, (system.DAE.nx, system.DAE.ny)) \
                        - spmatrix(mul(a5, M3), self.e1q, self.v, (system.DAE.nx, system.DAE.ny)) \
                        + spmatrix(mul(b4, M2), self.e1d, self.a, (system.DAE.nx, system.DAE.ny)) \
                        + spmatrix(mul(b4, M4), self.e1d, self.v, (system.DAE.nx, system.DAE.ny)) \
                        - spmatrix(mul(a2, M1), self.e2q, self.a, (system.DAE.nx, system.DAE.ny)) \
                        - spmatrix(mul(a2, M3), self.e2q, self.v, (system.DAE.nx, system.DAE.ny)) \
                        + spmatrix(mul(b2, M2), self.e2d, self.a, (system.DAE.nx, system.DAE.ny)) \
                        + spmatrix(mul(b2, M4), self.e2d, self.v, (system.DAE.nx, system.DAE.ny)) \
                        - spmatrix(mul(a6, self.KP), self.e1q, self.p, (system.DAE.nx, system.DAE.ny)) \
                        - spmatrix(mul(a3, self.KP), self.e2q, self.p, (system.DAE.nx, system.DAE.ny))

        system.DAE.Gx = system.DAE.Gx + spmatrix(Gp1, self.p, self.e2q, (system.DAE.ny, system.DAE.nx)) \
                        + spmatrix(Gp2, self.p, self.e2d, (system.DAE.ny, system.DAE.nx)) \
                        + spmatrix(Gq1, self.q, self.e2q, (system.DAE.ny, system.DAE.nx)) \
                        + spmatrix(Gq2, self.q, self.e2d, (system.DAE.ny, system.DAE.nx))

    def synsat2(self):

        # print(type([0.8] * self.n))
        # print(matrix(0.8, (self.n, 1)))
        b = matrix([[matrix(0.8, (self.n, 1))], list([1.0 - self.S10]), list([1.2 * (1.0 - self.S12)])])
        # print(matrix([12.5, -25, 12.5]))
        c2 = b * matrix([12.5, -25, 12.5])
        c1 = b * matrix([-27.5, 50, -22.5])
        c0 = b * matrix([15, -24, 10])

        output = matrix(1.0, (self.n, 1))

        for i in range(self.n):
            if system.DAE.x[self.e1q[i]] > 0.8:
                output[i] = mul(2*c2[i], system.DAE.x[self.e1q[i]]) + c1[i]

        return output


