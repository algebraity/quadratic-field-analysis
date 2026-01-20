from sage.all import *
import json
import multiprocessing as mp
import numpy as np
from plot_invariants import *
from track_fu_spikes import *

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

def _worker(i):
    x = polygen(ZZ, 'x')
    K = NumberField(x**Integer(2) - i, names=('u',))
    return (i, compute_field(K))

# Compute the field invariants of the first n real quadratic fields
def compute_invariants(n, jobs=None):
    if jobs is None:
        jobs = mp.cpu_count()

    orig_n = n
    invariants = {}
    i = 2
    ds = []
    while n > 0:
        if is_squarefree(i):
            ds.append(i)
        n -= 1
        i += 1

        if n-1 > 0 & (i % 10 == 0):
            print(str(round(((orig_n-n) / (orig_n))*100, 2)) + "%")

    try:
        ctx = mp.get_context("fork")
    except ValueError:
        ctx = mp.get_context()

    with ctx.Pool(processes=jobs) as pool:
        for d, inv in pool.imap_unordered(_worker, ds, chunksize=10000):
            x = polygen(ZZ, 'x')
            K = NumberField(x**Integer(2) - d, names=('u',))
            invariants[K] = inv

    return invariants

def main(n=-1):
    if n == -1:
        n = int(input("Enter the number of fields to compare: "))
        while not (isinstance(n, int)) and not (n > 0):
            n = int(input("Input not accepted. Enter 0 for real and 1 for imaginary: "))

    invariants = compute_invariants(n)
    if n < 10000:
        plot_invariants(invariants)
    inv_spikes = plot_fu_spikes(invariants)

    to_csv(invariants, inv_spikes, 'invariants_data.csv', "fu_spikes.csv")

def to_csv(invariants, inv_spikes, datafile, spikesfile):
    to_store = [["d", "dK", "hK", "fu", "rK", "mb"]]
    for field in invariants:
        to_store.append(invariants[field])
    np.savetxt(datafile, to_store, delimiter=',', fmt="%s")
    np.savetxt(spikesfile, [inv_spikes[0], inv_spikes[1]], delimiter=',', fmt="%s")


#def to_json(invariants, inv_spikes, filename):
#    print("Saving data to", filename)
#    to_store = {}
#
#    # Process the 'invariants' data
#    if isinstance(invariants, dict):
#        for field, invariants in invariants.items():
#            field_info = {}
#
#            # Store the invariants in a dictionary
#            field_info['defining_polynomial'] = str(field.polynomial())
#
#            # Store the invariants
#            field_info['invariants'] = {
#                'd': int(invariants[0]),        # Discriminant of the field (d)
#                'dK': int(invariants[1]),       # Discriminant of the field (d_K)
#                'hK': int(invariants[2]),       # Class number of K (h_K)
#                'fu': str(invariants[3]),       # Fundamental unit (fu), converted to string
#                'rK': float(invariants[4]),     # Regulator of K (R_K)
#                'mb': float(invariants[5])      # Minkowski bound of K (MB)
#            }
#
#            # Store the field info under its corresponding key
#            to_store[str(field)] = field_info
#
#        fu_spikes = []
#        for spike in inv_spikes:
#            fu_spikes.append([int(spike[0]), str(real(spike[1]))])
#        to_store["fu_spikes"] = fu_spikes
#
#    # Save the structured data to a JSON file
#    with open(filename, 'w') as json_file:
#        json.dump(to_store, json_file, indent=4)

#### MAIN FUNCTION CODE ####
if __name__ == "__main__":
    main()

