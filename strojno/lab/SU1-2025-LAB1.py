r"""°°°
Sveučilište u Zagrebu  
Fakultet elektrotehnike i računarstva  
  
## Strojno učenje 1 2025./2026.  
http://www.fer.unizg.hr/predmet/struce1
°°°"""
# |%%--%%| <1yvf69TJV3|5FPXlx4XeQ>
r"""°°°
------------------------------

### Prva laboratorijska vježba: Linearna regresija

*Verzija: 1.0
Zadnji put ažurirano: 1. 10. 2021.*

(c) 2015-2026 Jan Šnajder, Domagoj Alagić 

------------------------------
°°°"""
# |%%--%%| <5FPXlx4XeQ|R9NyuREDB0>
r"""°°°
### Pravila predaje
Predajom vježbe potvrđujete sljedeće točke:
1. Niste od drugoga primili pomoć pri rješavanju vježbe;
2. Atribuirali ste dijelove koda koji su preuzeti s interneta referencirajući ih u komentarima;
3. Niste koristili dijelove koda s interneta koji su specifični za laboratorijsku vježbu;
4. Niste koristili UI-asistente za kodiranje kao npr. GitHub Copilot (uključivo alate generativne UI, kao što je ChatGPT).

**Povreda bilo kojeg od gornjih pravila smatra se prekršajem te povlači akademske sankcije.**
°°°"""
# |%%--%%| <R9NyuREDB0|2Ia5uHkKHZ>
r"""°°°
### Upute

Prva laboratorijska vježba sastoji se od sedam zadataka. U nastavku slijedite upute navedene u ćelijama s tekstom. Rješavanje vježbe svodi se na **dopunjavanje ove bilježnice**: umetanja ćelije ili više njih **ispod** teksta zadatka, pisanja odgovarajućeg kôda te evaluiranja ćelija. 

Osigurajte da u potpunosti **razumijete** kôd koji ste napisali. Kod predaje vježbe, morate biti u stanju na zahtjev asistenta (ili demonstratora) preinačiti i ponovno evaluirati Vaš kôd. Nadalje, morate razumjeti teorijske osnove onoga što radite, u okvirima onoga što smo obradili na predavanju. Ispod nekih zadataka možete naći i pitanja koja služe kao smjernice za bolje razumijevanje gradiva (**nemojte pisati** odgovore na pitanja u bilježnicu). Stoga se nemojte ograničiti samo na to da riješite zadatak, nego slobodno eksperimentirajte. To upravo i jest svrha ovih vježbi.

Vježbe trebate raditi **samostalno**. Možete se konzultirati s drugima o načelnom načinu rješavanja, ali u konačnici morate sami odraditi vježbu. U protivnome vježba nema smisla.
°°°"""
# |%%--%%| <2Ia5uHkKHZ|v1BdN1HQIq>

# Učitaj osnovne biblioteke...
import numpy as np
import sklearn
import matplotlib.pyplot as plt
%pylab inline

# |%%--%%| <v1BdN1HQIq|n7ygZDl47K>
r"""°°°
### 1. Jednostavna regresija
°°°"""
# |%%--%%| <n7ygZDl47K|FB2QyuhEwK>
r"""°°°
Zadan je skup primjera $\mathcal{D}=\{(x^{(i)},y^{(i)})\}_{i=1}^4 = \{(0,4),(1,1),(2,2),(4,5)\}$. Primjere predstavite matricom $\mathbf{X}$ dimenzija $N\times n$ (u ovom slučaju $4\times 1$) i vektorom oznaka $\textbf{y}$, dimenzija $N\times 1$ (u ovom slučaju $4\times 1$), na sljedeći način:

°°°"""
# |%%--%%| <FB2QyuhEwK|d0Dy7BP2PZ>

X = np.array([[0],[1],[2],[4]])
y = np.array([4,1,2,5])

# |%%--%%| <d0Dy7BP2PZ|G4gMjIRM1r>
r"""°°°
### (a)

Proučite funkciju [`PolynomialFeatures`](http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PolynomialFeatures.html) iz biblioteke `sklearn` i upotrijebite je za generiranje matrice dizajna $\mathbf{\Phi}$ koja ne koristi preslikavanje u prostor više dimenzije (samo će svakom primjeru biti dodane *dummy* jedinice; $m=n+1$).

°°°"""
# |%%--%%| <G4gMjIRM1r|u17qtcBQUX>

