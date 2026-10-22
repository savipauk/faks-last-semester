r"""°°°
Sveučilište u Zagrebu  
Fakultet elektrotehnike i računarstva  
  
## Strojno učenje 1 2025./2026.  
http://www.fer.unizg.hr/predmet/struce1
°°°"""
# |%%--%%| <Dr3Mdgg4yH|yxP9VGMBrx>
r"""°°°
------------------------------

### Laboratorijska vježba 0: Uvod u Python

*Verzija: 1.1  
Zadnji put ažurirano: 4. 10. 2021.*

(c) 2015-2026 Jan Šnajder, Domagoj Alagić 

Rok za predaju: **N/A**

------------------------------
°°°"""
# |%%--%%| <yxP9VGMBrx|u08PCv6Feb>
r"""°°°
### 1. Python
°°°"""
# |%%--%%| <u08PCv6Feb|NIIXiNVpFz>
r"""°°°
#### 1.1. Liste
°°°"""
# |%%--%%| <NIIXiNVpFz|omgq2boyGO>

xs = [5, 6, 2, 3]
xs

# |%%--%%| <omgq2boyGO|sQ36OMPHWN>

xs[0]

# |%%--%%| <sQ36OMPHWN|O3ySJ4reR5>

xs[-1]

# |%%--%%| <O3ySJ4reR5|YSlp68MEAJ>

xs[2] = 10
xs

# |%%--%%| <YSlp68MEAJ|AFGjb1wtwc>

xs[0] = "a book"
xs

# |%%--%%| <AFGjb1wtwc|mmcXKm0w8U>

xs[1] = [3, 4]
xs

# |%%--%%| <mmcXKm0w8U|oUMz5gWniC>

xs += [99, 100]
xs

# |%%--%%| <oUMz5gWniC|G6uwNIIQf6>

xs.extend([22, 33])
xs

# |%%--%%| <G6uwNIIQf6|ZWBnxPHuwk>

xs[-1]

# |%%--%%| <ZWBnxPHuwk|lkaiezfVlm>

xs.pop()

# |%%--%%| <lkaiezfVlm|IkNu797P8R>

xs

# |%%--%%| <IkNu797P8R|ZuMUwFx3N7>

len(xs)

# |%%--%%| <ZuMUwFx3N7|46odS3PgEi>

xs[0:2]

# |%%--%%| <46odS3PgEi|YcxK3WglE3>

xs[2:]

# |%%--%%| <YcxK3WglE3|Q0LCuA8KHZ>

xs[:3]

# |%%--%%| <Q0LCuA8KHZ|t162zgxCOZ>

xs[:-2]

# |%%--%%| <t162zgxCOZ|PihyWKuXMF>

for el in xs:
    print(el)

# |%%--%%| <PihyWKuXMF|mhAAVm1DcR>

for idx, el in enumerate(xs):
    print(idx, el)

# |%%--%%| <mhAAVm1DcR|sTMm62ZWDH>

for idx in range(len(xs)):
    print(idx)

# |%%--%%| <sTMm62ZWDH|lNVq0fUVr2>

for idx in range(2, len(xs)):
    print(idx)

# |%%--%%| <lNVq0fUVr2|0bB79sKoeO>

for idx in range(0, len(xs), 2):
    print(idx)

# |%%--%%| <0bB79sKoeO|fXLtjGj8PE>

xs = []
for x in range(10):
    xs.append(x ** 2)
xs

# |%%--%%| <fXLtjGj8PE|PFiZdBdrQ7>

[x ** 2 for x in range(10)]

# |%%--%%| <PFiZdBdrQ7|bBBuMxsZLy>

[x ** 2 for x in range(10) if x % 2 == 0]

# |%%--%%| <bBBuMxsZLy|YxdTJ6r1Dx>

[x ** 2 if x % 2 == 0 else 512 for x in range(10)]

# |%%--%%| <YxdTJ6r1Dx|3udMYaCr0r>

for a, b in zip([1, 2, 3], [4, 5, 6]):
    print(a, b)

# |%%--%%| <3udMYaCr0r|eJZL98r9Tb>

for a, b in zip([1, 2, 3], [4, 5, 6, 7]):
    print(a, b)

# |%%--%%| <eJZL98r9Tb|xLSH17tAcf>

a_list, b_list = zip(*[(1, 4), (2, 3), (5, 6)])
print(a_list)
print(b_list)

# |%%--%%| <xLSH17tAcf|gCfMfIwYuF>
r"""°°°
#### 1.2. Stringovi
°°°"""
# |%%--%%| <gCfMfIwYuF|8XZ3QiM8Y1>

