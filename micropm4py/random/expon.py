import math

# RAN ON CORTEX M3, 64kb RAM

class consts:
    g = 536870911
    p = 2147483647
    c = 1


def gen():
    consts.c = (consts.c*consts.g) % consts.p
    return consts.c / consts.p


def pdf(x, lam):
    return lam*math.exp(-lam*x)


def cdf(x, lam):
    return 1-math.exp(-lam*x)


def getv(lam):
    return -1.0/lam*math.log(1.0 - gen())
