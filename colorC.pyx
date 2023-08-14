
cpdef corC(int x_1, int x_2, int y_1, int y_2):
    cdef int[3] color = [255,255,255]

    try:
        color[0] = int(50000 / (x_1+x_2))%255
    except:
        pass
    try:
        color[1] = int(80000 / (y_1+x_1+y_2+x_2))%255
    except:
        pass
    try:
        color[2] = int(50000 / (y_1+y_2))%255
    except:
        pass

    return color