cool_name = "Miyazaki"
cool_name

# |%%--%%| <8XZ3QiM8Y1|cW9mbaljkX>

cool_name + " is " + "great"

# |%%--%%| <cW9mbaljkX|IBiQvSSgK5>

num_people = 200000

# |%%--%%| <IBiQvSSgK5|kW8CgyjadU>

cool_name + " has " + num_people + " citizens"

# |%%--%%| <kW8CgyjadU|DgvJ2hWclB>

cool_name + " has " + str(num_people) + " citizens"

# |%%--%%| <DgvJ2hWclB|Msk8lBShWb>

len(cool_name)

# |%%--%%| <Msk8lBShWb|yst5cbGnn1>

print("{0} has {1} citizens".format(cool_name, num_people))

# |%%--%%| <yst5cbGnn1|65PmhMch7s>

print(f"{cool_name} has {num_people} citizens")

# |%%--%%| <65PmhMch7s|9JqtmV9PwX>
r"""°°°
#### 1.3. Razredi
°°°"""
# |%%--%%| <9JqtmV9PwX|mMamAY80xs>

class Product:

    def __init__(self, product_name=None, tags=None, price=0.0):
        self.product_name = product_name
        self.tags = [] if tags is None else tags
        self.price = price
        
    vat = 0.25 

    def product_price(self, with_pdv=False):
        if with_pdv:
            return self.price * (1 + self.vat)
        else:
            return self.price
    
    def contains_tag(self, tag):
        return (tag in self.tags)

# |%%--%%| <mMamAY80xs|WBNr8V3QOq>

prod = Product(product_name="toilet paper", tags=["health", "toilet", "fresh"], price=10)
print(prod.product_price(with_pdv=True))
print(prod.product_price(with_pdv=False))

# |%%--%%| <WBNr8V3QOq|t78GROjHBv>

prod.contains_tag("fresh")

# |%%--%%| <t78GROjHBv|9e13xa0kWe>

prod.contains_tag("money")

# |%%--%%| <9e13xa0kWe|raUG0xxDGU>

prod1 = Product(product_name="toilet paper", price=10)
prod2 = Product(product_name="toothbrush", price=10)
Product.vat = 0.5
prod1.vat = 0.3

# |%%--%%| <raUG0xxDGU|nQtlLZvv2y>

prod1.product_price(with_pdv=True)

# |%%--%%| <nQtlLZvv2y|mFzWgHZxGX>

prod2.product_price(with_pdv=True)

# |%%--%%| <mFzWgHZxGX|I6EgiceM6b>
r"""°°°
### 2. NumPy
°°°"""
# |%%--%%| <I6EgiceM6b|1yFjK24QNG>

import numpy as np

# |%%--%%| <1yFjK24QNG|2NnHoVKyL4>
r"""°°°
#### 2.1. Polja
°°°"""
# |%%--%%| <2NnHoVKyL4|GLRgaWgVyU>

a = np.array([1, 2, 3])
a

# |%%--%%| <GLRgaWgVyU|cqvjknpXIH>

c = np.array([1, 2, 3], dtype=np.float64)
c

# |%%--%%| <cqvjknpXIH|D8D7Orp9tu>

a.shape

# |%%--%%| <D8D7Orp9tu|J0Y4CKNbqz>

b = np.array([[1, 3, 4], [2, 3, 5]])
b

# |%%--%%| <J0Y4CKNbqz|iWGXIJMrQh>

b.shape

# |%%--%%| <iWGXIJMrQh|Mjb5pj0uF9>

b[1, 2]

# |%%--%%| <Mjb5pj0uF9|iq54xlNqdG>

b[0:1, 2] # Primijetite razliku!

# |%%--%%| <iq54xlNqdG|NhS4lDjnB9>

b[:, 2]

# |%%--%%| <NhS4lDjnB9|DnCusFjSW5>

b[0:2, 2]

# |%%--%%| <DnCusFjSW5|S6B0eXIuCU>

d = np.array([[1, 2, 3], [4, 5, 6]])
d

# |%%--%%| <S6B0eXIuCU|PVL0YzyCdZ>

np.append(d, 1)

# |%%--%%| <PVL0YzyCdZ|hpIq94fQBn>

np.append(d, [1, 2])

# |%%--%%| <hpIq94fQBn|urRzgXvizs>

d

# |%%--%%| <urRzgXvizs|Dy2TxoTGWp>

to_add = np.array([[1], [2]])
to_add