from sklearn.preprocessing import PolynomialFeatures
# Vaš kôd ovdje
poly = PolynomialFeatures(degree=1, include_bias=True)
matrix = poly.fit_transform(X)
matrix


# |%%--%%| <u17qtcBQUX|AEphw4iFDs>
r"""°°°
### (b)
°°°"""
# |%%--%%| <AEphw4iFDs|eckDwDZBUP>
r"""°°°
Upoznajte se s modulom [`linalg`](http://docs.scipy.org/doc/numpy/reference/routines.linalg.html). Izračunajte težine $\mathbf{w}$ modela linearne regresije kao $\mathbf{w}=(\mathbf{\Phi}^\intercal\mathbf{\Phi})^{-1}\mathbf{\Phi}^\intercal\mathbf{y}$. Zatim se uvjerite da isti rezultat možete dobiti izračunom pseudoinverza $\mathbf{\Phi}^+$ matrice dizajna, tj. $\mathbf{w}=\mathbf{\Phi}^+\mathbf{y}$, korištenjem funkcije [`pinv`](http://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.pinv.html).
°°°"""
# |%%--%%| <eckDwDZBUP|LQPvcWlMoI>

from numpy import linalg
# Vaš kôd ovdje
weights = linalg.matmul(
        linalg.matmul(
            linalg.inv(
                linalg.matmul(
                    linalg.matrix_transpose(matrix),
                    matrix
                )
            ), 
            linalg.matrix_transpose(matrix)
        ),
    y
)
weights_pinv = linalg.matmul(linalg.pinv(matrix), y)
print("weigths: ", weights)
print("weigths_pinv: ", weights_pinv)

# |%%--%%| <LQPvcWlMoI|jS8r84yNdz>
r"""°°°
Radi jasnoće, u nastavku je vektor $\mathbf{x}$ s dodanom *dummy* jedinicom $x_0=1$ označen kao $\tilde{\mathbf{x}}$.
°°°"""
# |%%--%%| <jS8r84yNdz|LuKcKw1ZWP>
r"""°°°
### (c)
°°°"""
# |%%--%%| <LuKcKw1ZWP|hHYWbYcTcs>
r"""°°°
Prikažite primjere iz $\mathcal{D}$ i funkciju $h(\tilde{\mathbf{x}})=\mathbf{w}^\intercal\tilde{\mathbf{x}}$. Izračunajte pogrešku učenja prema izrazu $E(h|\mathcal{D})=\frac{1}{2}\sum_{i=1}^N(\tilde{\mathbf{y}}^{(i)} - h(\tilde{\mathbf{x}}^{(i)}))^2$. Možete koristiti funkciju srednje kvadratne pogreške [`mean_squared_error`]( http://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html) iz modula [`sklearn.metrics`](http://scikit-learn.org/stable/modules/classes.html#module-sklearn.metrics).

**Q:** Gore definirana funkcija pogreške $E(h|\mathcal{D})$ i funkcija srednje kvadratne pogreške nisu posve identične. U čemu je razlika? Koja je "realnija"?
°°°"""
# |%%--%%| <hHYWbYcTcs|guWtwMsJnv>

from sklearn.metrics import mean_squared_error
# Vaš kôd ovdje

# |%%--%%| <guWtwMsJnv|3wRnMDrjGJ>
r"""°°°
### (d)
°°°"""
# |%%--%%| <3wRnMDrjGJ|VoqZl38K5y>
r"""°°°
Uvjerite se da za primjere iz $\mathcal{D}$ težine $\mathbf{w}$ ne možemo naći rješavanjem sustava $\mathbf{w}=\mathbf{\Phi}^{-1}\mathbf{y}$, već da nam doista treba pseudoinverz.

**Q:** Zašto je to slučaj? Bi li se problem mogao riješiti preslikavanjem primjera u višu dimenziju? Ako da, bi li to uvijek funkcioniralo, neovisno o skupu primjera $\mathcal{D}$? Pokažite na primjeru.
°°°"""
# |%%--%%| <VoqZl38K5y|TBZhj8q1g8>

# Vaš kôd ovdje

