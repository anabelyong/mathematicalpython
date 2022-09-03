import numpy as np
from numpy.random import random
import scipy
import scipy.stats
import matplotlib as mpl
import matplotlib.pyplot as plt

# initialize parameters
nA = 44; nB = 27; nAB = 4; nO = 88
p = 0.3; q=0.3; r = 1 - p - q
n = nA + nB + nAB + nO
hA = 0.5
hB= 0.5
w = 0.1

x = [nA, nB, nO, nAB]
theta=[p, q, r]

def log_likelihood(theta, x):
    # unpack list
    nA = x[0]; nB = x[1]; nO = x[2]; nAB = x[3]
    p = theta[0]; q = theta[1]; r = theta[2]

    # calculate each part of the equation individually
    pt1 = nA * np.log(p**2 + 2*p*r)
    pt2 = nB * np.log(q**2 + 2*q*r)
    pt3 = nAB * np.log(2*p*q)
    pt4 = nO * np.log(r**2)

    return pt1 + pt2 + pt3 + pt4

def reflect(x, a, b):
    # returns the values when x is reflected into the range (a,b)
    side = 0 
    e = 0

    if x < a:
        e = a - x
        side = 0
    elif x > b:
        e = x - b
        side = 1 

    if e !=0:
        n=np.trunc(e/(b-a))
        if (n-2*np.trunc(n/2) !=0): #change sdide if n is odd
            side=1-side
        e = e -n*(b-a)
        if side==1:
            x=b-e
        else:
            x=a+e
    return(round(x, 3))

def genecounting(theta, n, hA, hB):
    # unpack list
    nA = x[0]; nB = x[1]; nO = x[2]; nAB = x[3]
    p = theta[0]; q = theta[1]; r = theta[2]

    p = 1 / (2 * n) * (nAB + nA * (1 + hA))
    q = 1 / (2 * n) * (nAB + nB * (1 + hB))
    r = 1 - p - q

    hA = p**2 / (p**2 + 2 * p * r)
    hB = q**2 / (q**2 + 2 * q * r)
    
    return p, q, r

def make_new_number(theta, w):
    # generate random number between 0 and 1
    u = random()

    p = theta[0]
    q = theta[1]
    r = theta[2]

    # if statements for ... 
    if u < 1./3.:
        s = p + q
        pnew = p + w * (random() - 1/2)
        pnew = reflect(pnew, 0, s)
        qnew = s - pnew
        rnew = r
    elif u < 2./3.:
        s = q + r
        qnew = q + w * (random() - 1/2)
        qnew = reflect(qnew, 0, s)
        rnew = s - qnew
        pnew = p
    else:    
        s = r + p
        rnew = r + w * (random() - 1/2)
        rnew = reflect(rnew, 0, s)
        pnew = s - rnew
        qnew = q
    
    return pnew, qnew, rnew

print(f"Before: p:{p} q:{q} r:{r}")

plist = []; qlist = []; rlist = []; llist = []
for _ in range(10):
    #p, q, r = make_new_number(theta=[p, q, r], w=w)
    p, q, r  = genecounting(theta=[p, q, r], n=n)
    ll_value = log_likelihood(theta=[p, q, r], x=x) 

    plist.append(p)
    qlist.append(q)
    rlist.append(r)
    llist.append(ll_value)

print(f"After: p:{p} q:{q} r:{r}")

print('-'*25)
print("plist")
print(plist)
print('-'*25)
print("qlist")
print(qlist)
print('-'*25)
print("rlist")
print(rlist)
print('-'*25)
print("likelihood list")
print(llist)

# create plot
fig = plt.figure()
mpl.style.use("seaborn")
#plt.suptitle("Joint of p and q")
plt.plot(range(len(plist)), plist)
plt.xlabel('p')
plt.ylabel('q')
plt.show()