# |%%--%%| <Dy2TxoTGWp|ChWkVcsEHq>

d + to_add

# |%%--%%| <ChWkVcsEHq|SFiPLj18kn>

np.hstack([d, to_add])

# |%%--%%| <SFiPLj18kn|PQRDF7rdpp>

np.vstack([d, to_add])

# |%%--%%| <PQRDF7rdpp|SsOix0mHxg>

to_add2 = np.array([2, 3, 4])
to_add2

# |%%--%%| <SsOix0mHxg|xXCkJkGy94>

result = np.vstack([d, to_add2])
result

# |%%--%%| <xXCkJkGy94|aYr7o8ZmnT>

np.sqrt(result)

# |%%--%%| <aYr7o8ZmnT|sWdGU2n7M4>

result * 2

# |%%--%%| <sWdGU2n7M4|hOlMS5Ia7K>

result + result

# |%%--%%| <hOlMS5Ia7K|VixSK4o61h>

x = np.array([[1,2],[3,4]])
y = np.array([[5,6],[7,8]])
v = np.array([1,2])
w = np.array([5,3])
print(x)
print(y)
print(v)
print(w)

# |%%--%%| <VixSK4o61h|xDgbdj38Vn>

v.dot(w)

# |%%--%%| <xDgbdj38Vn|S1hmfAZe04>

np.dot(v, w)

# |%%--%%| <S1hmfAZe04|y6bv4XV3pL>

x.dot(v)

# |%%--%%| <y6bv4XV3pL|oSKcODqryu>

np.linalg.inv(x)

# |%%--%%| <oSKcODqryu|bDtC4WxFw4>

np.linalg.det(x)

# |%%--%%| <bDtC4WxFw4|1i7bKyJRFD>

np.linalg.norm(x)

# |%%--%%| <1i7bKyJRFD|wsS5w0MYIv>

x

# |%%--%%| <wsS5w0MYIv|GDOhpmdnCU>

np.max(x)

# |%%--%%| <GDOhpmdnCU|NXJhY4hD4A>

np.max(x, axis=0)

# |%%--%%| <NXJhY4hD4A|ZJWRNw6EIq>

np.max(x, axis=1)

# |%%--%%| <ZJWRNw6EIq|i2UJYG8KoB>

p = np.array([2, 3, 1, 6, 4, 5])
b = ["a", "b", "c", "d", "e", "f"]

# |%%--%%| <i2UJYG8KoB|FsuwBQzCc1>

np.max(p)

# |%%--%%| <FsuwBQzCc1|diCN5xK0ui>

np.argmax(p)

# |%%--%%| <diCN5xK0ui|gHnWD3p5pJ>

b[np.argmax(p)]

# |%%--%%| <gHnWD3p5pJ|6diXLF2R25>

np.mean(p)

# |%%--%%| <6diXLF2R25|19g32L3ES6>

np.var(p)

# |%%--%%| <19g32L3ES6|48mUTMTDX6>

np.linspace(1, 10, 100)

# |%%--%%| <48mUTMTDX6|RZjoMY3pgy>

w = np.array([[1, 2, 3], [4, 5, 6]])

# |%%--%%| <RZjoMY3pgy|5SfNcK9vhn>

w > 2

# |%%--%%| <5SfNcK9vhn|yi23Kc391k>

w[w>2]

# |%%--%%| <yi23Kc391k|sbbM2O2qGI>

w = np.array([1, 2, 3, 4, 5, 6, 7, 8])
y = np.array([0, 0, 0, 1, 0, 0, 1, 0])

# |%%--%%| <sbbM2O2qGI|3FEFbNndzz>

w[y==1] # Jako korisno!

# |%%--%%| <3FEFbNndzz|ypgJjBZhkD>

list(p)

# |%%--%%| <ypgJjBZhkD|dMXfkbuyYW>

p.tolist()

# |%%--%%| <dMXfkbuyYW|xCTVjWfDq5>
r"""°°°
### 3. Matplotlib
°°°"""
# |%%--%%| <xCTVjWfDq5|AoE9sdVZnf>

import matplotlib.pyplot as plt
%pylab inline

# |%%--%%| <AoE9sdVZnf|V0RISsQTjo>

plt.plot([1,2,3,4,5], [4,5,5,7,3])

# |%%--%%| <V0RISsQTjo|ePuTwJqfFB>

plt.plot(np.array([1,2,3,4,5]), np.array([4,5,5,7,3]))

# |%%--%%| <ePuTwJqfFB|eD1iNYRI4Q>

plt.plot([4,5,5,7,3])

