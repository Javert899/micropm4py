import math

# RAN ON CORTEX M3, 64kb RAM

class consts:
    g = 536870911
    p = 2147483647
    c = 1


def gen():
    consts.c = (consts.c*consts.g) % consts.p
    return consts.c / consts.p


def erf(x):
    v = 1
    v = v + 0.278393*x
    y = x*x
    v = v + 0.230389*y
    y = y*x
    v = v + 0.000972*y
    y = y*x
    v = v + 0.078108*y
    v = v*v
    v = v*v
    v = 1.0/v
    v = 1.0 - v
    return v


def pdf(x, mu, sig):
    return 1.0/(sig*math.sqrt(2*math.pi))*math.exp(-0.5*((x-mu)/sig)**2)


def cdf(x, mu, sig):
    return 0.5*(1.0 + erf((x-mu)/(sig*math.sqrt(2))))


def getv(mu, sig):
    v1 = gen()
    v2 = gen()
    return mu + sig*math.cos(2*math.pi*v2)*math.sqrt(-2.0*math.log(v1))


def main():
    print(erf(0.5))
    print(cdf(0.0, 0.0, 1.0))
    print(pdf(0.0, 0.0, 1.0))
    print("")
    i = 0
    while i < 10:
        print(getv(0.0, 1.0))
        i = i + 1


if __name__ == "__main__":
    main()