# |%%--%%| <TBZhj8q1g8|tl9vWldM8N>
r"""°°°
### (e) 
°°°"""
# |%%--%%| <tl9vWldM8N|V8zSjgEgMp>
r"""°°°
Proučite klasu [`LinearRegression`](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html) iz modula [`sklearn.linear_model`](http://scikit-learn.org/stable/modules/classes.html#module-sklearn.linear_model). Provjerite jesu li težine koje izračunava ta funkcija (dostupne pomoću atributa `coef_` i `intercept_`) jednake onima koje ste izračunali gore. Ako nisu, prilagodite kôd tako da jest.

**NB:** Obratite pozornost na to kako klase [`LinearRegression`](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html) i [`PolynomialFeatures`](http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PolynomialFeatures.html) koriste pomak i osigurajte da ga ne dodajete više puta.

Izračunajte predikcije modela (metoda `predict`) i uvjerite se da je pogreška učenja identična onoj koju ste ranije izračunali.
°°°"""
# |%%--%%| <V8zSjgEgMp|iUyfzByRQC>

from sklearn.linear_model import LinearRegression
# Vaš kôd ovdje

# |%%--%%| <iUyfzByRQC|ixBmXzmXgR>
r"""°°°
### 2. Polinomijalna regresija i utjecaj šuma
°°°"""
# |%%--%%| <ixBmXzmXgR|YNE8kdl9OO>
r"""°°°
### (a)

Razmotrimo sada regresiju na većem broju primjera. Definirajte funkciju `make_labels(X, f, noise=0)` koja uzima matricu neoznačenih primjera $\mathbf{X}_{N\times n}$ te generira vektor njihovih oznaka $\mathbf{y}_{N\times 1}$. Oznake se generiraju kao $y^{(i)} = f(x^{(i)})+\mathcal{N}(0,\sigma^2)$, gdje je $f:\mathbb{R}^n\to\mathbb{R}$ stvarna funkcija koja je generirala podatke (koja nam je u stvarnosti nepoznata), a $\sigma$ je standardna devijacija Gaussovog šuma, definirana parametrom `noise`. Za generiranje šuma možete koristiti funkciju [`numpy.random.normal`](https://numpy.org/doc/stable/reference/random/generated/numpy.random.normal.html). 

Generirajte skup za učenje od $N=50$ primjera uniformno distribuiranih u intervalu $[-5,5]$ pomoću funkcije $f(x) = 5 + x -2 x^2 -5 x^3$ uz šum  $\sigma=200$:
°°°"""
# |%%--%%| <YNE8kdl9OO|NeuHpiTRBU>

from numpy.random import normal
def make_labels(X, f, noise=0):
    # Vaš kôd ovdje

# |%%--%%| <NeuHpiTRBU|i3oia6m35Z>

def make_instances(x1, x2, N) :
    return np.array([np.array([x]) for x in np.linspace(x1,x2,N)])

# |%%--%%| <i3oia6m35Z|l607F3Dykr>

# Vaš kôd ovdje

# |%%--%%| <l607F3Dykr|4cJjdeUrJ1>
r"""°°°
Prikažite taj skup funkcijom [`scatter`](http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.scatter).
°°°"""
# |%%--%%| <4cJjdeUrJ1|5CoeVg6DJM>

# Vaš kôd ovdje

# |%%--%%| <5CoeVg6DJM|FoW7laJMFZ>
r"""°°°
### (b)
°°°"""
# |%%--%%| <FoW7laJMFZ|0zbwTovyFT>
r"""°°°
Trenirajte model polinomijalne regresije stupnja $d=3$. Na istom grafikonu prikažite naučeni model $h(\mathbf{x})=\mathbf{w}^\intercal\tilde{\mathbf{x}}$ i primjere za učenje. Izračunajte pogrešku učenja modela.
°°°"""
# |%%--%%| <0zbwTovyFT|E49y0QsAzj>

# Vaš kôd ovdje

# |%%--%%| <E49y0QsAzj|OBUiWHDUPp>
r"""°°°
### 3. Odabir modela
°°°"""
# |%%--%%| <OBUiWHDUPp|ARyCjQt0p8>
r"""°°°
### (a)

Na skupu podataka iz zadatka 2 trenirajte pet modela linearne regresije $\mathcal{H}_d$ različite složenosti, gdje je $d$ stupanj polinoma, $d\in\{1,3,5,10,20\}$. Prikažite na istome grafikonu skup za učenje i funkcije $h_d(\mathbf{x})$ za svih pet modela (preporučujemo koristiti `plot` unutar `for` petlje). Izračunajte pogrešku učenja svakog od modela.

**Q:** Koji model ima najmanju pogrešku učenja i zašto?
°°°"""
# |%%--%%| <ARyCjQt0p8|w57CavW9ul>

