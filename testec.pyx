###################
###Usando arrays###
###################

from cpython cimport array
import array
def vetor(n):
    """
    Pega o vetor e retorna ele com + i.
    Retorna um objeto array.
    """
    lent = len(n)
    cdef array.array n__ = array.array("i", n)
    cdef int[:] n_ = n__

    cdef int i
    for i in range(3):
        n_[i] = i + n_[i]
    return n_

cpdef double var(v__):
    cdef double[:] v = array.array("d", v__)
    cdef double m = 0,  resp = 0
    cdef int lent = len(v), i = 0,
    
    for i in range(lent):
        m = m + v[i]
        
    for i in range(lent):
        resp = resp + (v[i] - m) ** 2

    return resp/lent

cpdef iteracao(float self_x, float self_y, float self_repulsao, float self_angx, float self_angy,
             float obj_x, float obj_y, float obj_repulsao):
    
    cdef float x_resp = 0, y_resp = 0, fator = 0, fator_repulsao = 0
    try:
        x_resp = 1/(self_x - obj_x)
    except:
        pass
    try:
        y_resp = 1/(self_y - obj_y)
    except:
        pass

    try:
        fator = 1/(x_resp**2 + y_resp**2)**(1/2)
    except:
        pass

    if self_repulsao < 0 and obj_repulsao < 0:
        fator_repulsao = (self_repulsao + obj_repulsao)
    elif self_repulsao > 0 and obj_repulsao > 0:
        fator_repulsao = -(self_repulsao + obj_repulsao)
    elif self_repulsao > 0 and obj_repulsao < 0:
        fator_repulsao = (self_repulsao)/10
    elif self_repulsao < 0 and obj_repulsao > 0:
        fator_repulsao = (obj_repulsao)/10

    cdef float angx = 0, angy = 0
    angx = (x_resp*fator)*fator_repulsao * 20
    angy = (y_resp*fator)*fator_repulsao * 20

    return angx, angy

def ache_0_():
    from math import cos
    cdef int i
    cdef float x
    cdef double resp
    for i in range(1_000_000_000):
        x = i/10_000
        resp = cos(x) + 1.001 - x/1_000_000
        if resp < 0.0001 and resp < 0.0001:
            return x

cpdef mult_m(a, b):
    cdef float[3][3] a_ = a
    cdef float[3][3] b_ = b

    cdef float[3][3] c_

    c_[0][0] = a_[0][0] * b_[0][0] + a_[0][1] * b_[1][0] + a_[0][2] * b_[2][0]
    c_[0][1] = a_[0][0] * b_[0][1] + a_[0][1] * b_[1][1] + a_[0][2] * b_[2][1]
    c_[0][2] = a_[0][0] * b_[0][2] + a_[0][1] * b_[1][2] + a_[0][2] * b_[2][2]

    c_[1][0] = a_[1][0] * b_[0][0] + a_[1][1] * b_[1][0] + a_[1][2] * b_[2][0]
    c_[1][1] = a_[1][0] * b_[0][1] + a_[1][1] * b_[1][1] + a_[1][2] * b_[2][1]
    c_[1][2] = a_[1][0] * b_[0][2] + a_[1][1] * b_[1][2] + a_[1][2] * b_[2][2]

    c_[2][0] = a_[2][0] * b_[0][0] + a_[2][1] * b_[1][0] + a_[2][2] * b_[2][0]
    c_[2][1] = a_[2][0] * b_[0][1] + a_[2][1] * b_[1][1] + a_[2][2] * b_[2][1]
    c_[2][2] = a_[2][0] * b_[0][2] + a_[2][1] * b_[1][2] + a_[2][2] * b_[2][2]
    
    return c_

cpdef mult_m_v(a, b):
    cdef float[3][3] a_ = a
    cdef float[3] b_ = b

    cdef float[3] c_

    c_[0] = a_[0][0] * b_[0] + a_[0][1] * b_[1] + a_[0][2] * b_[2]
    c_[1] = a_[1][0] * b_[0] + a_[1][1] * b_[1] + a_[1][2] * b_[2]
    c_[2] = a_[2][0] * b_[0] + a_[2][1] * b_[1] + a_[2][2] * b_[2]
    
    return c_

cpdef float mult_v_v(a, b):
    cdef float[3] a_ = a
    cdef float[3] b_ = b

    cdef float c_
    c_ = a_[0] * b_[0] + a_[1] * b_[1] + a_[2] * b_[2]
    
    return c_

cpdef mult_v(a, b):
    cdef float[3] a_ = a
    cdef float[3] b_ = b

    cdef float[3] c_

    c_[0] = a_[0] * b_[0]
    c_[1] = a_[1] * b_[1]
    c_[2] = a_[2] * b_[2]
    
    return c_

cpdef double media_C(a_):
    cdef int[2] a = a_
    cdef float resp
    cdef int i = 0, l_ = a[1] - a[0]

    for i in range(a[0], a[1]):
        resp = resp + i
    resp = resp/l_
    return resp



    