# |%%--%%| <eD1iNYRI4Q|dTLRKSf1aL>

plt.plot([4,5,5,7,3], 'x');

# |%%--%%| <dTLRKSf1aL|CtpA2mSoFN>

def f(x): return x**2

# |%%--%%| <CtpA2mSoFN|4hGXrix80d>

xs = linspace(0,100); xs

# |%%--%%| <4hGXrix80d|kq73Nq0Xgx>

f(xs)

# |%%--%%| <kq73Nq0Xgx|yapJW8CwKx>

plt.plot(xs, f(xs))

# |%%--%%| <yapJW8CwKx|gj8EcMHMlS>

plt.plot(xs, f(xs), 'r+');

# |%%--%%| <gj8EcMHMlS|yd6cyNfFF0>

plt.plot(xs, 1 - f(xs), 'b', xs, f(xs)/2 - 1000, 'r--');

# |%%--%%| <yd6cyNfFF0|2gHrt2oBxR>

plt.plot(xs, f(xs), label='f(x)')
plt.plot(xs, 1 - f(xs), label='1-f(x)')
plt.legend(loc="center right")
plt.show()

# |%%--%%| <2gHrt2oBxR|j1liTnw2vd>

plt.plot(xs, f(xs), label='f(x)')
plt.plot(xs, 1 - f(xs), label='1-f(x)')
plt.legend(loc="best")
plt.show()

# |%%--%%| <j1liTnw2vd|TnAVGT5yHo>

plt.plot(xs, f(xs), label='f(x)')
plt.plot(xs, 1 - f(xs), label='1-f(x)')
plt.legend(loc="best")
plt.xlim([20, 80])
plt.show()

# |%%--%%| <TnAVGT5yHo|CPTdk0sH5c>

plt.plot(xs, f(xs), label=r'$\lambda^{3}$')
plt.plot(xs, 1 - f(xs), label=r'$\mathcal{N}$')
plt.legend(loc="best")
plt.xlim([20, 80])
plt.xlabel("hello")
plt.title("woohoo")
plt.show()

# |%%--%%| <CPTdk0sH5c|gUsTuUVp2V>

def f_1(x):
    return np.sqrt((1 - (np.abs(x) - 1)**2))
def f_2(x):
    return -3 * np.sqrt(1 - np.sqrt((np.abs(x)/2)))

x = np.linspace(-2, 2, 1000)
plt.plot(x, f_1(x), 'b-', label="bolja polovica")
plt.plot(x, f_2(x), 'r-', label="dobra polovica")
plt.xlim([-3, 3])
plt.ylim([-3, 1.5])
plt.xlabel("x")
plt.ylabel("y")
plt.legend(loc="lower right")
plt.show()

# |%%--%%| <gUsTuUVp2V|cZrOke8OJs>

plt.scatter([0, 1, 2, 0], [4, 5, 2, 1])
plt.show()

# |%%--%%| <cZrOke8OJs|dlIpr75uXA>

plt.scatter([0,1,2,0], [4, 5, 2, 1], s=200, marker='s');

# |%%--%%| <dlIpr75uXA|9WS2zMsNM2>

for c in 'rgb':
    plt.scatter(np.random.random(100), np.random.random(100), s=200, alpha=0.5, marker='o', c=c)

# |%%--%%| <9WS2zMsNM2|WvdSbvrQlZ>

plt.subplot(2,1,1)
plt.plot(xs, f(xs), label='f(x)', c="g")
plt.legend(loc="center right")

plt.subplot(2,1,2)
plt.plot(xs, f(xs), label='f(x)', c="r")
plt.legend(loc="center right")
plt.show()

# |%%--%%| <WvdSbvrQlZ|Cti0PlsjBj>

plt.subplot(2,3,1)
plt.plot(xs, f(xs), label='f(x)', c="g")
plt.legend(loc="center right")

plt.subplot(2,3,2)
plt.plot(xs, f(xs), label='f(x)', c="r")
plt.legend(loc="center right")

plt.subplot(2,3,3)
plt.plot(xs, f(xs), label='f(x)', c="m")
plt.legend(loc="center right")

plt.subplot(2,3,4)
plt.plot(xs, f(xs), label='f(x)', c="c")
plt.legend(loc="center right")

plt.subplot(2,3,5)
plt.plot(xs, f(xs), label='f(x)', c="y")
plt.legend(loc="center right")

plt.subplot(2,3,6)
plt.plot(xs, f(xs), label='f(x)', c="w")
plt.legend(loc="center right")
plt.show()