# Vaš kôd ovdje

# |%%--%%| <w57CavW9ul|52ZRtQd0KO>
r"""°°°
### (b)
°°°"""
# |%%--%%| <52ZRtQd0KO|a0KADyxBRi>
r"""°°°
Razdvojite skup primjera iz zadatka 2 pomoću funkcije [`model_selection.train_test_split`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html) na skup za učenja i skup za ispitivanje u omjeru 1:1. Prikažite na jednom grafikonu pogrešku učenja i ispitnu pogrešku za modele polinomijalne regresije $\mathcal{H}_d$, sa stupnjem polinoma $d$ u rasponu $d\in [1,2,\ldots,20]$. Budući da kvadratna pogreška brzo raste za veće stupnjeve polinoma, umjesto da iscrtate izravno iznose pogrešaka, iscrtajte njihove logaritme.

**NB:** Podjela na skupa za učenje i skup za ispitivanje mora za svih dvadeset modela biti identična.

**Q:** Je li rezultat u skladu s očekivanjima? Koji biste model odabrali i zašto?

**Q:** Pokrenite iscrtavanje više puta. U čemu je problem? Bi li problem bio jednako izražen kad bismo imali više primjera? Zašto?
°°°"""
# |%%--%%| <a0KADyxBRi|7B8ZqQrYuH>

from sklearn.model_selection import train_test_split
# Vaš kôd ovdje

# |%%--%%| <7B8ZqQrYuH|WZ9fRz4rbo>
r"""°°°
### (c)
°°°"""
# |%%--%%| <WZ9fRz4rbo|aV3kK7rQR9>
r"""°°°
Točnost modela ovisi o (1) njegovoj složenosti (stupanj $d$ polinoma), (2) broju primjera $N$, i (3) količini šuma. Kako biste to analizirali, nacrtajte grafikone pogrešaka kao u 3b, ali za različit $N\in$ (trećina, dvije trećine, sve) i količine šuma $\sigma\in\{100,200,500\}$ (ukupno 9 grafikona). Upotrijebite funkciju [`subplots`](http://matplotlib.org/examples/pylab_examples/subplots_demo.html) kako biste pregledno posložili grafikone u tablicu $3\times 3$. Podatci se generiraju na isti način kao u zadatku 2.

**NB:** Pobrinite se da svi grafikoni budu generirani nad usporedivim skupovima podataka, na sljedeći način. Generirajte najprije svih 1000 primjera, podijelite ih na skupove za učenje i skupove za ispitivanje (dva skupa od po 500 primjera). Zatim i od skupa za učenje i od skupa za ispitivanje načinite tri različite verzije, svaka s drugačijom količinom šuma (ukupno 2x3=6 verzija podataka). Kako bi simulirali veličinu skupa podataka, od tih dobivenih 6 skupova podataka uzorkujte trećinu, dvije trećine i sve podatke. Time ste dobili 18 skupova podataka -- skup za učenje i za testiranje za svaki od devet grafova.
°°°"""
# |%%--%%| <aV3kK7rQR9|AaaHTAXkMr>

# Vaš kôd ovdje

# |%%--%%| <AaaHTAXkMr|lB6UQoQZei>
r"""°°°
***Q:*** Jesu li rezultati očekivani? Obrazložite.
°°°"""
# |%%--%%| <lB6UQoQZei|sFnXsVxfOh>
r"""°°°
### 4. Regularizirana regresija
°°°"""
# |%%--%%| <sFnXsVxfOh|ch6lxqpqWf>
r"""°°°
### (a)

U gornjim eksperimentima nismo koristili **regularizaciju**. Vratimo se najprije na primjer iz zadatka 1. Na primjerima iz tog zadatka izračunajte težine $\mathbf{w}$ za polinomijalni regresijski model stupnja $d=3$ uz L2-regularizaciju (tzv. *ridge regression*), prema izrazu $\mathbf{w}=(\mathbf{\Phi}^\intercal\mathbf{\Phi}+\lambda\mathbf{I})^{-1}\mathbf{\Phi}^\intercal\mathbf{y}$. Napravite izračun težina za regularizacijske faktore $\lambda=0$, $\lambda=1$ i $\lambda=10$ te usporedite dobivene težine.

**Q:** Kojih je dimenzija matrica koju treba invertirati?

**Q:** Po čemu se razlikuju dobivene težine i je li ta razlika očekivana? Obrazložite.
°°°"""
# |%%--%%| <ch6lxqpqWf|XQOOQhO7zX>

