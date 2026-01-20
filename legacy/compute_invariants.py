from sage.all import *

# Compute the invariants of the number field K.
def compute_field(K):
    d = K.absolute_generator()**2                   # Compute the value of d (K = Q(sqrt(d)))
    dK = K.discriminant()                           # Compute the discriminant of K (d_K)
    hK = K.class_number()                           # Compute the class number of K (h_K)
    fu = K.units()[0]                               # Compute the fundamental unit of K
    rK = K.regulator()                              # Compute the regulator of K (R_K)
    mb = K.minkowski_bound()                        # Compute the Minkowski bound of K (MB)

    #print([d, dK, hK, fu, rK, mb])
    return [d, dK, hK, fu, rK, mb]

# Compute the field invariants of the first n real quadratic fields
def compute_invariants(n):
    orig_n = n
    invariants = {}
    i = 2
    while n > 0:
        if is_squarefree(i):
            x = polygen(ZZ, 'x')
            K = NumberField(x**Integer(2) - i, names=('u',))
            invariants[K] = compute_field(K)
            n-=1
        i+=1

        if n-1 > 0 & (i % 10 == 0):
            print(str(round(((orig_n-n) / (orig_n))*100, 2)) + "%")
    return invariants