# Vaš kôd ovdje

# |%%--%%| <XQOOQhO7zX|ua0y6UxJn8>
r"""°°°
### (b)
°°°"""
# |%%--%%| <ua0y6UxJn8|b1i3V3naBN>
r"""°°°
Proučite klasu [`Ridge`](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html#sklearn.linear_model.Ridge) iz modula [`sklearn.linear_model`](http://scikit-learn.org/stable/modules/classes.html#module-sklearn.linear_model), koja implementira L2-regularizirani regresijski model. Parametar $\alpha$ odgovara parametru $\lambda$. Primijenite model na istim primjerima kao u prethodnom zadatku i ispišite težine $\mathbf{w}$ (atributi `coef_` i `intercept_`). Ponovno, pripazite na pomak.

**Q:** Jesu li težine identične onima iz zadatka 4a? Ako nisu, objasnite zašto je to tako i kako biste to popravili.
°°°"""
# |%%--%%| <b1i3V3naBN|IuGJwYmJwS>

from sklearn.linear_model import Ridge
# Vaš kôd ovdje

# |%%--%%| <IuGJwYmJwS|g8BYviPu8A>
r"""°°°
### (c)

Vratimo se na slučaj $N=50$ slučajno generiranih primjera iz zadatka 2. Trenirajte modele polinomijalne regresije $\mathcal{H}_{\lambda,d}$ za $\lambda\in\{0,100\}$ i $d\in\{2,10\}$ (ukupno četiri modela). Skicirajte pripadne funkcije $h(\mathbf{x})$ i primjere (na jednom grafikonu; preporučujemo koristiti `plot` unutar `for` petlje).

**Q:** Jesu li rezultati očekivani? Obrazložite.
°°°"""
# |%%--%%| <g8BYviPu8A|xLWD1KU0w3>

# Vaš kôd ovdje

# |%%--%%| <xLWD1KU0w3|yFmokFFWFM>
r"""°°°
### (d)

Kao u zadataku 3b, razdvojite primjere na skup za učenje i skup za ispitivanje u omjeru 1:1. Prikažite krivulje logaritama pogreške učenja i ispitne pogreške u ovisnosti za model $\mathcal{H}_{d=10,\lambda}$, podešavajući faktor regularizacije $\lambda$ u rasponu $\lambda\in\{0,1,\dots,50\}$.

**Q:** Kojoj strani na grafikonu odgovara područje prenaučenosti, a kojoj podnaučenosti? Zašto?

**Q:** Koju biste vrijednosti za $\lambda$ izabrali na temelju ovih grafikona i zašto?

°°°"""
# |%%--%%| <yFmokFFWFM|g1JEJbzRjf>

# Vaš kôd ovdje

# |%%--%%| <g1JEJbzRjf|tgOBVjwbL0>
r"""°°°
### 5. L1-regularizacija i L2-regularizacija
°°°"""
# |%%--%%| <tgOBVjwbL0|rbIw48JnEb>
r"""°°°
Svrha regularizacije jest potiskivanje težina modela $\mathbf{w}$ prema nuli, kako bi model bio što jednostavniji. Složenost modela može se okarakterizirati normom pripadnog vektora težina $\mathbf{w}$, i to tipično L2-normom ili L1-normom. Za jednom trenirani model možemo izračunati i broj ne-nul značajki, ili L0-normu, pomoću sljedeće funkcije koja prima vektor težina $\mathbf{w}$:
°°°"""
# |%%--%%| <rbIw48JnEb|6MYsbyjVEv>

def nonzeroes(coef, tol=1e-6): 
    return len(coef) - len(coef[np.isclose(0, coef, atol=tol)])

# |%%--%%| <6MYsbyjVEv|98FSAb7M1j>
r"""°°°
### (a)

Za ovaj zadatak upotrijebite skup za učenje i skup za testiranje iz zadatka 3b. Trenirajte modele **L2-regularizirane** polinomijalne regresije stupnja $d=5$, mijenjajući hiperparametar $\lambda$ u rasponu $\{1,2,\dots,100\}$. Za svaki od treniranih modela izračunajte L{0,1,2}-norme vektora težina $\mathbf{w}$ te ih prikažite kao funkciju od $\lambda$. Pripazite što točno šaljete u funkciju za izračun normi.

**Q:** Objasnite oblik obiju krivulja. Hoće li krivulja za $\|\mathbf{w}\|_2$ doseći nulu? Zašto? Je li to problem? Zašto?

**Q:** Za $\lambda=100$, koliki je postotak težina modela jednak nuli, odnosno koliko je model rijedak?
°°°"""
# |%%--%%| <98FSAb7M1j|3jPFrpVRUB>

from sklearn.linear_model import Ridge
# Vaš kôd ovdje

# |%%--%%| <3jPFrpVRUB|Ou8XKEWFVS>
r"""°°°
### (b)
°°°"""
# |%%--%%| <Ou8XKEWFVS|mqcX6ifU6k>
r"""°°°
Glavna prednost L1-regularizirane regresije (ili *LASSO regression*) nad L2-regulariziranom regresijom jest u tome što L1-regularizirana regresija rezultira **rijetkim modelima** (engl. *sparse models*), odnosno modelima kod kojih su mnoge težine pritegnute na nulu. Pokažite da je to doista tako, ponovivši gornji eksperiment s **L1-regulariziranom** regresijom, implementiranom u klasi  [`Lasso`](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html) u modulu [`sklearn.linear_model`](http://scikit-learn.org/stable/modules/classes.html#module-sklearn.linear_model).
°°°"""
# |%%--%%| <mqcX6ifU6k|1urKHEkHDr>

from sklearn.linear_model import Lasso
# Vaš kôd ovdje

# |%%--%%| <1urKHEkHDr|20ubttGrlb>
r"""°°°
### 6. Značajke različitih skala
°°°"""
# |%%--%%| <20ubttGrlb|l59s6uDk3B>
r"""°°°
Često se u praksi možemo susreti sa podatcima u kojima sve značajke nisu jednakih magnituda. Primjer jednog takvog skupa je regresijski skup podataka `grades` u kojem se predviđa prosjek ocjena studenta na studiju (1--5) na temelju dvije značajke: bodova na prijamnom ispitu (1--3000) i prosjeka ocjena u srednjoj školi. Prosjek ocjena na studiju izračunat je kao težinska suma ove dvije značajke uz dodani šum.

Koristite sljedeći kôd kako biste generirali ovaj skup podataka.
°°°"""
# |%%--%%| <l59s6uDk3B|xmpeRw28Zc>

n_data_points = 500
np.random.seed(69)

# Generiraj podatke o bodovima na prijamnom ispitu koristeći normalnu razdiobu i ograniči ih na interval [1, 3000].
exam_score = np.random.normal(loc=1500.0, scale = 500.0, size = n_data_points) 
exam_score = np.round(exam_score)
exam_score[exam_score > 3000] = 3000
exam_score[exam_score < 0] = 0

# Generiraj podatke o ocjenama iz srednje škole koristeći normalnu razdiobu i ograniči ih na interval [1, 5].
grade_in_highschool = np.random.normal(loc=3, scale = 2.0, size = n_data_points)
grade_in_highschool[grade_in_highschool > 5] = 5
grade_in_highschool[grade_in_highschool < 1] = 1

# Matrica dizajna.
grades_X = np.array([exam_score,grade_in_highschool]).T

# Završno, generiraj izlazne vrijednosti.
rand_noise = np.random.normal(loc=0.0, scale = 0.5, size = n_data_points)
exam_influence = 0.9
grades_y = ((exam_score / 3000.0) * (exam_influence) + (grade_in_highschool / 5.0) \
            * (1.0 - exam_influence)) * 5.0 + rand_noise
grades_y[grades_y < 1] = 1
grades_y[grades_y > 5] = 5

# |%%--%%| <xmpeRw28Zc|bjDJALvYGz>
r"""°°°
### a)
°°°"""
# |%%--%%| <bjDJALvYGz|aBYz9nagSu>
r"""°°°
Iscrtajte ovisnost ciljne vrijednosti (y-os) o prvoj i o drugoj značajki (x-os). Iscrtajte dva odvojena grafa.
°°°"""
# |%%--%%| <aBYz9nagSu|N1lyF0H7MQ>

# Vaš kôd ovdje

# |%%--%%| <N1lyF0H7MQ|oHVRyz55kj>
r"""°°°
### b)
°°°"""
# |%%--%%| <oHVRyz55kj|78Rf4shGlk>
r"""°°°
Naučite model L2-regularizirane regresije ($\lambda = 0.01$), na podacima `grades_X` i `grades_y`:
°°°"""
# |%%--%%| <78Rf4shGlk|BkGi8bhqIT>

# Vaš kôd ovdje

# |%%--%%| <BkGi8bhqIT|2NCRTTnVaU>
r"""°°°
Sada ponovite gornji eksperiment, ali prvo skalirajte podatke `grades_X` i `grades_y` i spremite ih u varijable `grades_X_fixed` i `grades_y_fixed`. Za tu svrhu, koristite [`StandardScaler`](http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html).
°°°"""
# |%%--%%| <2NCRTTnVaU|oXe9wUrCGk>

from sklearn.preprocessing import StandardScaler
# Vaš kôd ovdje

# |%%--%%| <oXe9wUrCGk|q8uyEtfYom>
r"""°°°
**Q:** Gledajući grafikone iz podzadatka (a), koja značajka bi trebala imati veću magnitudu, odnosno važnost pri predikciji prosjeka na studiju? Odgovaraju li težine Vašoj intuiciji? Objasnite.  
°°°"""
# |%%--%%| <q8uyEtfYom|kNOEKioGDn>
r"""°°°
### 7. Multikolinearnost
°°°"""
# |%%--%%| <kNOEKioGDn|qqzDEwnMVY>
r"""°°°
### a)
°°°"""
# |%%--%%| <qqzDEwnMVY|yge2BjfszS>
r"""°°°
Izradite skup podataka `grades_X_fixed_colinear` tako što ćete u skupu `grades_X_fixed` iz
zadatka *7b* duplicirati zadnji stupac (ocjenu iz srednje škole). Time smo efektivno uveli savršenu multikolinearnost.
°°°"""
# |%%--%%| <yge2BjfszS|EXTYGaZL5F>

# Vaš kôd ovdje

# |%%--%%| <EXTYGaZL5F|lAYRqcVLOK>
r"""°°°
Ponovno, naučite na ovom skupu L2-regularizirani model regresije ($\lambda = 0.01$).
°°°"""
# |%%--%%| <lAYRqcVLOK|UgUjKZoReB>

# Vaš kôd ovdje

# |%%--%%| <UgUjKZoReB|FVOtkPYWkA>
r"""°°°
**Q:** Usporedite iznose težina s onima koje ste dobili u zadatku *7b*. Što se dogodilo?
°°°"""
# |%%--%%| <FVOtkPYWkA|z1Czf3mR7t>
r"""°°°
### b)
°°°"""
# |%%--%%| <z1Czf3mR7t|frp2rlufok>
r"""°°°
Slučajno uzorkujte 50% elemenata iz skupa `grades_X_fixed_colinear` i naučite dva modela L2-regularizirane regresije, jedan s $\lambda=0.01$ i jedan s $\lambda=1000$). Ponovite ovaj pokus 10 puta (svaki put s drugim podskupom od 50% elemenata).  Za svaki model, ispišite dobiveni vektor težina u svih 10 ponavljanja te ispišite standardnu devijaciju vrijednosti svake od težina (ukupno šest standardnih devijacija, svaka dobivena nad 10 vrijednosti).
°°°"""
# |%%--%%| <frp2rlufok|8wYSieBaPG>

# Vaš kôd ovdje

# |%%--%%| <8wYSieBaPG|tFHql3rvJ9>
r"""°°°
**Q:** Kako regularizacija utječe na stabilnost težina?  
**Q:** Jesu li koeficijenti jednakih magnituda kao u prethodnom pokusu? Objasnite zašto.
°°°"""

