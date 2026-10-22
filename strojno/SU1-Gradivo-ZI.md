# Strojno Učenje 1 - Gradivo za Ispit

**Fakultet elektrotehnike i računarstva, Sveučilište u Zagrebu**  
**Akademska godina 2025./2026.**

---

## Sadržaj

- [Cjelina 13: Procjena parametara](#cjelina-13-procjena-parametara)
- [Cjelina 14: Procjena parametara II](#cjelina-14-procjena-parametara-ii-mle-i-map)
- [Cjelina 15: Bayesov klasifikator](#cjelina-15-bayesov-klasifikator)
- [Cjelina 16: Bayesov klasifikator II](#cjelina-16-bayesov-klasifikator-ii)
- [Cjelina 17: Probabilistički grafički modeli](#cjelina-17-probabilistički-grafički-modeli)
- [Cjelina 18: Probabilistički grafički modeli II](#cjelina-18-probabilistički-grafički-modeli-ii-zaključivanje-i-učenje)
- [Cjelina 19: Grupiranje](#cjelina-19-grupiranje-clustering)
- [Cjelina 20: Grupiranje II](#cjelina-20-grupiranje-ii)
- [Cjelina 21: Vrednovanje modela](#cjelina-21-vrednovanje-modela)

---

## Pregled laboratorijske vježbe 4

### Što se traži u labosu:

| Zadatak | Tema            | Ključne vještine                               |
| ------- | --------------- | ---------------------------------------------- |
| 1       | ML procjena     | Implementacija Bernoullijeve izglednosti       |
| 2       | MAP procjena    | Beta distribucija, usporedba ML i MAP          |
| 3       | Iris analiza    | Log-izglednost Gaussa, korelacija, kovarijanca |
| 4       | Bayesove mreže  | pgmpy paket, konstrukcija mreže, inference     |
| 5       | Explaining away | Demonstracija fenomena                         |
| 6       | K-means         | Metoda lakta, silueta, pretpostavke algoritma  |
| 7       | GMM             | Usporedba s k-means                            |
| 8       | Vrednovanje     | Randov indeks                                  |

---

## Cjelina 13: Procjena parametara

> **🔬 LABOS:** Ova cjelina se ispituje u zadacima 1, 2 i 3 laboratorijske vježbe!

### Zašto probabilistički modeli?

**Tri ključne prednosti:**

1. **Teorijska podloga** - temelje se na teoriji vjerojatnosti
2. **Pouzdanost predikcije** - daju informaciju koliko je klasifikacija pouzdana
3. **Apriorno znanje** - mogu ugraditi prethodno znanje o problemu

> ⚠️ **VAŽNO ZA ISPIT:** Procjena parametara = učenje/treniranje modela u terminologiji strojnog učenja!

---

### Slučajne varijable - osnove

#### Diskretna vs. kontinuirana

| Vrsta            | Definicija                         | Primjer        |
| ---------------- | ---------------------------------- | -------------- |
| **Diskretna**    | Konačan/prebrojiv skup vrijednosti | Oznaka klase y |
| **Kontinuirana** | Neprekidan skup vrijednosti        | Prosjek ocjena |

**Diskretna:** $P(x_i) \geq 0$ i $\sum_i P(x_i) = 1$

**Kontinuirana:** Funkcija gustoće vjerojatnosti (PDF): $p(x) \geq 0$ i $\int_{-\infty}^{\infty} p(x) dx = 1$

---

### Očekivanje, varijanca, kovarijanca

#### Očekivanje (srednja vrijednost)

$$E[X] = \sum_x x \cdot P(x) \quad \text{(diskretna)}$$
$$E[X] = \int_{-\infty}^{\infty} x \cdot p(x) dx \quad \text{(kontinuirana)}$$

#### Varijanca

$$Var(X) = \sigma_X^2 = E[(X - E[X])^2] = E[X^2] - E[X]^2$$

#### Kovarijanca

$$Cov(X, Y) = \sigma_{X,Y} = E[(X - E[X])(Y - E[Y])]$$

> **VAŽNO:** $Cov(X, X) = Var(X)$

#### Pearsonov koeficijent korelacije

$$\rho_{X,Y} = \frac{Cov(X, Y)}{\sqrt{Var(X) \cdot Var(Y)}} = \frac{\sigma_{X,Y}}{\sigma_X \sigma_Y}$$

| Vrijednost  | Značenje                                                 |
| ----------- | -------------------------------------------------------- |
| $\rho = 1$  | Savršena pozitivna linearna ovisnost                     |
| $\rho = -1$ | Savršena negativna linearna ovisnost                     |
| $\rho = 0$  | Nema linearne ovisnosti (ALI može postojati nelinearna!) |

> ⚠️ **ZAMKA NA ISPITU:** Pearsonov koeficijent mjeri **samo linearnu** zavisnost! Varijable mogu biti nelinearno zavisne, a imati $\rho = 0$.

---

### Kovarijacijska matrica

Za višedimenzijsku varijablu $\mathbf{X} = (X_1, ..., X_n)$:

$$\Sigma_{ij} = Cov(X_i, X_j)$$

$$\Sigma = \begin{pmatrix} Var(X_1) & Cov(X_1, X_2) & \cdots \\ Cov(X_2, X_1) & Var(X_2) & \cdots \\ \vdots & \vdots & \ddots \end{pmatrix}$$

**Svojstva:**

- Kvadratna i **simetrična** matrica
- Na dijagonali: **varijance**
- Izvan dijagonale: **kovarijance**

**Specijalni slučajevi:**

| Slučaj                | Oblik matrice                           | Značenje                           |
| --------------------- | --------------------------------------- | ---------------------------------- |
| Nezavisne varijable   | Dijagonalna $\Sigma = diag(\sigma_i^2)$ | Nema korelacije                    |
| Izotropna kovarijanca | $\Sigma = \sigma^2 I$                   | Jednake varijance, nema korelacije |

> ⚠️ **VAŽNO:** Kovarijacijska matrica mora biti **pozitivno definitna** da bi imala inverz!

---

### Nezavisnost varijabli

Dvije varijable X i Y su **nezavisne** ako i samo ako:
$$P(X, Y) = P(X) \cdot P(Y)$$

**Ključna razlika:**

- Nezavisne varijable → **uvijek** nekorelirane ($\rho = 0$)
- Nekorelirane varijable → **NE MORAJU** biti nezavisne!

---

### Osnovne vjerojatnosne distribucije

#### 1. Bernoullijeva distribucija (binarna varijabla)

$$P(X = x | \mu) = \mu^x (1-\mu)^{1-x}$$

- **Parametar:** $\mu$ (vjerojatnost da $x = 1$)
- **Očekivanje:** $E[X] = \mu$
- **Varijanca:** $Var(X) = \mu(1-\mu)$

> **🔬 LABOS zadatak 1:** Implementacija funkcije izglednosti za Bernoullijeve varijable!

#### 2. Kategorička (multinulijeva) distribucija

Za K mogućih vrijednosti, koristi se **one-hot encoding**: $\mathbf{x} = (x_1, ..., x_K)$

$$P(X = \mathbf{x} | \boldsymbol{\mu}) = \prod_{k=1}^{K} \mu_k^{x_k}$$

gdje $\sum_k \mu_k = 1$

#### 3. Gaussova (normalna) distribucija

**Univarijatna:**
$$p(x | \mu, \sigma^2) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$$

**Multivarijatna:**
$$p(\mathbf{x} | \boldsymbol{\mu}, \Sigma) = \frac{1}{(2\pi)^{n/2}|\Sigma|^{1/2}} \exp\left(-\frac{1}{2}(\mathbf{x}-\boldsymbol{\mu})^T \Sigma^{-1}(\mathbf{x}-\boldsymbol{\mu})\right)$$

> **🔬 LABOS zadatak 3:** Implementacija log-izglednosti za Gaussovu distribuciju!

---

### Procjena parametara

**Ključni pojmovi:**

| Pojam            | Definicija                            |
| ---------------- | ------------------------------------- |
| **Populacija**   | Svi podaci                            |
| **Uzorak**       | Konačan podskup populacije            |
| **i.i.d.**       | Nezavisno i identično distribuirano   |
| **Statistika**   | Funkcija slučajnog uzorka             |
| **Procjenitelj** | Statistika koja procjenjuje parametar |
| **Procjena**     | Konkretna vrijednost procjenitelja    |

#### Pristranost procjenitelja

$$b_\theta(\Theta) = E[\Theta] - \theta$$

**Nepristran procjenitelj:** $E[\Theta] = \theta$ (pristranost = 0)

#### Primjer: Procjena srednje vrijednosti i varijance

**Procjenitelj srednje vrijednosti (NEPRISTRAN):**
$$\hat{\mu} = \frac{1}{N} \sum_i x^{(i)}$$

**Procjenitelj varijance (PRISTRAN!):**
$$\hat{\sigma}^2 = \frac{1}{N} \sum_i (x^{(i)} - \hat{\mu})^2$$

Pristranost: $E[\hat{\sigma}^2] = \frac{N-1}{N}\sigma^2$ → **podcjenjuje** varijancu!

**Nepristran procjenitelj varijance (Besselova korekcija):**
$$\hat{\sigma}^2_{nepr.} = \frac{1}{N-1} \sum_i (x^{(i)} - \hat{\mu})^2$$

> ⚠️ **VAŽNO ZA ISPIT:** Zašto dijelimo s $N-1$ a ne $N$? Zato što je procjenitelj s $N$ **pristran** i podcjenjuje varijancu!

---

### Metode za izvođenje procjenitelja

1. **MLE** - Maximum Likelihood Estimator (Cjelina 14)
2. **MAP** - Maximum A Posteriori (Cjelina 14)
3. **Bayesovski procjenitelj** (nije na ovom kolegiju)

---

### 📝 Moguća ispitna pitanja s odgovorima

**1. Što je razlika između očekivanja i varijance?**

> **Očekivanje** ($E[X]$) je prosječna/srednja vrijednost slučajne varijable - govori nam oko koje vrijednosti se varijabla "vrti". **Varijanca** ($Var(X)$) mjeri koliko vrijednosti varijable variraju (rasipaju se) oko te srednje vrijednosti. Očekivanje nam daje "centar", a varijanca nam govori koliko su podaci rašireni oko tog centra.

---

**2. Što mjeri Pearsonov koeficijent korelacije i koje su njegove granice?**

> Pearsonov koeficijent korelacije ($\rho_{X,Y}$) mjeri **stupanj linearne zavisnosti** između dvije varijable. Granice su **-1 do +1**:
>
> - $\rho = +1$: savršena pozitivna linearna ovisnost (kad X raste, Y raste proporcionalno)
> - $\rho = -1$: savršena negativna linearna ovisnost (kad X raste, Y pada proporcionalno)
> - $\rho = 0$: nema linearne ovisnosti
>
> **VAŽNO:** Mjeri SAMO linearnu zavisnost - varijable mogu biti nelinearno zavisne, a imati $\rho = 0$!

---

**3. Mogu li nekorelirane varijable biti zavisne? Obrazloži.**

> **DA, mogu!** Pearsonov koeficijent korelacije mjeri samo **linearnu** zavisnost. Ako je $\rho = 0$, to znači da nema linearne veze, ali može postojati **nelinearna zavisnost**.
>
> **Primjer:** Neka je $Y = X^2$ gdje je $X$ simetrično distribuiran oko nule (npr. $X \in \{-2, -1, 0, 1, 2\}$). Tada je $\rho_{X,Y} = 0$ jer je veza parabolična (simetrična po Y osi), ali Y očito ovisi o X!
>
> **Obrat vrijedi:** Ako su varijable **nezavisne**, tada su **uvijek** nekorelirane ($\rho = 0$).

---

**4. Zašto je procjenitelj varijance s $\frac{1}{N}$ pristran?**

> Procjenitelj $\hat{\sigma}^2 = \frac{1}{N}\sum(x^{(i)} - \hat{\mu})^2$ je **pristran** jer koristi procijenjenu srednju vrijednost $\hat{\mu}$ umjesto prave $\mu$.
>
> Može se pokazati da je $E[\hat{\sigma}^2] = \frac{N-1}{N}\sigma^2 \neq \sigma^2$.
>
> Procjenitelj **podcjenjuje** pravu varijancu (pristranost je negativna: $-\frac{\sigma^2}{N}$).
>
> **Rješenje:** Koristi se **Besselova korekcija** - dijeli se s $N-1$ umjesto $N$:
> $$\hat{\sigma}^2_{nepristran} = \frac{1}{N-1}\sum(x^{(i)} - \hat{\mu})^2$$
>
> Intuitivno: gubimo jedan "stupanj slobode" jer smo $\mu$ procijenili iz istih podataka.

---

**5. Kako izgleda kovarijacijska matrica za nezavisne varijable?**

> Za nezavisne varijable, kovarijacijska matrica je **dijagonalna matrica**:
> $$\Sigma = \begin{pmatrix} \sigma_1^2 & 0 & \cdots & 0 \\ 0 & \sigma_2^2 & \cdots & 0 \\ \vdots & \vdots & \ddots & \vdots \\ 0 & 0 & \cdots & \sigma_n^2 \end{pmatrix}$$
>
> Na dijagonali su varijance pojedinih varijabli, a izvan dijagonale su **nule** jer je $Cov(X_i, X_j) = 0$ za $i \neq j$ (nezavisne varijable su nekorelirane).
>
> **Specijalni slučaj - izotropna kovarijanca:** Ako sve varijable imaju istu varijancu $\sigma^2$, tada je $\Sigma = \sigma^2 I$ (skalar puta jedinična matrica).

---

**6. Napiši Bernoullijevu distribuciju i njezine parametre.**

> **Bernoullijeva distribucija** modelira binarnu slučajnu varijablu ($x \in \{0, 1\}$):
> $$P(X = x | \mu) = \mu^x (1-\mu)^{1-x}$$
>
> **Parametar:** $\mu \in [0, 1]$ - vjerojatnost da $X = 1$
>
> **Svojstva:**
>
> - $P(X = 1) = \mu$
> - $P(X = 0) = 1 - \mu$
> - Očekivanje: $E[X] = \mu$
> - Varijanca: $Var(X) = \mu(1-\mu)$
>
> **Primjer:** Bacanje novčića - $\mu = 0.5$ za pošten novčić.

---

**7. Što znači i.i.d. pretpostavka?**

> **i.i.d.** = **independently and identically distributed** (nezavisno i identično distribuirano)
>
> Dvije ključne pretpostavke o uzorku $(X_1, X_2, ..., X_N)$:
>
> 1. **Nezavisno (independently):** Ishod jedne varijable NE utječe na ishod druge. Matematički: $P(X_1, X_2, ..., X_N) = P(X_1) \cdot P(X_2) \cdot ... \cdot P(X_N)$
> 2. **Identično distribuirano (identically distributed):** Sve varijable dolaze iz **iste distribucije** s istim parametrima (jer su iz iste populacije).
>
> **Zašto je važno?** Ova pretpostavka je temeljna za većinu algoritama strojnog učenja - omogućuje nam da iz uzorka zaključujemo o cijeloj populaciji.

---

## Cjelina 14: Procjena parametara II (MLE i MAP)

> **🔬 LABOS:** Ova cjelina se ispituje u zadacima 1 i 2 laboratorijske vježbe!

---

### Funkcija izglednosti (Likelihood Function)

**Ključna ideja:** Vjerojatnost podataka $D$ za dane parametre $\theta$, ali promatrana kao funkcija od $\theta$!

$$\mathcal{L}(\theta | D) = p(D | \theta) = \prod_{i=1}^{N} p(x^{(i)} | \theta)$$

> ⚠️ **VAŽNO:** Izglednost **NIJE** vjerojatnost parametara! To je vjerojatnost **podataka** pod modelom s parametrima $\theta$.

**Za Bernoullijevu varijablu** (m uspjeha od N pokušaja):
$$\mathcal{L}(\mu | D) = \mu^m (1-\mu)^{N-m}$$

> **🔬 LABOS zadatak 1:** Implementacija ove funkcije!

---

### Procjenitelj MLE (Maximum Likelihood Estimator)

**Ideja:** Nađi parametre koji maksimiziraju vjerojatnost da smo dobili upravo taj uzorak!

$$\hat{\theta}_{MLE} = \arg\max_{\theta} \mathcal{L}(\theta | D) = \arg\max_{\theta} \ln \mathcal{L}(\theta | D)$$

#### MLE za osnovne distribucije

| Distribucija    | MLE procjenitelj                                                                                             |
| --------------- | ------------------------------------------------------------------------------------------------------------ |
| **Bernoulli**   | $\hat{\mu}_{MLE} = \frac{m}{N}$ (relativna frekvencija)                                                      |
| **Kategorička** | $\hat{\mu}_{k,MLE} = \frac{N_k}{N}$                                                                          |
| **Gaussova**    | $\hat{\mu}_{MLE} = \frac{1}{N}\sum x^{(i)}$, $\hat{\sigma}^2_{MLE} = \frac{1}{N}\sum(x^{(i)} - \hat{\mu})^2$ |

> ⚠️ **PROBLEM MLE:** Sklon je **prenaučenosti**, posebno kad imamo malo podataka!

**Primjer problema:** Ako od 5 bacanja novčića dobijemo 0 glava → MLE daje $\mu = 0$ (nemoguće dobiti glavu!) - to je očito preekstremno.

---

### Procjenitelj MAP (Maximum A Posteriori)

**Ideja:** Kombiniraj informacije iz podataka s **apriornim znanjem** o parametrima!

Koristi **Bayesovo pravilo**:
$$p(\theta | D) = \frac{p(D | \theta) \cdot p(\theta)}{p(D)}$$

**MAP procjenitelj:**
$$\hat{\theta}_{MAP} = \arg\max_{\theta} p(\theta | D) = \arg\max_{\theta} \underbrace{p(D | \theta)}_{\text{izglednost}} \cdot \underbrace{p(\theta)}_{\text{prior}}$$

> **Usporedba MLE vs MAP:**
>
> - **MLE:** $\hat{\theta}_{MLE} = \arg\max_{\theta} p(D | \theta)$
> - **MAP:** $\hat{\theta}_{MAP} = \arg\max_{\theta} p(D | \theta) \cdot p(\theta)$
>
> Razlika je u **prioru** $p(\theta)$!

---

### Konjugatne distribucije

Ako odaberemo "pravu" apriornu distribuciju, aposteriorna će biti **iste vrste**!

| Izglednost      | Konjugatni prior | Aposteriorna |
| --------------- | ---------------- | ------------ |
| **Bernoulli**   | Beta             | Beta         |
| **Kategorička** | Dirichlet        | Dirichlet    |
| **Gaussova**    | Gaussova         | Gaussova     |

---

### Beta-Bernoullijev model

> **🔬 LABOS zadatak 2:** Ovaj model se koristi u zadatku!

#### Beta distribucija (prior za $\mu$)

$$p(\mu | \alpha, \beta) = \frac{1}{B(\alpha, \beta)} \mu^{\alpha-1} (1-\mu)^{\beta-1}$$

**Parametri $\alpha$ i $\beta$ su HIPERPARAMETRI** (moramo ih odabrati unaprijed!)

| $\alpha, \beta$      | Značenje                                                                    |
| -------------------- | --------------------------------------------------------------------------- |
| $\alpha = \beta = 1$ | Uniformni prior (neinformativan) - sve vrijednosti $\mu$ jednako vjerojatne |
| $\alpha = \beta = 2$ | Blago preferiram $\mu = 0.5$ (pošten novčić)                                |
| $\alpha = \beta > 2$ | Jače preferiram $\mu = 0.5$                                                 |
| $\alpha > \beta$     | Preferiram $\mu > 0.5$                                                      |
| $\alpha < \beta$     | Preferiram $\mu < 0.5$                                                      |

**Mod (maksimum) beta distribucije:**
$$\text{mod} = \frac{\alpha - 1}{\alpha + \beta - 2} \quad (\text{za } \alpha, \beta > 1)$$

#### MAP procjenitelj za Bernoullijeve varijable

Aposteriorna distribucija je **opet Beta** s parametrima:

- $\alpha' = m + \alpha$
- $\beta' = N - m + \beta$

**MAP procjenitelj:**
$$\boxed{\hat{\mu}_{MAP} = \frac{m + \alpha - 1}{N + \alpha + \beta - 2}}$$

#### Laplaceov procjenitelj (specijalni slučaj)

Za $\alpha = \beta = 2$:
$$\hat{\mu}_{Laplace} = \frac{m + 1}{N + 2}$$

> ⚠️ **KLJUČNO:** Laplaceov procjenitelj **nikad** ne daje 0 ili 1, čak i kad je $m = 0$ ili $m = N$! To rješava problem prenauučenosti.

---

### Usporedba MLE i MAP

| Aspekt              | MLE           | MAP                                             |
| ------------------- | ------------- | ----------------------------------------------- |
| Koristi prior?      | ❌ Ne         | ✅ Da                                           |
| Prenauučenost?      | Sklon         | Manje sklon                                     |
| Malo podataka?      | Loš           | Bolji                                           |
| Puno podataka?      | Dobar         | Jednako dobar                                   |
| Formula (Bernoulli) | $\frac{m}{N}$ | $\frac{m + \alpha - 1}{N + \alpha + \beta - 2}$ |

> **VAŽNO:** Kad $N \to \infty$, MAP konvergira prema MLE (podaci dominiraju nad priorom)!
>
> Kad je prior uniforman ($\alpha = \beta = 1$), MAP = MLE!

---

### Dirichlet-kategorički model

Za kategoričku varijablu s K vrijednosti:

**Dirichlet distribucija** (prior):
$$p(\boldsymbol{\mu} | \boldsymbol{\alpha}) = \frac{1}{B(\boldsymbol{\alpha})} \prod_{k=1}^{K} \mu_k^{\alpha_k - 1}$$

**MAP procjenitelj:**
$$\hat{\mu}_{k,MAP} = \frac{N_k + \alpha_k - 1}{\sum_k (N_k + \alpha_k) - K}$$

Za $\alpha_k = 2$ (svi jednaki):
$$\hat{\mu}_{k,MAP} = \frac{N_k + 1}{N + K}$$

---

### Zaglađivanje (Smoothing)

MAP procjenitelj efektivno radi **zaglađivanje** - preraspodjelu mase vjerojatnosti s vrlo vjerojatnih na manje vjerojatne događaje.

**Bez zaglađivanja:** Ako se neka vrijednost nikad nije pojavila, $\hat{\mu} = 0$
**Sa zaglađivanjem:** Čak i ako se nikad nije pojavila, $\hat{\mu} > 0$

**ML procjena:** $\hat{\mu}_{ML} = m/N$
**MAP procjena:** $\hat{\mu}_{MAP} = (m + \alpha - 1) / (N + \alpha + \beta - 2)$

---

### 📝 Moguća ispitna pitanja s odgovorima

**1. Što je funkcija izglednosti i po čemu se razlikuje od vjerojatnosti?**

> **Funkcija izglednosti** $\mathcal{L}(\theta|D)$ je vjerojatnost podataka $D$ za dane parametre $\theta$, ali promatrana kao **funkcija od $\theta$** (dok je $D$ fiksiran).
>
> **Ključna razlika:** Izglednost NIJE vjerojatnost parametara! $\int \mathcal{L}(\theta|D) d\theta \neq 1$ općenito.
>
> Vjerojatnost govori "za fiksne parametre, kolika je šansa za ovaj ishod?", dok izglednost govori "za fiksne podatke, koji parametri su najizgledniji?"

---

**2. Zašto je MLE sklon prenauučenosti i kako MAP rješava taj problem?**

> **MLE problem:** MLE se previše oslanja na podatke. Ako imamo malo podataka, može dati ekstremne procjene.
>
> **Primjer:** 5 bacanja novčića, 0 glava → MLE kaže $\mu = 0$ (nemoguće dobiti glavu!)
>
> **MAP rješenje:** MAP kombinira podatke s apriornim znanjem. Prior "vuče" procjenu prema razumnim vrijednostima.
>
> S priorom $\alpha = \beta = 2$: $\hat{\mu}_{MAP} = \frac{0 + 1}{5 + 2} = 0.14$ - puno razumnije!

---

**3. Što su konjugatne distribucije i zašto su korisne?**

> **Konjugatne distribucije:** Ako je prior konjugatan za danu izglednost, tada je aposteriorna distribucija **iste vrste** kao prior.
>
> **Primjer:** Beta prior + Bernoulli likelihood = Beta posterior
>
> **Korisnost:**
>
> 1. **Analitičko rješenje:** Možemo izračunati MAP u zatvorenoj formi
> 2. **Online učenje:** Posterior možemo koristiti kao novi prior kad dođu novi podaci

---

**4. Kako se parametri $\alpha$ i $\beta$ beta distribucije odnose na apriorno znanje?**

> - $\alpha$ i $\beta$ su **hiperparametri** (moramo ih odabrati unaprijed)
> - Veći $\alpha$ → vjerujemo da je $\mu$ bliže 1
> - Veći $\beta$ → vjerujemo da je $\mu$ bliže 0
> - $\alpha = \beta$ → simetrično oko 0.5
> - $\alpha = \beta = 1$ → uniformni prior (nemamo apriorno znanje)
> - $\alpha = \beta = 2$ → blago preferiramo $\mu = 0.5$ (Laplaceov prior)

---

**5. Kada MAP konvergira prema MLE?**

> MAP konvergira prema MLE u dva slučaja:
>
> 1. **Uniformni prior** ($\alpha = \beta = 1$): Tada $p(\theta)$ = const, pa MAP = MLE
> 2. **Puno podataka** ($N \to \infty$): Podaci dominiraju nad priorom. U formuli $\frac{m + \alpha - 1}{N + \alpha + \beta - 2}$, za veliki N, $\alpha$ i $\beta$ postaju zanemarivi → dobivamo $\frac{m}{N}$ = MLE

---

**6. Što je Laplaceovo zaglađivanje?**

> **Laplaceovo zaglađivanje** je MAP procjena s priorom $\alpha = \beta = 2$:
> $$\hat{\mu}_{Laplace} = \frac{m + 1}{N + 2}$$
>
> **Efekt:** Nikad ne dobijemo $\mu = 0$ ili $\mu = 1$, čak i za ekstremne podatke.
>
> **Za kategoričke varijable:** $\hat{\mu}_k = \frac{N_k + 1}{N + K}$
>
> Intuitivno: kao da smo prije promatranja već vidjeli 1 uspjeh i 1 neuspjeh (ili 1 primjer svake kategorije).

---

### 🎯 Stvarna ispitna pitanja (Cjelina 14)

#### Pitanje 1: Po čemu se izglednost razlikuje od vjerojatnosti?

| Odgovor  | Tvrdnja                                                                                                                                                                  |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| A        | $\mathcal{L}(\theta\|D)$ jednaka je gustoći vjerojatnosti $p(\theta\|D)$, ali nije ograničena sa 1                                                                       |
| B        | Ako su podaci diskretni, onda je funkcija izglednosti parametara $\theta$ isto što i zajednička vjerojatnost uzorka $D$ i parametara $\theta$                            |
| **✅ C** | $\mathcal{L}(\theta\|D)$ jednaka je gustoći vjerojatnosti $p(D\|\theta)$, samo što je izglednost funkcija parametara $\theta$, dok je $p(D\|\theta)$ funkcija uzorka $D$ |
| D        | Za razliku od vjerojatnosti, funkcija izglednosti je simetrična, u smislu da vrijedi $\mathcal{L}(\theta\|D) = p(D\|\theta)$                                             |

> **Objašnjenje:** Izglednost i vjerojatnost $p(D|\theta)$ su **ista formula**, ali gledamo ih iz različite perspektive:
>
> - $p(D|\theta)$ - funkcija od $D$ (parametri fiksirani)
> - $\mathcal{L}(\theta|D)$ - funkcija od $\theta$ (podaci fiksirani)

---

#### Pitanje 2: Što je zapravo funkcija log-izglednosti?

| Odgovor  | Tvrdnja                                                                                                                                                      |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| A        | Funkcija koja primjeru x pridjeljuje vjerojatnost $p(y\|x)$...                                                                                               |
| B        | Funkcija koja uzorku $D$ pridjeljuje vjerojatnost parametara $\theta$...                                                                                     |
| **✅ C** | Funkcija koja parametrima $\theta$ pridjeljuje vjerojatnost uzorka $D$, uz pretpostavku da se uzorak pokorava distribuciji definiranoj modelom $h(x;\theta)$ |
| D        | Funkcija koja primjeru $(x,y)$ pridjeljuje vjerojatnost pripadanja skupu...                                                                                  |

> **Objašnjenje:** Log-izglednost $\ln\mathcal{L}(\theta|D)$ je logaritam vjerojatnosti podataka za dane parametre. Parametrima $\theta$ pridjeljuje broj koji govori koliko su ti parametri "izgledni" s obzirom na podatke.

---

#### Pitanje 3: Za koji parametar distribucije je MLE procjena PRISTRANA?

| Odgovor  | Tvrdnja                                       |
| -------- | --------------------------------------------- |
| A        | Srednja vrijednost Gaussove distribucije      |
| B        | Varijanca Bernoullijeve distribucije          |
| C        | Srednja vrijednost Bernoullijeve distribucije |
| **✅ D** | Kovarijacijska matrica Gaussove distribucije  |

> **Objašnjenje:** MLE za srednju vrijednost (i Gaussove i Bernoullijeve) je **nepristran**. Ali MLE za varijancu/kovarijacijsku matricu je **pristran** jer dijeli s $N$ umjesto $N-1$:
> $$\hat{\Sigma}_{MLE} = \frac{1}{N}\sum(x^{(i)} - \hat{\mu})(x^{(i)} - \hat{\mu})^T \quad \text{(PRISTRANO!)}$$
>
> ⚠️ **Napomena:** Tehnički, i B je pristrano (varijanca Bernoullija je $\mu(1-\mu)$, a MLE za to je $\hat{\mu}(1-\hat{\mu})$ što je pristrano), ali D je "klasičniji" primjer koji se uvijek spominje.

---

#### Pitanje 4: Što znači da je prior konjugatan izglednosti i zašto to želimo?

| Odgovor  | Tvrdnja                                                                                                                                                                                                                       |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A        | Apriorna distribucija ista vrsta kao vjerojatnost podataka...                                                                                                                                                                 |
| B        | Apriorna distribucija upravljana hiperparametrima... parametri priora i izglednosti identični...                                                                                                                              |
| C        | Aposteriorna distribucija ista kao izglednost parametara...                                                                                                                                                                   |
| **✅ D** | Umnožak izglednosti i apriorne distribucije daje distribuciju koja je **iste vrste kao i apriorna**, a ako je iz eksponencijalne familije, **mod postoji u zatvorenoj formi**, što omogućava analitički izračun procjenitelja |

> **Objašnjenje:** Konjugatnost znači: Prior × Likelihood = Posterior **iste vrste kao Prior**
>
> Npr: Beta × Bernoulli = Beta
>
> **Zašto je to dobro?**
>
> 1. Možemo analitički naći maksimum (MAP)
> 2. Omogućava online učenje (posterior postaje novi prior)

---

#### Pitanje 5: Što ako prior NIJE konjugatan izglednosti?

| Odgovor  | Tvrdnja                                                                                                                                 |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **✅ A** | Aposteriornu distribuciju $p(\theta\|D)$ ne možemo izvesti u zatvorenoj formi, ali MAP možemo izračunati **heurističkom optimizacijom** |
| B        | Zajedničku distribuciju ne možemo izvesti, pa MAP nije definiran                                                                        |
| C        | Ako je prior iz eksponencijalne familije, posterior je u zatvorenoj formi...                                                            |
| D        | Neovisno o prioru, MAP je izračunljiv optimizacijom drugog reda                                                                         |

> **Objašnjenje:** Bez konjugatnosti:
>
> - Posterior nema lijepu zatvorenu formu
> - ALI MAP je i dalje definiran kao $\arg\max_\theta p(D|\theta)p(\theta)$
> - Možemo ga naći **numerički** (gradijentni uspon, Newton...)

---

#### Pitanje 6: Kada MLE i MAP daju JEDNAKE procjene?

| Odgovor  | Tvrdnja                                                       |
| -------- | ------------------------------------------------------------- |
| A        | Kada $p(\theta)$ definiramo kao unimodalnu distribuciju       |
| **✅ B** | Kada broj primjera $N$ teži prema beskonačno                  |
| C        | Kada je $p(\theta)$ konjugatna izglednosti                    |
| D        | Kada se u $D$ realizirala svaka vrijednost slučajne varijable |

> **Objašnjenje:** Dva slučaja kad MAP = MLE:
>
> 1. **Uniformni prior** ($\alpha = \beta = 1$) - jer $p(\theta) = const$
> 2. **$N \to \infty$** - podaci dominiraju, prior postaje nebitan
>
> U formuli $\frac{m + \alpha - 1}{N + \alpha + \beta - 2}$, za veliki $N$, $\alpha$ i $\beta$ postaju zanemarivi → dobivamo $\frac{m}{N}$ = MLE

---

#### Pitanje 7: Bayesov klasifikator, mali skup za učenje, MLE vs MAP (Laplace)

**Kontekst:** Procjenjujemo $\mu$ Bernoullijeve distribucije. Skup za učenje je malen. Procjenitelj $\hat{\mu}$ može biti pristran ili nepristran, ali ako je prenaučen, neće dobro generalizirati.

| MLE                 | MAP (Laplace)             |
| ------------------- | ------------------------- |
| Nepristran          | Pristran                  |
| Može biti prenaučen | Manje sklon prenaučenosti |
| Loš za male skupove | Bolji za male skupove     |

> **Ključni uvid:** MAP procjenitelj je **pristran** (pomaknut prema prioru), ali zato **bolje generalizira** jer nije prenaučen!
>
> ⚠️ **Nepristranost ≠ Dobra generalizacija!**

---

#### Pitanje 8: Što i kako maksimizira MAP procjenitelj?

| Odgovor  | Tvrdnja                                                                                                                                                                |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **✅ A** | **Zajedničku gustoću** vjerojatnosti parametara i podataka $p(D,\theta) = p(D\|\theta)p(\theta)$, u **zatvorenoj formi ako je prior konjugatan**, inače **iterativno** |
| B        | Aposteriornu vjerojatnost podataka...                                                                                                                                  |
| C        | Zajedničku vjerojatnost, iterativno ako je prior iz eksp. familije...                                                                                                  |
| D        | Aposteriornu gustoću vjerojatnosti podataka...                                                                                                                         |

> **Objašnjenje:** MAP maksimizira:
> $$\hat{\theta}_{MAP} = \arg\max_\theta p(\theta|D) = \arg\max_\theta \underbrace{p(D|\theta) \cdot p(\theta)}_{= p(D, \theta)}$$
>
> To je **zajednička vjerojatnost** (jer je $p(D)$ konstanta).
>
> - **Konjugatan prior** → zatvorena forma
> - **Nekonjugatan prior** → iterativna optimizacija

---

### ⚠️ Najčešće zamke na ispitu (Cjelina 14)

1. **Izglednost NIJE vjerojatnost parametara** - nego vjerojatnost podataka kao funkcija parametara

2. **MLE za varijancu je PRISTRAN** - podcjenjuje pravu varijancu

3. **Nepristranost ≠ Dobra generalizacija** - MAP je pristran ali generalizira bolje!

4. **MAP = MLE** u dva slučaja: uniformni prior ILI $N \to \infty$

5. **Konjugatnost** - osigurava da je posterior iste vrste kao prior (Beta-Bernoulli, Dirichlet-Kategorička, Gauss-Gauss)

---

### 🧮 Praktične formule za numeričke zadatke

#### Gaussova log-izglednost

Za uzorak $D = \{x^{(1)}, ..., x^{(N)}\}$:

$$\ln \mathcal{L}(\mu, \sigma^2 | D) = -\frac{N}{2}\ln(2\pi) - N\ln\sigma - \frac{\sum_i (x^{(i)} - \mu)^2}{2\sigma^2}$$

**MLE procjene:**
$$\hat{\mu}_{MLE} = \frac{1}{N}\sum_i x^{(i)} \quad \quad \hat{\sigma}^2_{MLE} = \frac{1}{N}\sum_i (x^{(i)} - \hat{\mu})^2$$

**Nepristrana procjena varijance:**
$$\hat{\sigma}^2_{UB} = \frac{N}{N-1} \hat{\sigma}^2_{MLE} = \frac{1}{N-1}\sum_i (x^{(i)} - \hat{\mu})^2$$

> ⚠️ **VAŽNO:** $\mathcal{L}(\hat{\mu}_{MLE}, \hat{\sigma}^2_{MLE}) > \mathcal{L}(\hat{\mu}_{MLE}, \hat{\sigma}^2_{UB})$ uvijek! MLE po definiciji maksimizira izglednost!

---

#### Sekvencijalno Bayesovo učenje (Online learning)

Posterior iz prvog uzorka postaje prior za drugi uzorak!

**Za Beta-Bernoulli:**

1. Prior: $\alpha_0, \beta_0$
2. Nakon prvog uzorka $(N_1, m_1)$: $\alpha_1 = m_1 + \alpha_0$, $\beta_1 = N_1 - m_1 + \beta_0$
3. Nakon drugog uzorka $(N_2, m_2)$: $\alpha_2 = m_2 + \alpha_1$, $\beta_2 = N_2 - m_2 + \beta_1$

**MAP nakon prvog uzorka:**
$$\hat{\mu}_1 = \frac{m_1 + \alpha_0 - 1}{N_1 + \alpha_0 + \beta_0 - 2}$$

**MAP nakon oba uzorka:**
$$\hat{\mu}_2 = \frac{(m_1 + m_2) + \alpha_0 - 1}{(N_1 + N_2) + \alpha_0 + \beta_0 - 2}$$

---

#### Dirichlet-kategorički model

**MAP za K-vrijednosnu kategoričku varijablu:**
$$\hat{\mu}_{k,MAP} = \frac{N_k + \alpha_k - 1}{\sum_j (N_j + \alpha_j) - K}$$

Za simetričan prior $\alpha_k = \alpha$ za sve k:
$$\hat{\mu}_{k,MAP} = \frac{N_k + \alpha - 1}{N + K\alpha - K}$$

> **Tipičan zadatak:** Odrediti $\alpha$ tako da određena vrijednost $x_k$ bude najvjerojatnija!
>
> Rješenje: $\hat{\mu}_k > \hat{\mu}_j$ za sve $j \neq k$ → riješi nejednadžbu za $\alpha$

---

#### Kada su MAP i MLE jednaki (osim uniformnog priora)?

Za Beta-Bernoulli, MAP = MLE = $\frac{m}{N}$ kada:

$$\frac{m + \alpha - 1}{N + \alpha + \beta - 2} = \frac{m}{N}$$

Rješavanjem:
$$m(N + \alpha + \beta - 2) = N(m + \alpha - 1)$$
$$mN + m\alpha + m\beta - 2m = Nm + N\alpha - N$$
$$m\alpha + m\beta - 2m = N\alpha - N$$
$$m(\alpha + \beta - 2) = N(\alpha - 1)$$

Ako je MLE = 0.2 (npr. m=2, N=10), traži $\alpha, \beta$ koji zadovoljavaju gornju jednadžbu.

---

#### Tablica vrijednosti za brzo računanje

| Podatak               | Formula                                                                  |
| --------------------- | ------------------------------------------------------------------------ |
| Srednja vrijednost    | $\bar{x} = \frac{1}{N}\sum x_i$                                          |
| MLE varijanca         | $\hat{\sigma}^2 = \frac{1}{N}\sum(x_i - \bar{x})^2$                      |
| Nepristrana varijanca | $s^2 = \frac{N}{N-1}\hat{\sigma}^2$                                      |
| Log Gaussove PDF      | $\ln p(x) = -\frac{1}{2}\ln(2\pi\sigma^2) - \frac{(x-\mu)^2}{2\sigma^2}$ |
| Beta mod              | $\frac{\alpha - 1}{\alpha + \beta - 2}$                                  |
| Bernoulli MLE         | $\frac{m}{N}$                                                            |
| Bernoulli MAP         | $\frac{m + \alpha - 1}{N + \alpha + \beta - 2}$                          |
| Laplace               | $\frac{m + 1}{N + 2}$                                                    |

---

### 📊 Tipovi numeričkih zadataka (Cjelina 14)

1. **Izračun log-izglednosti** za Gaussovu distribuciju na podskupu podataka
2. **Usporedba log-izglednosti** s različitim procjenama parametara (MLE vs nepristrana)
3. **Sekvencijalno učenje** - posterior → novi prior → novi posterior
4. **Dirichlet-kategorički** - izbor hiperparametara $\alpha$ za željeni ishod
5. **Pronalaženje $\alpha, \beta$** za koje MAP = MLE

---

## Cjelina 15: Bayesov klasifikator

> ℹ️ **Ova cjelina NIJE u labosu** - samo teorija za ispit!

---

### Osnovna pravila vjerojatnosti

#### Pravilo zbroja (marginalizacija)

$$P(x) = \sum_y P(x, y)$$

Iz zajedničke vjerojatnosti dobivamo **marginalnu vjerojatnost**.

#### Pravilo umnoška

$$P(x, y) = P(y|x)P(x) = P(x|y)P(y)$$

#### Bayesovo pravilo (ključno!)

$$P(y|x) = \frac{P(x|y)P(y)}{P(x)}$$

> **Snaga Bayesovog pravila:** Omogućava **obrnuti smjer zaključivanja** - iz $P(x|y)$ možemo dobiti $P(y|x)$!

---

### Bayesov klasifikator

$$P(y|x) = \frac{p(x|y)P(y)}{p(x)} = \frac{p(x|y)P(y)}{\sum_{y'} p(x|y')P(y')}$$

| Naziv                         | Simbol    | Značenje                                 |
| ----------------------------- | --------- | ---------------------------------------- |
| **Aposteriorna vjerojatnost** | $P(y\|x)$ | Vjerojatnost klase za dani primjer       |
| **Izglednost klase**          | $p(x\|y)$ | Distribucija primjera unutar klase       |
| **Apriorna vjerojatnost**     | $P(y)$    | Vjerojatnost klase neovisno o primjerima |
| **Marginalna vjerojatnost**   | $p(x)$    | Vjerojatnost primjera neovisno o klasi   |

#### MAP hipoteza (predikcija)

$$h(x) = \arg\max_y p(x|y)P(y)$$

> **Zašto faktoriziramo $p(x,y)$?** Jer je zajednička distribucija složena, a faktorizacijom dobivamo jednostavnije distribucije koje možemo modelirati standardnim teorijskim distribucijama!

---

### Generativni vs. Diskriminativni modeli

| Aspekt       | Generativni                    | Diskriminativni                 |
| ------------ | ------------------------------ | ------------------------------- |
| **Modelira** | Zajedničku $p(x, y)$           | Aposteriornu $P(y\|x)$ direktno |
| **Primjeri** | Bayesov klasifikator, GMM, HMM | Logistička regresija, SVM, k-NN |
| **Granica**  | Implicitno (iz $p(x,y)$)       | Eksplicitno                     |

#### Prednosti generativnih modela

1. ✅ **Ugradnja pozadinskog znanja** - kroz apriorne distribucije
2. ✅ **Interpretabilnost** - intuitivna interpretacija temeljena na vjerojatnosti
3. ✅ **Razne analize** - možemo računati razne vjerojatnosti (uvjetne, marginalne)
4. ✅ **Generiranje podataka** - možemo uzorkovati sintetičke primjere
5. ✅ **Detekcija outliera** - preko $p(x)$

#### Nedostaci generativnih modela

1. ❌ **Potreba za velikim brojem primjera** - za pouzdanu procjenu
2. ❌ **Nepotrebna složenost** - ako nas zanima samo klasifikacija, zašto modelirati cijelu $p(x,y)$?
3. ❌ **Više parametara** - složeniji modeli

> **U praksi:** Diskriminativni modeli često rade bolje ako nas zanima samo točnost klasifikacije!

---

### Gaussov Bayesov klasifikator

Za **kontinuirane značajke** - izglednost klase modeliramo Gaussovom distribucijom.

#### Univarijatni slučaj (jedna značajka)

$$p(x|y=j) = \frac{1}{\sqrt{2\pi}\sigma_j} \exp\left(-\frac{(x-\mu_j)^2}{2\sigma_j^2}\right)$$

**Model (log-skala):**
$$h_j(x) = -\ln\sigma_j - \frac{(x-\mu_j)^2}{2\sigma_j^2} + \ln P(y=j)$$

#### Multivarijatni slučaj (više značajki)

$$p(x|y=j) = \frac{1}{(2\pi)^{n/2}|\Sigma_j|^{1/2}} \exp\left(-\frac{1}{2}(x-\mu_j)^T\Sigma_j^{-1}(x-\mu_j)\right)$$

**Model (log-skala):**
$$h_j(x) = -\frac{1}{2}\ln|\Sigma_j| - \frac{1}{2}(x-\mu_j)^T\Sigma_j^{-1}(x-\mu_j) + \ln P(y=j)$$

---

### Varijante Gaussovog Bayesovog klasifikatora

#### Ključno pitanje: Kakva je granica između klasa?

| Kovarijacijska matrica              | Granica                  | Oblik izokontura |
| ----------------------------------- | ------------------------ | ---------------- |
| Različita za svaku klasu $\Sigma_j$ | **Kvadratna** (parabola) | Različite elipse |
| Dijeljena $\Sigma$                  | **Linearna**             | Iste elipse      |

> ⚠️ **VAŽNO ZA ISPIT:** Ako je kovarijacijska matrica **dijeljena** između klasa → granica je **LINEARNA**!

#### Tablica varijanti

| Pretpostavka           | Matrica                     | Parametri | Granica      |
| ---------------------- | --------------------------- | --------- | ------------ |
| Različite, pune        | $\Sigma_j$                  | $O(n^2)$  | Kvadratna    |
| **Dijeljena, puna**    | $\Sigma$                    | $O(n^2)$  | **Linearna** |
| Dijeljena, dijagonalna | $\Sigma = diag(\sigma_i^2)$ | $O(n)$    | Linearna     |
| Dijeljena, izotropna   | $\Sigma = \sigma^2 I$       | $O(n)$    | Linearna     |

#### Dijeljena kovarijacijska matrica

$$\hat{\Sigma} = \sum_j \hat{\mu}_j \hat{\Sigma}_j$$

(težinski prosjek po apriornim vjerojatnostima klasa)

#### Dijagonalna matrica → Uvjetna nezavisnost značajki!

Ako je $\Sigma = diag(\sigma_i^2)$, tada:
$$p(x|y) = \prod_{i=1}^{n} p(x_i|y)$$

Ovo vodi do **Naivnog Bayesovog klasifikatora** (Cjelina 16)!

#### Izotropna matrica

$$\Sigma = \sigma^2 I$$

Pretpostavlja da su sve značajke istog raspona (ima smisla ako smo skalirali značajke).

---

### MLE procjene parametara

$$\hat{\mu}_j = \frac{1}{N_j} \sum_{i:y^{(i)}=j} x^{(i)}$$

$$\hat{\Sigma}_j = \frac{1}{N_j} \sum_{i:y^{(i)}=j} (x^{(i)} - \hat{\mu}_j)(x^{(i)} - \hat{\mu}_j)^T$$

$$P(y=j) = \frac{N_j}{N}$$

---

### Generativna priča

Bayesov klasifikator opisuje **stohasatički proces generiranja podataka**:

1. **Korak 1:** Odaberi oznaku $y$ prema distribuciji $P(y)$
2. **Korak 2:** Za odabrani $y$, generiraj primjer $x$ prema distribuciji $p(x|y)$

> Ovo omogućava **generiranje sintetičkih podataka** nakon što je model naučen!

---

### 📝 Moguća ispitna pitanja (Cjelina 15)

**1. Što modeliraju generativni, a što diskriminativni modeli?**

> **Generativni:** Zajedničku distribuciju $p(x, y) = p(x|y)P(y)$
>
> **Diskriminativni:** Aposteriornu vjerojatnost $P(y|x)$ direktno

---

**2. Navedi prednosti i nedostatke generativnih modela.**

> **Prednosti:** Ugradnja pozadinskog znanja, interpretabilnost, razne analize, detekcija outliera
>
> **Nedostaci:** Potreba za više primjera, nepotrebna složenost za klasifikaciju, više parametara

---

**3. Kada je granica Gaussovog Bayesovog klasifikatora linearna?**

> Kada je kovarijacijska matrica **dijeljena** između svih klasa ($\Sigma_j = \Sigma$ za sve $j$).
>
> Ako svaka klasa ima svoju kovarijacijsku matricu, granica je **kvadratna** (parabola).

---

**4. Što znači pretpostavka dijagonalne kovarijacijske matrice?**

> Znači da su značajke **uvjetno nezavisne** uz zadanu klasu:
> $$p(x|y) = \prod_i p(x_i|y)$$
>
> To je temelj **Naivnog Bayesovog klasifikatora**.

---

**5. Kako se računa dijeljena kovarijacijska matrica?**

> Kao **težinski prosjek** kovarijacijskih matrica pojedinačnih klasa:
> $$\hat{\Sigma} = \sum_j P(y=j) \hat{\Sigma}_j$$
>
> Klase s većom apriornom vjerojatnosti više doprinose.

---

**6. Što je generativna priča?**

> Opis **stohastičkog procesa** koji generira podatke:
>
> 1. Uzorkuj klasu $y$ iz $P(y)$
> 2. Uzorkuj primjer $x$ iz $p(x|y)$
>
> Omogućava generiranje sintetičkih podataka.

---

### 🎯 Stvarna ispitna pitanja (Cjelina 15)

#### Pitanje 1: Zašto su diskriminativni modeli često točniji od generativnih?

| Odgovor  | Tvrdnja                                                                                                                                    |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| A        | Kod generativnih modela MLE je pristran, dok diskriminativni uče gradijentnim spustom koji je nepristran                                   |
| **✅ B** | Diskriminativni modeli s **manje parametara** mogu modelirati istu granicu između klasa, pa trebaju manje primjera i teže ih je prenaučiti |
| C        | Generativni modeli mogu modelirati nelinearne zavisnosti, što dovodi do prenaučenosti                                                      |
| D        | Diskriminativni modeli modeliraju zajedničku distribuciju pa ostvaruju veću točnost                                                        |

> **Objašnjenje:** Diskriminativni modeli modeliraju samo granicu $P(y|x)$, ne cijelu $p(x,y)$. Za istu klasifikacijsku sposobnost trebaju **manje parametara** → manje podataka za učenje → manja šansa za prenaučenost!

---

#### Pitanje 2: Što znači "nepotrebna složenost modeliranja" kod generativnih modela?

| Odgovor  | Tvrdnja                                |
| -------- | -------------------------------------- | -------------------------------------------------------------------------- |
| A        | $p(x,y)$ se faktorizira kao $p(y       | x)p(x)$, no ima više parametara                                            |
| B        | Generativni modeli modeliraju $p(y     | x)$ što iziskuje više parametara                                           |
| C        | Generativni modeli definiraju $p(y     | x)$ zasebno za svaku klasu                                                 |
| **✅ D** | Za klasifikaciju je potrebna samo $p(y | x)$, koja se može modelirati s **manje parametara** od zajedničke $p(x,y)$ |

> **Objašnjenje:** Ako nas zanima **samo klasifikacija**, modeliranje cijele zajedničke distribucije $p(x,y)$ je "overkill". Dovoljno je modelirati $P(y|x)$ direktno, što zahtijeva manje parametara.

---

#### Pitanje 3: K=2 klase, diskretne značajke (neke binarne, neke višeznačne). Koje distribucije koristimo?

| Odgovor  | Za $P(y)$         | Za $P(x           | y)$ |
| -------- | ----------------- | ----------------- | --- |
| **✅ A** | **Bernoullijeva** | **Multinulijeva** |
| B        | Kategorička       | Gaussova          |
| C        | Bernoullijeva     | Gaussova          |
| D        | Gaussova          | Multinulijeva     |

> **Objašnjenje:**
>
> - $K=2$ klase → **Bernoullijeva** za $P(y)$
> - Diskretne značajke (viševrijednosne) → **Multinulijeva (kategorička)** za $P(x|y)$

---

#### Pitanje 4: K>2 klase, značajke su realni brojevi $x \in \mathbb{R}^n$. Koje distribucije koristimo?

| Odgovor  | Za $P(y)$       | Za $P(x       | y)$ |
| -------- | --------------- | ------------- | --- |
| A        | Bernoullijeva   | Gaussova      |
| **✅ B** | **Kategorička** | **Gaussova**  |
| C        | Gaussova        | Multinulijeva |
| D        | Kategorička     | Kategorička   |

> **Objašnjenje:**
>
> - $K>2$ klase → **Kategorička (multinulijeva)** za $P(y)$
> - Kontinuirane značajke → **Gaussova** za $P(x|y)$

---

#### Pitanje 5: Po čemu se vidi da je Bayesov klasifikator GENERATIVAN model?

$$h(x;\theta) = \arg\max_y p(x|y)P(y)$$

| Odgovor  | Tvrdnja                                                        |
| -------- | -------------------------------------------------------------- | ---------------------------------- |
| A        | Faktorizira zajedničku vjerojatnost i zanemaruje $p(x)$        |
| B        | Parametre računa MAP-procjeniteljem                            |
| **✅ C** | Modelira **vjerojatnost primjera i oznaka**, budući da je $p(x | y)P(y) = p(x,y)$ (pravilo umnoška) |
| D        | Klasificira prema MAP-hipotezi                                 |

> **Objašnjenje:** Model je generativan jer modelira **zajedničku vjerojatnost** $p(x,y) = p(x|y)P(y)$, a ne direktno aposteriornu $P(y|x)$.

---

#### Pitanje 6: Uz koje MINIMALNE pretpostavke je broj parametara za $\Sigma$ linearan u $n$?

| Odgovor  | Tvrdnja                                         |
| -------- | ----------------------------------------------- |
| A        | Šum je isti za sve klase                        |
| B        | Značajke nisu korelirane i šum ne ovisi o klasi |
| C        | Šum je isti za sve klase i sve značajke         |
| **✅ D** | **Nema linearne zavisnosti između značajki**    |

> **Objašnjenje:**
>
> - Puna matrica: $O(n^2)$ parametara
> - **Dijagonalna matrica** (nema korelacije): $O(n)$ parametara
>
> Minimalna pretpostavka za $O(n)$ je **dijagonalna $\Sigma$**, tj. nema linearne zavisnosti (korelacije) između značajki!

---

### ⚠️ Zamke na ispitu (Cjelina 15)

1. **Diskriminativni NE modeliraju $p(x,y)$** - oni modeliraju $P(y|x)$ direktno!

2. **Generativni = modelira $p(x,y)$**, diskriminativni = modelira $P(y|x)$

3. **Izbor distribucije:**
   - $K=2$ klase → Bernoulli za $P(y)$
   - $K>2$ klase → Kategorička za $P(y)$
   - Kontinuirane značajke → Gaussova
   - Diskretne značajke → Multinulijeva/Kategorička

4. **Za $O(n)$ parametara $\Sigma$** → mora biti dijagonalna (bez korelacije)

---

### 🧮 Praktične formule za numeričke zadatke (Cjelina 15)

#### Izračun h_j(x) - log zajedničke vjerojatnosti

**Puna formula (multivarijatni Gauss):**
$$h_j(x) = \ln p(x, y=j) = \ln p(x|y=j) + \ln P(y=j)$$

$$h_j(x) = -\frac{n}{2}\ln(2\pi) - \frac{1}{2}\ln|\Sigma_j| - \frac{1}{2}(x-\mu_j)^T\Sigma_j^{-1}(x-\mu_j) + \ln P(y=j)$$

**Pojednostavljena (bez konstanti za usporedbu):**
$$h_j(x) \propto -\frac{1}{2}\ln|\Sigma_j| - \frac{1}{2}(x-\mu_j)^T\Sigma_j^{-1}(x-\mu_j) + \ln P(y=j)$$

---

#### Dijeljena kovarijacijska matrica

$$\hat{\Sigma} = \sum_j P(y=j) \cdot \hat{\Sigma}_j = \sum_j \frac{N_j}{N} \cdot \hat{\Sigma}_j$$

**Primjer:** Za K=2 klase s $\hat{\mu}_1 = 0.2$, $\hat{\mu}_2 = 0.8$:
$$\hat{\Sigma} = 0.2 \cdot \hat{\Sigma}_1 + 0.8 \cdot \hat{\Sigma}_2$$

---

#### Granica između klasa

Granica je gdje $h_1(x) = h_0(x)$, tj. $h_1(x) - h_0(x) = 0$

**Za dijeljenu $\Sigma$ (linearna granica):**
$$w^T x + w_0 = 0$$
gdje:

- $w = \Sigma^{-1}(\mu_1 - \mu_0)$
- $w_0 = -\frac{1}{2}\mu_1^T\Sigma^{-1}\mu_1 + \frac{1}{2}\mu_0^T\Sigma^{-1}\mu_0 + \ln\frac{P(y=1)}{P(y=0)}$

---

#### Broj parametara za različite varijante

| Model                            | Parametri za $\Sigma$      | Ukupno    |
| -------------------------------- | -------------------------- | --------- |
| Različite pune $\Sigma_j$        | $K \cdot \frac{n(n+1)}{2}$ | $O(Kn^2)$ |
| Dijeljena puna $\Sigma$          | $\frac{n(n+1)}{2}$         | $O(n^2)$  |
| Različite dijagonalne            | $K \cdot n$                | $O(Kn)$   |
| Dijeljena dijagonalna            | $n$                        | $O(n)$    |
| Dijeljena izotropna $\sigma^2 I$ | $1$                        | $O(1)$    |

> **Napomena:** Uvijek dodaj $K \cdot n$ za vektore $\mu_j$ i $K-1$ za apriorne vjerojatnosti!

---

#### Određivanje apriornih vjerojatnosti iz grafa

**Iz grafa izglednosti i posteriora:**

- Posterior $\propto$ Likelihood $\times$ Prior
- Ako klasa ima **malu izglednost** ali **veliki posterior** → ima **veliki prior**!
- Ako klasa ima **veliku izglednost** ali **mali posterior** → ima **mali prior**!

**Provjera:** Zbroj svih $P(y=j)$ mora biti 1!

---

#### Usporedba složenosti modela

**Relacije:**

- $\mathcal{H}_1 \supset \mathcal{H}_2$ znači: $\mathcal{H}_1$ je **složeniji** (ima više parametara)
- $\mathcal{H}_1 > \mathcal{H}_2$ znači: $\mathcal{H}_1$ ima **više parametara**

**Primjer hijerarhije:**
$$\text{Različite pune } \Sigma_j \supset \text{Dijeljena puna } \Sigma \supset \text{Dijeljena dijagonalna} \supset \text{Dijeljena izotropna}$$

---

#### Praktični savjeti za računanje

1. **Za dijagonalnu $\Sigma$:**
   - $|\Sigma| = \prod_i \sigma_i^2$ (produkt dijagonalnih elemenata)
   - $\Sigma^{-1} = diag(1/\sigma_i^2)$
   - $(x-\mu)^T\Sigma^{-1}(x-\mu) = \sum_i \frac{(x_i-\mu_i)^2}{\sigma_i^2}$

2. **Nepristrana procjena varijance:**
   $$\hat{\sigma}^2_{UB} = \frac{1}{N_j-1}\sum_{i:y^{(i)}=j}(x^{(i)} - \hat{\mu}_j)^2$$

3. **Za $x = \mu_j$:**
   $$(x-\mu_j)^T\Sigma^{-1}(x-\mu_j) = 0$$

---

### 📊 Tipovi numeričkih zadataka (Cjelina 15)

| Zadatak | Što se računa                    | Ključna formula                              |
| ------- | -------------------------------- | -------------------------------------------- |
| 1       | Apriorne vjerojatnosti iz grafa  | Posterior ∝ Likelihood × Prior               |
| 2       | Usporedba složenosti modela      | Broj parametara za $\Sigma$                  |
| 3       | $h_j(x)$ s dijeljenom $\Sigma$   | $\hat{\Sigma} = \sum_j P(y=j)\hat{\Sigma}_j$ |
| 4       | Promjena modela → nova granica   | Gdje se MAP hipoteze razlikuju               |
| 5       | Točke na granici između klasa    | $h_1(x) - h_0(x) = 0$                        |
| 6       | $h_j(x)$ s dijagonalnom $\Sigma$ | $\sum_i \frac{(x_i-\mu_i)^2}{\sigma_i^2}$    |

---

## Cjelina 16: Bayesov klasifikator II (Naivan Bayes)

> ℹ️ **Ova cjelina NIJE u labosu** - samo teorija za ispit!

---

### Veza: Gaussov Bayesov klasifikator ↔ Logistička regresija

**Ključno otkriće:** Gaussov Bayesov klasifikator s **dijeljenom kovarijacijskom matricom** daje **istu granicu** kao logistička regresija!

$$P(y=1|x) = \sigma(\alpha) = \frac{1}{1 + e^{-\alpha}}$$

gdje je:
$$\alpha = \ln\frac{p(x|y=1)P(y=1)}{p(x|y=0)P(y=0)} = w^T x + w_0$$

| Model                | Tip             | Parametri (za n značajki)   |
| -------------------- | --------------- | --------------------------- |
| Logistička regresija | Diskriminativan | $n + 1$                     |
| Gaussov Bayesov      | Generativan     | $\frac{n(n+1)}{2} + 2n + 1$ |

> ⚠️ **VAŽNO:** Ista granica, ali generativni model ima **VIŠE parametara**! Zato diskriminativni modeli često rade bolje.

**Kada izlaz logističke regresije odgovara pravoj vjerojatnosti?**

1. Primjeri iz obje klase su normalno distribuirani (Gaussova izglednost)
2. Kovarijacijska matrica je dijeljena

---

### Naivan Bayesov klasifikator

#### Problem s punom izglednosti

Ako $x = (x_1, ..., x_n)$ modeliramo kao jednu kategoričku varijablu:

- Broj parametara: $K \cdot (\prod_{k=1}^{n} K_k - 1)$ → **EKSPONENCIJALNO** u broju značajki!
- Model **ne može generalizirati** - neviđeni primjeri imaju vjerojatnost 0

#### Rješenje: Pretpostavka uvjetne nezavisnosti

$$P(x_1, ..., x_n | y) = \prod_{k=1}^{n} P(x_k | y)$$

**Značenje:** Značajke su **uvjetno nezavisne** uz zadanu klasu y.

#### Model naivnog Bayesovog klasifikatora

$$h(x) = \arg\max_y P(y) \prod_{k=1}^{n} P(x_k | y)$$

#### Broj parametara

$$\sum_{k=1}^{n} (K_k - 1) \cdot K + (K - 1)$$

> **Usporedba:**
>
> - Puna izglednost: $O(\prod K_k)$ → **eksponencijalno**
> - Naivni Bayes: $O(\sum K_k)$ → **linearno**!

---

### Pravilo lanca (Chain Rule)

$$P(x_1, ..., x_n) = \prod_{k=1}^{n} P(x_k | x_1, ..., x_{k-1})$$

**Za izglednost klase:**
$$P(x_1, ..., x_n | y) = \prod_{k=1}^{n} P(x_k | x_1, ..., x_{k-1}, y)$$

Naivni Bayes pojednostavljuje: $P(x_k | x_1, ..., x_{k-1}, y) = P(x_k | y)$

---

### Uvjetna nezavisnost

#### Marginalna nezavisnost

$$X \perp Y \iff P(X, Y) = P(X) \cdot P(Y)$$

Ekvivalentno: $P(X|Y) = P(X)$ (poznavanje Y ne utječe na X)

#### Uvjetna nezavisnost

$$X \perp Y | Z \iff P(X, Y | Z) = P(X|Z) \cdot P(Y|Z)$$

Ekvivalentno: $P(X | Y, Z) = P(X | Z)$ (ako znamo Z, Y ne daje dodatnu info o X)

> ⚠️ **PAZI:** Varijable mogu biti:
>
> - Marginalno zavisne, ali uvjetno nezavisne
> - Marginalno nezavisne, ali uvjetno zavisne!

---

### Učenje naivnog Bayesovog klasifikatora

#### MLE za apriorne vjerojatnosti

$$P(y = j) = \frac{N_j}{N}$$

#### MLE za izglednosti (PROBLEM!)

$$P(x_k | y = j) = \frac{N_{kj}}{N_j}$$

**Problem:** Ako se neka kombinacija $(x_k, y)$ nikad ne pojavi → $P(x_k|y) = 0$ → cijela aposteriorna = 0!

#### MAP (Laplaceovo zaglađivanje) - RJEŠENJE

$$P(x_k | y = j) = \frac{N_{kj} + 1}{N_j + K_k}$$

> ⚠️ **VAŽNO ZA ISPIT:** Kod naivnog Bayesa **uvijek koristimo zaglađivanje** za izglednosti!

---

### Polunaivan Bayesov klasifikator

**Ideja:** Relaksirati pretpostavku nezavisnosti za neke parove značajki.

Umjesto:
$$P(x_1, x_2, x_3 | y) = P(x_1|y) \cdot P(x_2|y) \cdot P(x_3|y)$$

Koristimo (ako $x_2$ i $x_3$ nisu nezavisne):
$$P(x_1, x_2, x_3 | y) = P(x_1|y) \cdot P(x_2, x_3|y)$$

**Trade-off:**

- ✅ Točniji model (bolje modelira zavisnosti)
- ❌ Više parametara

#### Kako odabrati koje značajke združiti?

1. **Unakrsna provjera** (algoritam FSSJ)
2. **Uzajamna informacija** (algoritmi TAN, k-DB)

---

### Uzajamna informacija (Mutual Information)

**Kullback-Leibler divergencija:**
$$D_{KL}(P || Q) = \sum_x P(x) \ln \frac{P(x)}{Q(x)}$$

**Uzajamna informacija:**
$$I(X, Y) = D_{KL}(P(X,Y) || P(X)P(Y)) = \sum_{x,y} P(x,y) \ln \frac{P(x,y)}{P(x)P(y)}$$

| Vrijednost    | Značenje           |
| ------------- | ------------------ |
| $I(X,Y) = 0$  | X i Y su nezavisne |
| $I(X,Y) > 0$  | X i Y su zavisne   |
| Veći $I(X,Y)$ | Jača zavisnost     |

> **Primjena:** Značajke s visokom uzajamnom informacijom treba združiti u zajednički faktor!

---

### 📝 Moguća ispitna pitanja (Cjelina 16)

**1. Koja je veza između Gaussovog Bayesovog klasifikatora i logističke regresije?**

> Gaussov Bayesov klasifikator s **dijeljenom kovarijacijskom matricom** daje **istu granicu** kao logistička regresija (neregularizirana).
>
> Razlika: Bayesov klasifikator ima **više parametara** jer modelira cijelu $p(x,y)$, dok logistička regresija modelira samo $P(y|x)$.

---

**2. Što je pretpostavka naivnog Bayesovog klasifikatora?**

> Pretpostavka **uvjetne nezavisnosti značajki** uz zadanu klasu:
> $$P(x_1, ..., x_n | y) = \prod_k P(x_k | y)$$
>
> To znači: ako znamo klasu y, značajke ne daju informaciju jedna o drugoj.

---

**3. Zašto naivni Bayes koristi zaglađivanje (MAP umjesto MLE)?**

> Ako MLE procjena za neku kombinaciju $(x_k, y)$ bude 0 (jer se nikad nije pojavila u podacima), onda će **cijela aposteriorna vjerojatnost biti 0** (jer se faktori množe!).
>
> Laplaceovo zaglađivanje: $P(x_k|y) = \frac{N_{kj} + 1}{N_j + K_k}$ osigurava da nijedna vjerojatnost nije 0.

---

**4. Što je uvjetna nezavisnost i kako se razlikuje od marginalne?**

> **Marginalna nezavisnost:** $X \perp Y$ znači $P(X,Y) = P(X)P(Y)$
>
> **Uvjetna nezavisnost:** $X \perp Y | Z$ znači $P(X,Y|Z) = P(X|Z)P(Y|Z)$
>
> **Važno:** Varijable mogu biti marginalno zavisne ali uvjetno nezavisne (i obrnuto)!

---

**5. Kako se mjeri zavisnost između varijabli?**

> **Uzajamna informacija:**
> $$I(X,Y) = \sum_{x,y} P(x,y) \ln \frac{P(x,y)}{P(x)P(y)}$$
>
> - $I(X,Y) = 0$ → nezavisne
> - $I(X,Y) > 0$ → zavisne (veća vrijednost = jača zavisnost)
>
> Koristi se za odluku koje značajke združiti u polunaivnom Bayesu.

---

**6. Usporedi broj parametara: puna izglednost vs. naivni Bayes**

> Za n binarnih značajki i K klasa:
>
> | Model           | Broj parametara                           |
> | --------------- | ----------------------------------------- |
> | Puna izglednost | $K \cdot (2^n - 1)$ → **eksponencijalno** |
> | Naivni Bayes    | $K \cdot n$ → **linearno**                |
>
> Zato naivni Bayes može generalizirati, a puna izglednost ne može.

---

### ⚠️ Zamke na ispitu (Cjelina 16)

1. **Gaussov Bayes = Logistička regresija** samo ako je kovarijacijska matrica **dijeljena**!

2. **Naivni Bayes uvijek koristi zaglađivanje** (MAP, ne MLE) za izglednosti

3. **Uvjetna nezavisnost ≠ marginalna nezavisnost** - mogu biti različite!

4. **Broj parametara:**
   - Puna izglednost: eksponencijalan
   - Naivni Bayes: linearan

5. **Uzajamna informacija** mjeri zavisnost (ne korelaciju!)

---

### 🎯 Stvarna ispitna pitanja (Cjelina 16)

#### Pitanje 1: Što znači da su GBC i LR generativno-diskriminativni par?

| Odgovor  | Tvrdnja                                                                                                                       |
| -------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **✅ A** | Aposteriorna vjerojatnost klase za GBC može se izraziti kao **poopćeni linearni model sa sigmoidnom aktivacijskom funkcijom** |
| B        | GBC i neregularizirana LR modeliraju identične distribucije zajedničke vjerojatnosti                                          |
| C        | Izlaz modela LR jednak je zajedničkoj vjerojatnosti modela GBC                                                                |
| D        | GBC i LR ostvaruju istu pogrešku na skupu za učenje                                                                           |

> **Objašnjenje:** GBC s dijeljenom $\Sigma$ daje $P(y=1|x) = \sigma(w^Tx + w_0)$, što je **točno forma logističke regresije** (poopćeni linearni model sa sigmoidom)!

---

#### Pitanje 2: Što je točno za par GBC (dijeljena Σ) i LR bez regularizacije?

| Odgovor  | Tvrdnja                                                                         |
| -------- | ------------------------------------------------------------------------------- |
| A        | GBC i LR optimiraju različite funkcije pogreške, pa mogu dati različite granice |
| B        | Učenje GBC je računalno složenije od učenja LR                                  |
| **✅ C** | Oba modela daju **linearnu granicu**, ali GBC ima **više parametara** od LR     |
| D        | Vjerojatnosni izlaz GBC odgovara komplementu izlaza LR                          |

> **Objašnjenje:**
>
> - Oba daju linearnu granicu (zato su par!)
> - GBC: $\frac{n(n+1)}{2} + 2n + 1$ parametara
> - LR: $n + 1$ parametara
>
> GBC ima puno više parametara jer modelira cijelu $p(x,y)$.

---

#### Pitanje 3: Po čemu se polunaivan Bayes (SNBC) razlikuje od naivnog (NBC)?

| Odgovor  | Tvrdnja                                                                        |
| -------- | ------------------------------------------------------------------------------ |
| A        | SNBC pretpostavlja zavisnosti, ali ima manje parametara od NBC                 |
| B        | SNBC ima više parametara, ali manje bridova u Bayesovoj mreži                  |
| C        | SNBC faktorizira u manje faktora, pa ima manje parametara                      |
| **✅ D** | SNBC ima **više parametara** od NBC te **modelira zavisnosti** između značajki |

> **Objašnjenje:** Polunaivni Bayes:
>
> - **Združuje** neke značajke u zajedničke faktore (npr. $P(x_2, x_3|y)$ umjesto $P(x_2|y)P(x_3|y)$)
> - Time bolje modelira zavisnosti
> - Ali ima **više parametara** (zajednički faktor ima više kombinacija)

---

#### Pitanje 4: Kako KL-divergencija mjeri zavisnost varijabli?

| Odgovor  | Tvrdnja                                                                                                         |
| -------- | --------------------------------------------------------------------------------------------------------------- |
| A        | Manje zavisne → manja KL-divergencija između marginalnih i uvjetne vjerojatnosti                                |
| B        | Manje zavisne → veća KL-divergencija između faktorizirane i marginalne vjerojatnosti                            |
| **✅ C** | **Više zavisne** → **veća KL-divergencija** između zajedničke vjerojatnosti $P(X,Y)$ i faktorizirane $P(X)P(Y)$ |
| D        | Više zavisne → manja KL-divergencija između zajedničke i faktorizirane vjerojatnosti                            |

> **Objašnjenje:** Uzajamna informacija:
> $$I(X,Y) = D_{KL}(P(X,Y) || P(X)P(Y))$$
>
> - Ako su varijable **nezavisne**: $P(X,Y) = P(X)P(Y)$ → $I(X,Y) = 0$
> - Ako su **zavisne**: $P(X,Y) \neq P(X)P(Y)$ → $I(X,Y) > 0$
> - **Jača zavisnost** = veće odstupanje = **veća KL-divergencija**

---

### 🧮 Praktične formule za numeričke zadatke (Cjelina 16)

#### Broj parametara - usporedba modela

**Za n značajki, K klasa:**

| Model                           | Broj parametara                 |
| ------------------------------- | ------------------------------- |
| Logistička regresija            | $n + 1$                         |
| GBC (dijeljena $\Sigma$)        | $\frac{n(n+1)}{2} + Kn + (K-1)$ |
| Naivan Bayes (binarne značajke) | $K \cdot n + (K-1)$             |
| Polunaivan Bayes                | Ovisi o združivanju             |

**Primjer (zadatak 1):** Za n=100, K=2:

- LR: $100 + 1 = 101$
- GBC: $\frac{100 \cdot 101}{2} + 2 \cdot 100 + 1 = 5050 + 201 = 5251$
- Razlika: $5251 - 101 = 5150$

---

#### Naivan Bayes - korak po korak

**Za primjer** $x = (x_1, x_2, ..., x_n)$:

1. **Izračunaj P(y=j)** za svaku klasu (Laplace):
   $$P(y=j) = \frac{N_j + 1}{N + K}$$

2. **Izračunaj P(x_k|y=j)** za svaku značajku (Laplace):
   $$P(x_k = v | y=j) = \frac{N_{k,v,j} + 1}{N_j + K_k}$$
   gdje je $K_k$ broj mogućih vrijednosti značajke $x_k$

3. **Izračunaj nenormaliziranu aposteriornu:**
   $$P(y=j) \cdot \prod_k P(x_k | y=j)$$

4. **Normaliziraj:**
   $$P(y=j|x) = \frac{P(y=j) \prod_k P(x_k|y=j)}{\sum_{j'} P(y=j') \prod_k P(x_k|y=j')}$$

---

#### Polunaivan Bayes - združeni faktori

Ako združujemo značajke $x_i$ i $x_j$:

**Umjesto:** $P(x_i|y) \cdot P(x_j|y)$

**Koristimo:** $P(x_i, x_j|y)$ (zajednički faktor)

**Broj parametara za združeni faktor:**
$$(K_i \cdot K_j - 1) \cdot K$$

---

#### Uvjetna nezavisnost - provjera

**Naivni Bayes pretpostavlja:** $P(x_i|y) = P(x_i|x_j, y)$

**Pitanje tipa:** "Koja jednakost NE vrijedi?"

Traži parove značajki koje su **zavisne unutar klase**:

- Ako je $x_i$ = "stožer" i $x_j$ = "pandemija", unutar klase y=1 (korona članak):
  - $P(\text{stožer}|y=1) \neq P(\text{stožer}|\text{pandemija}, y=1)$
  - Jer ako je članak o pandemiji i sadrži "pandemija", vjerojatnije je da sadrži i "stožer"

---

#### Uzajamna informacija iz podataka

**Korak 1:** Procijeni $P(x_i, x_j)$ s Laplaceovim zaglađivanjem

**Korak 2:** Procijeni marginalne $P(x_i)$ i $P(x_j)$

**Korak 3:** Izračunaj:
$$I(x_i, x_j) = \sum_{v_i, v_j} P(x_i=v_i, x_j=v_j) \cdot \ln\frac{P(x_i=v_i, x_j=v_j)}{P(x_i=v_i) \cdot P(x_j=v_j)}$$

**Odluka za polunaivan Bayes:**

- Ako $I(x_i, x_j) > \text{prag}$ (npr. 0.01) → **združi** $x_i$ i $x_j$

---

#### Broj parametara - složeni modeli

**Za mješovite značajke** (diskretne + kontinuirane):

| Komponenta                                    | Parametri                                                      |
| --------------------------------------------- | -------------------------------------------------------------- |
| Kategorička ($K_k$ vrijednosti)               | $(K_k - 1) \cdot K$ za svaku klasu                             |
| Kontinuirana (dijeljena dijagonalna $\Sigma$) | $n_{cont}$ varijanci + $K \cdot n_{cont}$ srednjih vrijednosti |
| Združeni faktor $(x_i, x_j)$                  | $(K_i \cdot K_j - 1) \cdot K$                                  |
| Prior                                         | $K - 1$                                                        |

---

### 📊 Tipovi numeričkih zadataka (Cjelina 16)

| Zadatak | Što se računa                  | Ključno                                    |
| ------- | ------------------------------ | ------------------------------------------ | ----------------------------------- |
| 1       | Razlika parametara GBC - LR    | Formula $\frac{n(n+1)}{2}$ za kov. matricu |
| 2       | $P(y=1                         | x)$ naivni Bayes                           | Laplace zaglađivanje!               |
| 3       | Koja nezavisnost NE vrijedi?   | Traži zavisne značajke unutar klase        |
| 4       | $P(y=1                         | x)$ polunaivan Bayes                       | Združeni faktor za zavisne značajke |
| 5       | Ukupno parametara 3 modela     | Zbroji sve komponente                      |
| 6       | Faktorizacija iz uzajamne info | $I > 0.01$ → združi                        |
| 7       | Izračun uzajamne informacije   | $I(x_i, x_j)$ iz podataka s Laplaceom      |

---

## Cjelina 17: Probabilistički grafički modeli

> ✅ **Ova cjelina JE u labosu!** - koristi se `pgmpy` biblioteka

---

### Što su PGM-ovi?

**Probabilistički grafički modeli (PGM)** su sažet način zapisa **zajedničke distribucije** pomoću grafa.

- **Čvorovi** = sluačajne varijable
- **Bridovi** = zavisnosti između varijabli
- Svaka varijabla interagira samo s manjim brojem drugih varijabli (**lokalne zavisnosti**)

**Dvije osnovne porodice:**

| Vrsta                 | Graf                           | Tipično učenje  |
| --------------------- | ------------------------------ | --------------- |
| **Bayesove mreže**    | Usmjereni aciklički graf (DAG) | Generativno     |
| **Markovljeve mreže** | Neusmjereni graf               | Diskriminativno |

**Tri aspekta PGM-a:**

1. **Reprezentacija** - kako zapisati zajedničku distribuciju
2. **Zaključivanje (inference)** - odrediti vrijednosti nepoznatih varijabli
3. **Učenje** - naučiti parametre (i strukturu) iz podataka

---

### Bayesove mreže (Belief Networks)

**Bayesova mreža** = usmjereni aciklički graf (DAG) + uvjetne vjerojatnosne distribucije (CPD)

#### Faktorizacija zajedničke distribucije

Za Bayesovu mrežu sa n čvorova:

$$p(x) = \prod_{k=1}^{n} p(x_k | pa(x_k))$$

gdje $pa(x_k)$ označava **roditelje** čvora $x_k$.

> 📌 **Ključno:** Čvorovi se mogu poredati u **topološki uređaj** - roditelji uvijek dolaze prije djece!

#### Primjer faktorizacije

Za mrežu: $x \rightarrow y \rightarrow z$

$$p(x, y, z) = p(x) \cdot p(y|x) \cdot p(z|y)$$

#### Pravilo lanca (Chain Rule)

Svaku zajedničku distribuciju možemo faktorizirati:

$$p(x_1, ..., x_n) = \prod_{k=1}^{n} p(x_k | x_1, ..., x_{k-1})$$

> ⚠️ **Problem:** Potpuno povezan graf ima **eksponencijalno** parametara!
>
> **Rješenje:** Uvesti **uvjetne nezavisnosti** → pojednostaviti faktorizaciju

---

### Uređajno Markovljevo svojstvo

$$x_k \perp (pred(x_k) \setminus pa(x_k)) | pa(x_k)$$

**Značenje:** Ako su poznate vrijednosti roditelja, čvor $x_k$ je nezavisan od svih prethodnika koji nisu roditelji.

---

### D-odvajanje (D-separation)

**Svrha:** Odrediti jesu li dvije varijable **uvjetno nezavisne** analizom staza u grafu.

#### Tri osnovna slučaja

| Struktura                       | Naziv               | Graf                  | z neopažen         | z opažen           |
| ------------------------------- | ------------------- | --------------------- | ------------------ | ------------------ |
| $x \leftarrow z \rightarrow y$  | **Račvanje (fork)** | Zajednički uzrok      | x, y **ZAVISNI**   | x, y **NEZAVISNI** |
| $x \rightarrow z \rightarrow y$ | **Lanac (chain)**   | Sekvenca              | x, y **ZAVISNI**   | x, y **NEZAVISNI** |
| $x \rightarrow z \leftarrow y$  | **Sraz (collider)** | Zajednička posljedica | x, y **NEZAVISNI** | x, y **ZAVISNI**   |

> ⚠️ **KRITIČNO ZA ISPIT:** Sraz je **SUPROTAN** od račvanja i lanca!

#### Pravila d-odvajanja (sažetak)

**Staza je d-odvojena** ako:

1. Sadrži **lanac** ili **račvanje** gdje je srednji čvor **OPAŽEN**
2. Sadrži **sraz** gdje srednji čvor (i svi njegovi sljedbenici) **NISU OPAŽENI**

**Čvorovi x i y su uvjetno nezavisni** ⟺ **SVE staze** između njih su d-odvojene

---

### Efekt objašnjavanja (Explaining Away)

**Ključni koncept za ispit i labos!**

Kod **sraza** ($x \rightarrow z \leftarrow y$):

- Apriorno: $x \perp y$ (nezavisni)
- Ako opazimo z: $x \not\perp y | z$ (postaju zavisni!)

**Intuicija:** x i y se "natječu" za objašnjavanje z.

#### Primjer s novčićima

- x, y = dva novčića (nezavisni)
- z = zbroj novčića

Ako opazimo z=1 i x=0, onda **mora** biti y=1!

→ Opažanje z **inducira zavisnost** između x i y.

#### Primjer s prskalicom (LABOS!)

```
      Cloudy (C)
       /     \
      ↓       ↓
 Sprinkler  Rain
    (S)      (R)
      \       /
       ↓     ↓
     Wet Grass (W)
```

**Efekt objašnjavanja:**

- $S \perp R | C$ (nezavisni ako znamo je li oblačno)
- $S \not\perp R | C, W$ (zavisni ako znamo je li trava mokra!)

**Zašto?** Ako je trava mokra i pada kiša, manje je vjerojatno da je radila prskalica (jer kiša već objašnjava mokru travu).

---

### Primjeri Bayesovih mreža

#### 1. Naivni Bayes kao Bayesova mreža

```
        y
      / | \
     ↓  ↓  ↓
    x₁ x₂ x₃
```

Faktorizacija: $p(x, y) = p(y) \prod_j p(x_j | y)$

#### 2. Polunaivni Bayes

```
        y
      / | \
     ↓  ↓  ↓
    x₁ x₂→x₃
```

Faktorizacija: $p(x, y) = p(y) \cdot p(x_1|y) \cdot p(x_2|y) \cdot p(x_3|x_2, y)$

#### 3. Skriveni Markovljev model (HMM)

```
z₁ → z₂ → z₃ → ...  (skrivena stanja)
↓    ↓    ↓
x₁   x₂   x₃  ...   (opažanja)
```

Faktorizacija: $p(x, z) = p(z_1)p(x_1|z_1) \prod_{k=2}^{n} p(z_k|z_{k-1})p(x_k|z_k)$

---

### 🎯 Moguća ispitna pitanja (Cjelina 17)

**Q1: Što je probabilistički grafički model (PGM)?**

> **A:** PGM je sažet način zapisa zajedničke distribucije pomoću grafa, gdje čvorovi predstavljaju varijable, a bridovi zavisnosti između njih. Temelji se na pretpostavkama o uvjetnoj nezavisnosti koje pojednostavljuju faktorizaciju.

**Q2: Koja je razlika između Bayesovih mreža i Markovljevih mreža?**

> **A:** Bayesove mreže koriste **usmjereni aciklički graf (DAG)** i tipično se uče generativno, dok Markovljeve mreže koriste **neusmjereni graf** i tipično se uče diskriminativno. Svaka može prikazati zavisnosti koje druga ne može.

**Q3: Što je uređajno Markovljevo svojstvo?**

> **A:** $x_k \perp (pred(x_k) \setminus pa(x_k)) | pa(x_k)$ - čvor je uvjetno nezavisan od svih prethodnika (po topološkom uređaju) koji nisu njegovi roditelji, ako znamo vrijednosti roditelja.

**Q4: Navedite i objasnite tri slučaja d-odvajanja.**

> **A:**
>
> - **Račvanje** ($x \leftarrow z \rightarrow y$): x i y nezavisni ako je z opažen
> - **Lanac** ($x \rightarrow z \rightarrow y$): x i y nezavisni ako je z opažen
> - **Sraz** ($x \rightarrow z \leftarrow y$): x i y nezavisni ako z NIJE opažen (suprotno!)

**Q5: Što je efekt objašnjavanja (explaining away)?**

> **A:** Fenomen kod strukture sraza: dvije apriorno nezavisne varijable postaju zavisne kada opazimo njihovu zajedničku posljedicu. Intuitivno, varijable se "natječu" za objašnjavanje posljedice.

**Q6: Zašto PGM-ovi mogu generalizirati, dok potpuno povezani modeli ne mogu?**

> **A:** PGM-ovi uvode pretpostavke o **uvjetnoj nezavisnosti** koje smanjuju broj parametara s eksponencijalnog na polinomijalni. Bez tih pretpostavki, kombinacije vrijednosti koje se nisu pojavile u učenju imaju vjerojatnost 0.

---

### 📋 Teorijska pitanja s ispita (Cjelina 17)

**1. (T) Za Bayesovu mrežu kažemo da je generativni i parametarski model. Zašto?**

| Odgovor | Tekst                                                                                                                                                                                                                                                                                  |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A       | Generativni jer definira zajedničku vjerojatnost svih varijabli, i opaženih i skrivenih, a parametarski jer se parametri modela mogu dobiti MLE-procjenom za svaki čvor Bayesove mreže zasebno                                                                                         |
| B       | Generativni jer se može koristiti za generiranje skupa primjera na temelju zajedničke distribucije, a parametarski jer su broj čvorova mreže i njihovo povezivanje definirani parametrima                                                                                              |
| C       | Generativni jer svaki čvor odgovara uvjetnoj vjerojatnosti koja je, na temelju Markovljevog uređajnog svojstva, generirana distribucijama čvorova roditelja, a parametarski jer Bayesova mreža zapravo definira zajedničku distribuciju koja je opisana skupom parametara              |
| **✓ D** | **Generativni jer opisuje postupak kojim se mogu generirati podatci koji se pokoravaju određenoj zajedničkoj vjerojatnosnoj distribuciji, a parametarski jer svaki čvor Bayesove mreže definira uvjetnu vjerojatnost preko teorijske distribucije koja je opisana svojim parametrima** |

> 📌 **Objašnjenje:**
>
> - **Generativni** = model opisuje **generativnu priču** - kako se podatci generiraju
> - **Parametarski** = koristi teorijske distribucije (Bernoulli, Gaussian...) s parametrima koje procjenjujemo

---

**2. (T) Bayesove mreže na sažet način prikazuju zajedničku distribuciju te kodiraju uvjetne stohastičke nezavisnosti između varijabli. Koja je veza između uvjetnih nezavisnosti varijabli u Bayesovoj mreži i opasnosti od prenaučenosti?**

| Odgovor | Tekst                                                                                                                                                                                |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| A       | Uvođenjem pretpostavki o uvjetnoj nezavisnosti povećava se broj čvorova mreže, a time i broj parametara, što model čini složenijim i time sklonijim prenaučenosti                    |
| **✓ B** | **Uvođenje pretpostavki o uvjetnoj nezavisnosti pojednostavljuje strukturu Bayesove mreže i smanjuje broj parametara, čime se smanjuje i mogućnost prenaučenosti**                   |
| C       | Uvjetne nezavisnosti određuju strukturu mreže na način da definiraju koji su čvorovi međusobno povezani, međutim to nema utjecaja na složenost modela niti na sklonost prenaučenosti |
| D       | Pretpostavke o uvjetnoj nezavisnosti čine induktivnu pristranost modela, pa što je više uvjetnih nezavisnosti, to je veća pristranost i model je lakše prenaučiti                    |

> 📌 **Objašnjenje:** Uvjetne nezavisnosti **uklanjaju bridove** → manje parametara → manja složenost → **manja prenaučenost**!

---

**3. (T) Bayesova mreža na sažet način definira zajedničku distribuciju vjerojatnosti uz određene pretpostavke uvjetne nezavisnosti. Neka je jedna takva pretpostavka $x_1 \perp \{x_2, x_3\} | x_4$. Koji je efekt uvođenja ove pretpostavke na graf Bayesove mreže?**

| Odgovor | Tekst                    |
| ------- | ------------------------ |
| A       | Dodavanje dva brida      |
| B       | Dodavanje tri brida      |
| **✓ C** | **Uklanjanje dva brida** |
| D       | Uklanjanje tri brida     |

> 📌 **Objašnjenje:** Pretpostavka $x_1 \perp \{x_2, x_3\} | x_4$ znači:
>
> - $x_1$ je nezavisan od $x_2$ (uz $x_4$) → **uklanja se brid** $x_2 - x_1$
> - $x_1$ je nezavisan od $x_3$ (uz $x_4$) → **uklanja se brid** $x_3 - x_1$
> - Ukupno: **2 brida se uklanjaju**

---

**4. (T) Skriveni Markovljev model (HMM) posebna je vrsta Bayesove mreže. Na što se odnosi pridjev "skriveni" u nazivu tog modela?**

| Odgovor | Tekst                                                                                     |
| ------- | ----------------------------------------------------------------------------------------- |
| A       | Model opisuje prijelaze između stanja, a trenutačno stanje ovisi samo o prethodnom stanju |
| **✓ B** | **Neke varijable modela nisu opažene u podatcima, ali zavise o opaženim varijablama**     |
| C       | Opažene varijable ovise samo o trenutačnom stanju i prethodno opaženoj varijabli          |
| D       | Stanja modela poredana su u lanac, a izlazi modela vidljivi su samo za posljednje stanje  |

> 📌 **Objašnjenje:** U HMM-u:
>
> - **Skrivena stanja** $z_1, z_2, ...$ → NISU opažena u podatcima
> - **Opažanja** $x_1, x_2, ...$ → ono što vidimo
> - "Skriveni" = stanja procesa su **latentne varijable** koje ne možemo direktno mjeriti

---

**5. (T) Bayesova mreža može se upotrijebiti za modeliranje kauzalnih odnosa između varijabli. Jedan primjer takvog zaključivanja jest "efekt objašnjavanja". Gdje u Bayesovoj mreži nastupa efekt objašnjavanja i kako se on manifestira?**

| Odgovor | Tekst                                                                                                                                     |
| ------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **✓ A** | **U strukturi $x \rightarrow z \leftarrow y$, gdje su uzroci x i y nezavisni, ali postaju zavisni ako je opažena posljedica z**           |
| B       | U strukturi $x \rightarrow z \rightarrow y$, gdje su uzrok x i posljedica y zavisni, ali postaju nezavisni ako je opažen posredni uzrok z |
| C       | U strukturi $x \leftarrow z \rightarrow y$, gdje su uzroci x i y zavisni, ali postaju nezavisni ako je opažena posljedica z               |
| D       | U strukturi $x \rightarrow z \rightarrow y$, gdje su uzrok x i posljedica y nezavisni, ali postaju zavisni ako je opažen posredni uzrok z |

> 📌 **Objašnjenje:** Efekt objašnjavanja = **SRAZ** ($x \rightarrow z \leftarrow y$)
>
> - Apriorno: $x \perp y$ (nezavisni)
> - Ako opazimo z: $x \not\perp y | z$ (zavisni!)
> - Intuicija: x i y se **"natječu" za objašnjavanje** z

> ⚠️ **ZAMKA:** Odgovor C opisuje **račvanje** (fork), ne sraz! Kod račvanja je OBRNUTO - opažanje z čini x i y NEZAVISNIMA.

---

### 🧮 Praktične formule za numeričke zadatke (Cjelina 17)

#### Broj parametara u Bayesovoj mreži

Za diskretnu varijablu $x_k$ s $K_k$ vrijednosti i roditeljima koji imaju ukupno $\prod_j K_{pa_j}$ kombinacija:

$$\text{Parametri za } x_k = (K_k - 1) \cdot \prod_{j \in pa(x_k)} K_j$$

**Ukupno parametara** = suma po svim čvorovima

#### Primjer: Prskalica

| Čvor       | Roditelji | Kombinacija roditelja | Vrijednosti | Parametri |
| ---------- | --------- | --------------------- | ----------- | --------- |
| C          | -         | 1                     | 2           | 1         |
| S          | C         | 2                     | 2           | 2         |
| R          | C         | 2                     | 2           | 2         |
| W          | S, R      | 4                     | 2           | 4         |
| **Ukupno** |           |                       |             | **9**     |

#### Računanje d-odvajanja korak po korak

1. **Identificiraj sve staze** između dva čvora (ignoriraj smjer bridova)
2. **Za svaku stazu** provjeri:
   - Ako je **lanac/račvanje** → srednji čvor mora biti **opažen** da odvojimo
   - Ako je **sraz** → srednji čvor (i sljedbenici) moraju biti **neopaženi** da odvojimo
3. **Čvorovi su nezavisni** ⟺ **sve staze su odvojene**

#### Primjer: Jesu li C i W nezavisni?

Staze C → W:

1. C → S → W (lanac)
2. C → R → W (lanac)

Za nezavisnost: oba S i R moraju biti opaženi!

→ $C \perp W | S, R$ (da)
→ $C \not\perp W$ (ne, ako S i R nisu opaženi)

---

### 📊 Tipovi numeričkih zadataka (Cjelina 17)

| Zadatak | Što se računa                    | Ključno                                              |
| ------- | -------------------------------- | ---------------------------------------------------- | --------- |
| 1       | Konstrukcija BN iz faktorizacije | Bridovi idu od uvjetujuće prema uvjetovanoj          |
| 2       | Faktorizacija iz dane BN         | $p(x) = \prod p(x_k                                  | pa(x_k))$ |
| 3       | D-odvajanje                      | Račvanje/lanac: opažen odvaja; Sraz: neopažen odvaja |
| 4       | Efekt objašnjavanja              | Sraz + opažena posljedica → zavisnost                |
| 5       | Broj parametara                  | $(K_k - 1) \cdot \prod K_{pa}$ za svaki čvor         |
| 6       | pgmpy upiti                      | `infer.query(['X'], evidence={'Y': val})`            |

---

### 🧮 Napomene za problemske zadatke (Cjelina 17)

#### Zadatak tip 1: Usporedba broja parametara modela

**Primjer:** Polunaivni Bayes s binarnim značajkama i klasom

Za **binarne varijable** (K=2):

- Svaki čvor bez roditelja: **1 parametar** (jer P(x=0) = 1 - P(x=1))
- Svaki čvor s jednim roditeljem: **2 parametra** (po 1 za svaku vrijednost roditelja)
- Svaki čvor s dva roditelja: **4 parametra** (2×2 kombinacije)

**Model H₁ (naivni Bayes):** y → x₁, y → x₂, y → x₃

- P(y): 1 param
- P(x₁|y), P(x₂|y), P(x₃|y): svaki 2 → ukupno 6
- **Ukupno: 7 parametara**

**Model H₂ (polunaivni):** dodaje brid x₂ → x₃

- P(y): 1 param
- P(x₁|y): 2 param
- P(x₂|y): 2 param
- P(x₃|x₂,y): 4 param (2 roditelja!)
- **Ukupno: 9 parametara** (+2 od H₁)

**Model H₃ (potpuno povezan):** x₁ → x₂ → x₃

- P(y): 1
- P(x₁|y): 2
- P(x₂|x₁,y): 4
- P(x₃|x₁,x₂,y): 8
- **Ukupno: 15 parametara** (+6 od H₂)

> **Odgovor za tip 1:** H₂ ima **2 više** od H₁, **6 manje** od H₃ → **Odgovor B**

---

#### Zadatak tip 2: Uvjetne nezavisnosti iz faktorizacije

**Postupak:**

1. Nacrtaj graf iz faktorizacije (brid: uvjet → uvjetovana)
2. Odredi topološki uređaj (roditelji prije djece)
3. Primijeni Markovljevo svojstvo: $x_k \perp (pred(x_k) \setminus pa(x_k)) | pa(x_k)$

**Primjer:** $P(w,x,y,z) = P(w)P(y)P(x|w,y)P(z|w)$

Graf:

```
w → x ← y
↓
z
```

Topološki uređaj: w, y, x, z (ili w, y, z, x - ovisi o izboru)

**Markovljevo svojstvo:**

- Za x: $x \perp \emptyset | \{w,y\}$ (w,y su roditelji)
- Za z: $z \perp \{y,x\} | w$ → dobivamo **z⊥y|w** i **z⊥x|w**

> **Ključno:** Traži nezavisnosti gdje čvor NEMA direktan brid s prethodnikom!

---

#### Zadatak tip 3: Faktorizacija iz nezavisnosti + broj parametara

**Primjer:** 5 varijabli, v,w binarne, x,y ternarne, topološki uređaj v,w,x,y,z

Dane nezavisnosti:

- $v \perp w$ (marginalna)
- $w \perp x | v$
- $v \perp y | \{w,x\}$
- $\{v,w\} \perp z | \{x,y\}$

**Korak 1:** Odredi roditelje svakog čvora

- v: nema roditelja (prvi u uređaju)
- w: v je prethodnik, ali v⊥w → **nema roditelja**
- x: v,w prethodnici, w⊥x|v → **roditelj samo v**
- y: v,w,x prethodnici, v⊥y|{w,x} → **roditelji w,x**
- z: v,w,x,y prethodnici, {v,w}⊥z|{x,y} → **roditelji x,y**

**Korak 2:** Faktorizacija
$$P(v,w,x,y,z) = P(v)P(w)P(x|v)P(y|w,x)P(z|x,y)$$

**Korak 3:** Broj parametara (v,w binarne=2, x,y ternarne=3)

- P(v): 1
- P(w): 1
- P(x|v): (3-1)×2 = 4
- P(y|w,x): (3-1)×2×3 = 12
- P(z|x,y): (Kz-1)×3×3 = ?

> **Pazi:** Zadatak ne kaže je li z binarna ili ternarna! Provjeri u originalnom zadatku.

---

#### Zadatak tip 4: Efekt objašnjavanja - konkretna manifestacija

**Scenarij prometnih gužvi:**

```
J (jutro) → G (gužva) ← V (večer)
              ↓
         N (nesreća)
              ↓
         T (zastoj tramvaja) ← S (struja)
              ↓
         P (pješačenje)
```

**Efekt objašnjavanja nastupa kod SRAZA!**

Sraz: $J \rightarrow G \leftarrow V$

**Manifestacija:**

- Apriorno: $J \perp V$ (jutro i večer nezavisni)
- Ako opazimo G=1 (ima gužve): $J \not\perp V | G$

**Konkretno:** $P(V=1|G=1,J=1) < P(V=1|G=1)$

> Ako znamo da je gužva I da je jutro, **manja** je vjerojatnost da je večer (jer jutro već objašnjava gužvu)!

---

#### Zadatak tip 5: D-odvajanje - provjera tvrdnji

**Postupak:**

1. Pronađi SVE staze između dva čvora
2. Za svaku stazu provjeri je li d-odvojena
3. Čvorovi su nezavisni AKO su SVE staze odvojene

**Primjer:** Je li $x \perp z | y$?

Pronađi staze x → ... → z, provjeri za svaku:

- Lanac/račvanje na stazi: srednji čvor mora biti u evidenciji (y)
- Sraz na stazi: srednji čvor NE SMIJE biti u evidenciji

---

#### Zadatak tip 6: D-odvajanje s više varijabli

**Primjer:** $P(u,v,w,x,y,z) = P(u|x)P(v|x)P(w|v,x)P(x)P(y|u,x,z)P(z|v,w)$

**Pitanje:** Za koju varijablu je svejedno je li opažena, ako želimo da x⊥z?

**Postupak:**

1. Nacrtaj graf
2. Pronađi staze x → z
3. Za svaku provjeri što treba opaziti da bude odvojena
4. Ako neka varijabla ne utječe na odvajanje → ta je odgovor

> **Trik:** Varijabla koja NIJE na nijednoj stazi između x i z ne utječe na njihovu nezavisnost!

---

## Cjelina 18: Probabilistički grafički modeli II (Zaključivanje i učenje)

> ✅ **Ova cjelina JE u labosu!** - egzaktno zaključivanje s `VariableElimination`

---

### Zaključivanje u Bayesovim mrežama

**Cilj:** Izračunati vjerojatnost varijabli upita uz opažene varijable

#### Podjela varijabli

| Vrsta       | Oznaka | Opis                                             |
| ----------- | ------ | ------------------------------------------------ |
| **Opažene** | $x_o$  | Varijable čije vrijednosti znamo                 |
| **Upit**    | $x_q$  | Varijable čiju vjerojatnost želimo znati         |
| **Smetnje** | $x_n$  | Varijable koje nas ne zanimaju (marginaliziramo) |

#### Dvije vrste upita

**1. Aposteriorni upiti:**
$$P(x_q | x_o) = \frac{\sum_{x_n} P(x_q, x_o, x_n)}{P(x_o)} = \frac{\sum_{x_n} P(x_q, x_o, x_n)}{\sum_{x_n, x_q'} P(x_q', x_o, x_n)}$$

**2. MAP upiti (najvjerojatnije objašnjenje):**
$$x_q^* = \arg\max_{x_q} \sum_{x_n} P(x_q, x_o, x_n)$$

> ⚠️ **PAZI:** Najvjerojatniji vektor $\neq$ kombinacija zasebno najvjerojatnijih vrijednosti!

---

### Primjer zaključivanja (Prskalica)

**Upit:** Ako je trava mokra (w=1), kolika je vjerojatnost kiše i prskalice?

$$P(s=1|w=1) = \frac{P(s=1, w=1)}{P(w=1)} = \frac{\sum_{c,r} P(c,s=1,r,w=1)}{\sum_{c,r,s} P(c,s,r,w=1)}$$

**Rezultati iz mreže:**

- $P(w=1) = 0.6471$ (vjerojatnost dokaza)
- $P(s=1|w=1) = 0.43$ (43% vjerojatnost prskalice)
- $P(r=1|w=1) = 0.708$ (70.8% vjerojatnost kiše)

> 📌 **Zaključak:** Vjerojatnije je da je trava mokra zbog **kiše** nego zbog prskalice!

---

### Egzaktno zaključivanje: Eliminacija varijabli

**Problem:** Naivna konstrukcija zajedničke distribucije → **kombinatorna eksplozija** ($K^n$ kombinacija)

**Rješenje:** Dinamičko programiranje - izračunaj i pohrani međurezultate

#### Postupak eliminacije varijabli (sum-product)

1. **Presloži** faktore tako da izlučiš zajedničke članove
2. **Marginaliziraj** varijablu po varijablu
3. **Pohrani** međurezultate (memoizacija)

**Primjer:**
$$P(w) = \sum_c \sum_s \sum_r P(c)P(s|c)P(r|c)P(w|s,r)$$

Preslagivanjem:
$$P(w) = \sum_s \sum_r P(w|s,r) \underbrace{\sum_c P(c)P(s|c)P(r|c)}_{t_1(s,r)}$$

Definiraj pomoćne funkcije:

- $t_1(s,r) = \sum_c P(c)P(s|c)P(r|c)$
- $t_2(s,w) = \sum_r P(w|s,r) \cdot t_1(s,r)$
- $t_3(w) = \sum_s t_2(s,w)$

**Ušteda:** Od 62 operacije → 34 operacije!

> 📌 **Ključno:** Što manje bridova u mreži → više ponavljajućih izraza → veća ušteda

---

### Približno zaključivanje: Metode uzorkovanja

Kada je egzaktno zaključivanje preskupo, koristimo **uzorkovanje**.

#### 1. Unaprijedno uzorkovanje (Forward Sampling)

**Postupak:**

1. Kreni od korijena (po topološkom uređaju)
2. Za svaki čvor uzorkuj iz njegove uvjetne distribucije
3. Ponovi N puta → dobij uzorak iz $P(x)$

**Problem:** Uzorkuje iz zajedničke distribucije, ne iz aposteriorne!

#### 2. Uzorkovanje s odbacivanjem (Rejection Sampling)

**Postupak:**

1. Generiraj uzorak unaprijednim uzorkovanjem
2. **Odbaci** uzorke gdje $x_o$ nema željene vrijednosti
3. Koristi samo "dobre" uzorke

**Problem:** Ako je $P(x_o)$ mala, većina uzoraka se odbacuje!

#### 3. Uzorkovanje po važnosti (Importance Sampling)

**Postupak:**

1. Fiksiraj opažene varijable na željene vrijednosti
2. Uzorkuj ostale varijable
3. Dodijeli **težine** uzorcima prema izglednosti

**Problem:** Ako se distribucija uzorkovanja razlikuje od aposteriorne, procjena je loša.

#### 4. Gibbsovo uzorkovanje (MCMC) ⭐

**Najčešće korištena metoda!**

**Postupak:**

1. Kreni od slučajnog vektora $x^0$
2. **Ciklički** uzorkuj svaku varijablu iz uvjetne distribucije:
   - $x_1^{t+1} \sim P(x_1 | x_2^t, x_3^t, ...)$
   - $x_2^{t+1} \sim P(x_2 | x_1^{t+1}, x_3^t, ...)$
   - ...
3. Ponavljaj dok ne konvergira

**Za aposteriorne upite:** Fiksiraj opažene varijable, uzorkuj samo varijable upita!

**Markovljev omotač:** Uvjetna distribucija ovisi samo o:

- Roditeljima
- Djeci
- Roditeljima djece

> 📌 **Burn-in period:** Odbaci prvih nekoliko uzoraka dok se lanac ne "zagrije"

---

### Učenje Bayesovih mreža

#### 1. Potpuni podatci (sve varijable opažene)

**Ključno:** Log-izglednost se **dekomponira** po čvorovima mreže!

$$\ln L(\theta|D) = \sum_{k=1}^{n} \sum_{i=1}^{N} \ln P(x_k^{(i)} | pa(x_k^{(i)}), \theta_k)$$

**Posljedica:** Možemo nezavisno procijeniti parametre za svaki čvor!

**MLE za kategoričke varijable:**
$$\hat{\mu}_{k,j,l} = \frac{N_{k,j,l}}{N_{k,j}}$$

gdje je:

- $N_{k,j,l}$ = broj primjera s vrijednošću $l$ za varijablu $k$, uz vrijednost $j$ roditelja
- $N_{k,j}$ = ukupan broj primjera s vrijednošću $j$ roditelja

**MAP (Laplace zaglađivanje):**
$$\hat{\mu}_{k,j,l} = \frac{N_{k,j,l} + 1}{N_{k,j} + K_k}$$

#### 2. Nepotpuni podatci (skrivene varijable)

**Problem:** Log-izglednost se **NE dekomponira**!

$$\ln L(\theta|D) = \sum_{i=1}^{N} \ln \sum_z P(z^{(i)}|\theta) P(x^{(i)}|z^{(i)}, \theta)$$

Logaritam je "zapeo" između suma → **nema zatvorene forme**!

**Rješenja:**

1. **Gradijentni uspon** - iterativna optimizacija
2. **EM algoritam** - alternira između:
   - E-korak: izračunaj očekivane vrijednosti skrivenih varijabli
   - M-korak: maksimiziraj izglednost kao da su skrivene var. opažene

**Dodatni problem:** Funkcija **nije konveksna** → lokalni optimumi!

---

#### Ručno računanje na papiru

**Korak 1:** Zapiši faktorizaciju iz mreže
$$P(c,s,r,w) = P(c)P(s|c)P(r|c)P(w|s,r)$$

**Korak 2:** Za upit $P(s|w=1)$, marginaliziraj po c i r:
$$P(s|w=1) = \frac{\sum_{c,r} P(c)P(s|c)P(r|c)P(w=1|s,r)}{\sum_{c,r,s} P(c)P(s|c)P(r|c)P(w=1|s,r)}$$

**Korak 3:** Uvrstiti vrijednosti iz CPT tablica i izračunati!

#### Važno pitanje iz labosa

**Q:** Zašto je $P(c=1) \neq P(c=1|s=1,r=1)$ ako S i R nisu roditelji od C?

**A:** Zbog **efekta objašnjavanja**!

- C → S i C → R tvore **račvanje**
- S → W ← R tvori **sraz**
- Kada opazimo S=1 i R=1, to nam daje informaciju o C (preko račvanja)
- Konkretno: ako znamo da radi prskalica I pada kiša, to nam govori nešto o oblačnosti!

---

### 🎯 Moguća ispitna pitanja (Cjelina 18)

**Q1: Koja je razlika između aposteriornih upita i MAP upita?**

> **A:** Aposteriorni upiti vraćaju **cijelu distribuciju** $P(x_q|x_o)$, dok MAP upiti vraćaju **najvjerojatniju vrijednost** $\arg\max_{x_q} P(x_q|x_o)$.

**Q2: Zašto je egzaktno zaključivanje NP-teško?**

> **A:** Broj kombinacija vrijednosti raste **eksponencijalno** s brojem varijabli ($K^n$). Eliminacija varijabli ovisi o veličini najvećeg faktora.

**Q3: Kako eliminacija varijabli štedi računske operacije?**

> **A:** Koristi **dinamičko programiranje** - pohranjuje međurezultate (memoizacija). Što je graf rjeđi, više izraza se ponavlja i veća je ušteda.

**Q4: Zašto je uzorkovanje s odbacivanjem neefikasno?**

> **A:** Ako je vjerojatnost dokaza $P(x_o)$ mala, većina uzoraka ne odgovara opaženim vrijednostima i odbacuje se. Za rijetke događaje trebamo ogromno uzoraka.

**Q5: Što je Markovljev omotač i zašto je važan za Gibbsovo uzorkovanje?**

> **A:** Markovljev omotač čvora su njegovi **roditelji, djeca i roditelji djece**. Uvjetna distribucija varijable ovisi samo o varijablama u omotaču, što omogućava efikasno Gibbsovo uzorkovanje.

**Q6: Zašto se kod nepotpunih podataka log-izglednost ne dekomponira?**

> **A:** Zbog marginalizacije po skrivenim varijablama, logaritam ostaje "zarobljen" između suma i ne može se raspodijeliti po čvorovima. Zato nema rješenja u zatvorenoj formi.

---

### 📋 Teorijska pitanja s ispita (Cjelina 18)

**1. (T) Na koji način izračunavamo aposteriorni upit?**

| Odgovor | Tekst                                                                                                                                                               |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **✓ A** | **Kao omjer zajedničke vjerojatnosti marginalizirane po varijablama smetnje i zajedničke vjerojatnosti marginalizirane po varijablama smetnje i varijablama upita** |
| B       | Kao omjer zajedničke vjerojatnosti marginalizirane po varijablama upita i zajedničke vjerojatnosti marginalizirane po opaženim varijablama                          |
| C       | Kao umnožak zajedničke vjerojatnosti marginalizirane po opaženim varijablama i zajedničke vjerojatnosti marginalizirane po varijablama smetnje                      |
| D       | Kao umnožak vjerojatnosti varijable upita uvjetovane na opažene varijable i zajedničke vjerojatnosti marginalizirane po varijablama smetnje                         |

> 📌 **Formula:**
> $$P(x_q|x_o) = \frac{\sum_{x_n} P(x_q, x_o, x_n)}{\sum_{x_n, x_q} P(x_q, x_o, x_n)}$$
>
> - **Brojnik:** marginaliziraj samo po smetnji ($x_n$)
> - **Nazivnik:** marginaliziraj po smetnji ($x_n$) I upitu ($x_q$)

---

**2. (T) Kako je definiran rezultat MAP-upita?**

| Odgovor | Tekst                                        |
| ------- | -------------------------------------------- |
| A       | $\arg\max_{x_o} \sum_{x_n} p(x_q, x_o, x_n)$ |
| B       | $\arg\max_{x_o} \sum_y p(x_q, x_o, x_n)$     |
| **✓ C** | $\arg\max_{x_q} \sum_{x_n} p(x_q, x_o, x_n)$ |
| D       | $\arg\max_{x_q} \sum_{x_n} p(x_q, x_o, x_n)$ |

> 📌 **Objašnjenje:** MAP traži **najvjerojatniju vrijednost za $x_q$** (varijable upita), ne za $x_o$ (opažene)!
>
> - Marginaliziramo po $x_n$ (smetnje)
> - Maksimiziramo po $x_q$ (upit)

---

**3. (T) Zašto radimo uzorkovanje iz Bayesove mreže da bismo procijenili parametre distribucije, kad te parametre već imamo?**

| Odgovor | Tekst                                                                                                                                     |
| ------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| A       | Ne trebamo znati parametre svih čvorova, već samo čvorova roditelja onih distribucija za koje želimo procijeniti parametre                |
| B       | Vrijednosti parametara svih distribucija su procjene koje inicijaliziramo i zatim iterativno ažuriramo u svakom koraku uzorkovanja        |
| **✓ C** | **Uzorkovanje koristimo da bismo procijenili parametre bilo koje distribucije, a ne samo uvjetnih distribucija u čvorovima mreže**        |
| D       | Uzorkovanjem procjenjujemo parametre latentnih varijabli, čije vrijednosti ne opažamo, pa nam ti parametri nisu poznati prije uzorkovanja |

> 📌 **Objašnjenje:** Parametri CPD-ova u mreži su poznati, ali nas zanima **aposteriorna distribucija** $P(x_q|x_o)$ koja nije direktno zadana u mreži. Uzorkovanjem iz mreže možemo procijeniti parametre **bilo koje** derivirane distribucije!

---

**4. (T) Koji je nedostatak metode uzorkovanja s odbacivanjem?**

| Odgovor | Tekst                                                                                                            |
| ------- | ---------------------------------------------------------------------------------------------------------------- |
| **✓ A** | **Ako je vjerojatnost $P(x_o)$ mala, treba generirati mnogo vektora da bi uzorak bio velik i procjena pouzdana** |
| B       | Ako je vjerojatnost $P(x_o)$ velika, mnogo će generiranih vektora biti odbačeno i procjena će biti pristrana     |
| C       | Ako je vjerojatnost $P(x_o)$ mala, generiramo vektore iz apriorne distribucije $P(x_q)$ i procjena je pristrana  |
| D       | Ako je vjerojatnost $P(x_o)$ velika, generirani vektori nisu iz aposteriorne distribucije i procjena je netočna  |

> 📌 **Objašnjenje:** Ako je $P(x_o)$ mala (rijedak događaj), većina uzoraka **neće** imati tražene vrijednosti opaženih varijabli i bit će odbačeni. Trebamo generirati **ogromno** uzoraka da bismo dobili dovoljno "dobrih"!

---

**5. (T) Koji je problem kod primjene unaprijednog uzorkovanja za izračun aposteriornih upita nad Bayesovom mrežom?**

| Odgovor | Tekst                                                                                     |
| ------- | ----------------------------------------------------------------------------------------- |
| A       | Mnogo uzorkovanih vektora morat će biti odbačeni, pa procjena neće biti pouzdana          |
| **✓ B** | **Dobiveni vektori bit će uzorkovani iz apriorne, a ne aposteriorne distribucije**        |
| C       | Kod marginalizacije varijabli smetnje dolazi do kombinatorne eksplozije                   |
| D       | Skrivene varijable nisu opažene, pa se log-izglednost ne dekomponira po varijablama mreže |

> 📌 **Objašnjenje:** Unaprijedno uzorkovanje generira uzorke iz **zajedničke distribucije** $P(x)$, a ne iz **aposteriorne** $P(x_q|x_o)$! Za aposteriorne upite moramo koristiti druge metode (odbacivanje, Gibbs, itd.)

---

**6. (T) Što je prednost procjene parametara kod potpunih podataka (modela bez skrivenih varijabli) u odnosu na nepotpune podatke (modela sa skrivenim varijablama)?**

| Odgovor | Tekst                                                                                                                                                                                   |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A       | Kod potpunih podataka minimizacija funkcije log-izglednosti ima rješenje u zatvorenoj formi, ali funkcija nije konkavna, pa može imati više lokalnih optimuma...                        |
| B       | Kod potpunih podataka maksimizacija log-izglednosti ima rješenje u zatvorenoj formi, ali samo ako su opažene varijable na početku niza po topološkom uređaju čvorova...                 |
| C       | Kod potpunih podataka MLE procjena parametara ima rješenje u zatvorenoj formi, dok MAP procjena nema...                                                                                 |
| **✓ D** | **Kod potpunih podataka log-izglednost se dekomponira po strukturi mreže, pa parametre svake uvjetne distribucije možemo procijeniti nezavisno od drugih čvorova i u zatvorenoj formi** |

> 📌 **Ključno:**
>
> - **Potpuni podatci:** $\ln L = \sum_k \sum_i \ln P(x_k^{(i)}|pa(x_k^{(i)}))$ → **dekomponira se!**
> - **Nepotpuni podatci:** logaritam "zapne" između suma → **NE dekomponira se!**

---

**7. (T) Zašto i kako Bayesovu mrežu učimo nad nepotpunim podatcima?**

| Odgovor | Tekst                                                                                                      |
| ------- | ---------------------------------------------------------------------------------------------------------- |
| A       | Jer se log-izglednost dekomponira po čvorovima mreže, pa MLE ili MAP procjenjujemo u zatvorenoj formi      |
| B       | Jer MLE nema rješenje u zatvorenoj formi, pa umjesto MLE koristimo gradijentni uspon ili EM-algoritam      |
| **✓ C** | **Jer mreža ima skrivene varijable koje ne opažamo, pa moramo koristiti iterativne metode za MAP ili MLE** |
| D       | Jer mreža ima manje čvorova nego što je opaženih varijabli, pa koristimo eliminaciju varijabli             |

> 📌 **Objašnjenje:**
>
> - **Nepotpuni podatci** = model ima **skrivene varijable** (nisu u podatcima)
> - Log-izglednost se ne dekomponira → nema zatvorene forme
> - Koristimo **iterativne metode:** gradijentni uspon ili **EM algoritam**
> - Dodatni problem: funkcija **nije konveksna** → lokalni optimumi!

---

### 🧮 Praktične formule za numeričke zadatke (Cjelina 18)

#### Računanje uvjetne vjerojatnosti

$$P(x_q | x_o) = \frac{\sum_{x_n} P(x_q, x_o, x_n)}{\sum_{x_n, x_q} P(x_q, x_o, x_n)}$$

**Brojnik:** Marginaliziraj samo varijable smetnje
**Nazivnik:** Marginaliziraj varijable smetnje I varijable upita

#### MLE za CPT tablicu

$$\hat{P}(x_k = l | pa(x_k) = j) = \frac{\text{broj primjera s } x_k=l \text{ i } pa(x_k)=j}{\text{broj primjera s } pa(x_k)=j}$$

#### MAP za CPT tablicu (Laplace)

$$\hat{P}(x_k = l | pa(x_k) = j) = \frac{N_{k,j,l} + 1}{N_{k,j} + K_k}$$

#### Složenost eliminacije varijabli

- Ovisi o **širini stabla** (tree width) grafa
- Za lanac: $O(nK^2)$
- Za potpuno povezan graf: $O(K^n)$

---

### 📊 Tipovi numeričkih zadataka (Cjelina 18)

| Zadatak | Što se računa         | Ključno                                    |
| ------- | --------------------- | ------------------------------------------ |
| 1       | $P(x_q \| x_o)$ ručno | Marginaliziraj po $x_n$, normaliziraj      |
| 2       | Broj operacija        | Prebroji množenja i zbrajanja              |
| 3       | MLE iz podataka       | Relativna frekvencija                      |
| 4       | MAP iz podataka       | Laplace zaglađivanje                       |
| 5       | pgmpy upiti           | `infer.query(['X'], evidence={'Y': v})`    |
| 6       | Gibbsovo uzorkovanje  | Uvjetna dist. ovisi o Markovljevom omotaču |

---

### 🧮 Napomene za problemske zadatke (Cjelina 18)

#### Zadatak tip 1: Aposteriorna vjerojatnost iz CPT tablica

**Primjer:** P(R=1 | W=1, C=0) za mrežu prskalice

**Postupak:**

1. Zapiši faktorizaciju: $P(C,S,R,W) = P(C)P(S|C)P(R|C)P(W|S,R)$

2. Primijeni Bayesovo pravilo:
   $$P(R=1|W=1,C=0) = \frac{P(R=1,W=1,C=0)}{P(W=1,C=0)}$$

3. Marginaliziraj po S:
   $$P(R=1,W=1,C=0) = \sum_S P(C=0)P(S|C=0)P(R=1|C=0)P(W=1|S,R=1)$$

4. Uvrstiti vrijednosti iz CPT tablica i izračunati!

**Trik:** Fiksiraj opažene varijable (C=0, W=1), marginaliziraj samo po neopaženim (S).

---

#### Zadatak tip 2: MAP procjena parametara iz podataka

**Primjer:** BN s varijablama L, N, S, T, treniraj na N=7 primjera

**Postupak:**

1. **Prebroji frekvencije** iz tablice podataka:
   - $N_{L=1}$ = broj primjera gdje L=1
   - $N_{S=1|L=0,N=0}$ = broj primjera gdje S=1 i L=0 i N=0
   - itd.

2. **Primijeni Laplace zaglađivanje** (α=β=2):
   $$\hat{P}(X=v|pa) = \frac{N_{X=v,pa} + 1}{N_{pa} + K_X}$$

gdje je $K_X$ broj mogućih vrijednosti varijable X.

3. **Izračunaj zajedničku vjerojatnost:**
   $$P(L=1,S=1,N=1) = P(L=1) \cdot P(N=1) \cdot P(S=1|L=1,N=1)$$

> ⚠️ **PAZI:** Za ternarnu varijablu (N ima 3 vrijednosti), $K_N = 3$!

---

#### Zadatak tip 3: Uzorkovanje s odbacivanjem - broj odbačenih

**Primjer:** P(y | x=1, z=0), N=1000 uzoraka

**Postupak:**

1. Izračunaj **vjerojatnost dokaza** $P(x_o)$:
   $$P(x=1, z=0) = \sum_y P(x=1)P(y)P(z=0|x=1,y)$$

2. **Očekivani broj prihvaćenih** uzoraka:
   $$N_{prihvaćeno} = N \cdot P(x_o)$$

3. **Očekivani broj odbačenih** uzoraka:
   $$N_{odbačeno} = N - N_{prihvaćeno} = N \cdot (1 - P(x_o))$$

**Primjer izračuna:**

- $P(x=1) = 0.2$, $P(y=1) = 0.3$
- $P(z=0|x=1,y=0) = 0.8$, $P(z=0|x=1,y=1) = 0.5$
- $P(x=1,z=0) = 0.2 \cdot [0.7 \cdot 0.8 + 0.3 \cdot 0.5] = 0.2 \cdot 0.71 = 0.142$
- Prihvaćeno: $1000 \cdot 0.142 = 142$
- Odbačeno: $1000 - 142 = 858$

---

#### Zadatak tip 4: MAP upit - najvjerojatnije objašnjenje

**Primjer:** Medicinska dijagnoza, traži $\arg\max_{U,S} P(U,S|V=0,T=1)$

**Postupak:**

1. Za **svaku kombinaciju** vrijednosti varijabli upita izračunaj:
   $$P(U=u, S=s, V=0, T=1) = P(V=0)P(B)P(U|V=0,B)P(S)P(T=1|U,S)$$

   (marginaliziraj po B ako nije u upitu)

2. **Sortiraj** po vjerojatnosti, pronađi $p_1$ (najveća) i $p_2$ (druga najveća)

3. Izračunaj omjer: $p_1 / p_2$

**Kombinacije za provjeru:** (U=0,S=0), (U=0,S=1), (U=1,S=0), (U=1,S=1)

---

#### Zadatak tip 5: MAP procjena iz uzorkovanja s odbacivanjem

**Primjer:** Procijeni $\mu = P(x=0|y=1,z=0)$, N=100 uzoraka

**Postupak:**

1. Izračunaj **vjerojatnost dokaza**:
   $$P(y=1, z=0) = P(w) \cdot P(x) \cdot P(y=1|w,x) \cdot P(z=0|x)$$
   (marginaliziraj po w i x)

2. Izračunaj **očekivani broj prihvaćenih** uzoraka:
   $$N_{acc} = N \cdot P(y=1, z=0)$$

3. Od prihvaćenih, izračunaj **koliko ima x=0**:
   $$P(x=0|y=1,z=0) = \frac{P(x=0,y=1,z=0)}{P(y=1,z=0)}$$

4. **Očekivani broj** uzoraka s x=0:
   $$m = N_{acc} \cdot P(x=0|y=1,z=0)$$

5. **MAP procjena** s Laplaceom (α=β=2):
   $$\hat{\mu}_{MAP} = \frac{m + 1}{N_{acc} + 2}$$

---

#### Brze formule za zadatke

| Što se traži      | Formula                                                                         |
| ----------------- | ------------------------------------------------------------------------------- |
| Aposteriorna      | $P(x_q\|x_o) = \frac{\sum_{x_n} P(x_q,x_o,x_n)}{\sum_{x_n,x_q} P(x_q,x_o,x_n)}$ |
| MAP iz podataka   | $\hat{\mu} = \frac{N_{uspjeh} + 1}{N_{total} + K}$                              |
| Odbačeni uzorci   | $N_{rej} = N \cdot (1 - P(x_o))$                                                |
| MAP upit          | $x^* = \arg\max_x \sum_{x_n} P(x,x_o,x_n)$                                      |
| Omjer objašnjenja | $\frac{p_1}{p_2}$ = najvjerojatnija / druga najvjerojatnija                     |

---

#### Česte greške u zadacima

⚠️ **Zaborav marginalizacije:** Uvijek marginaliziraj po SVIM neopaženim varijablama koje nisu u upitu!

⚠️ **Krivi K u Laplaceu:**

- Binarna varijabla: K=2
- Ternarna varijabla: K=3

⚠️ **Odbacivanje vs prihvaćanje:**

- Prihvaćeni = $N \cdot P(x_o)$
- Odbačeni = $N \cdot (1 - P(x_o))$

⚠️ **MAP upit vs aposteriorna:**

- Aposteriorna: vraća **distribuciju**
- MAP: vraća **najvjerojatniju vrijednost**

---

## Cjelina 19: Grupiranje (Clustering)

> ✅ **Ova cjelina JE u labosu!** - K-means, elbow, silhouette, Rand index

---

### Nenadzirano učenje - pregled

**Nenadzirano učenje:** Nemamo oznake y, samo primjere $D = \{x^{(i)}\}_{i=1}^{N}$

**Četiri osnovna zadatka:**

1. **Grupiranje (clustering)** - nalaženje grupa sličnih primjera
2. **Procjena gustoće** - nalaženje $p(x)$ koja opisuje distribuciju podataka
3. **Otkrivanje outliera** - nalaženje primjera koji odskaču
4. **Smanjenje dimenzionalnosti** - PCA, t-SNE, itd.

---

### Vrste grupiranja

| Kriterij       | Vrsta         | Opis                                                  |
| -------------- | ------------- | ----------------------------------------------------- |
| **Struktura**  | Particijsko   | Plosnate grupe (bez podgrupa)                         |
|                | Hijerarhijsko | Grupe imaju podgrupe (dendrogram)                     |
| **Pripadnost** | Tvrdo (hard)  | Primjer pripada SAMO jednoj grupi                     |
|                | Meko (soft)   | Primjer može pripadati više grupa (s vjerojatnostima) |

---

### Algoritam K-sredina (K-means)

**Najjednostavniji i najpoznatiji algoritam grupiranja!**

#### Kriterijska funkcija

$$J = \sum_{k=1}^{K} \sum_{i=1}^{N} b_k^{(i)} \|x^{(i)} - \mu_k\|^2$$

gdje je:

- $\mu_k$ = centroid (središte) grupe k
- $b_k^{(i)} \in \{0,1\}$ = indikator pripadnosti (1 ako $x^{(i)}$ pripada grupi k)
- $\|x - \mu\|^2$ = kvadrat euklidske udaljenosti

#### Algoritam

```
1. Inicijaliziraj centroide μ₁, ..., μₖ (npr. slučajno)
2. Ponavljaj:
   a) Pridijeli svaki primjer najbližoj grupi:
      b_k^(i) = 1 ako k = argmin_j ||x^(i) - μ_j||
   b) Ažuriraj centroide:
      μ_k = Σᵢ b_k^(i) x^(i) / Σᵢ b_k^(i)
3. Dok μ_k ne konvergiraju
```

#### Svojstva algoritma

| Svojstvo             | Vrijednost                                         |
| -------------------- | -------------------------------------------------- |
| **Složenost**        | $O(T \cdot n \cdot N \cdot K)$ - linearno u svemu! |
| **Deterministički?** | Ne (ovisi o početnim centroidima)                  |
| **Konvergira?**      | Da (konačan broj konfiguracija, J monotono pada)   |
| **Optimalan?**       | Ne - nalazi **lokalni** optimum!                   |

#### Odabir početnih centroida

| Metoda                 | Opis                                        | Problem                   |
| ---------------------- | ------------------------------------------- | ------------------------- |
| Nasumični primjeri     | Odaberi K primjera                          | Outlieri, lokalni optimum |
| Perturbacija centroida | $\mu + \epsilon$                            | Lokalni optimum           |
| PCA inicijalizacija    | Podjeli prvu glavnu komponentu              | Lokalni optimum           |
| **k-means++** ⭐       | Svaki novi centroid što dalje od postojećih | **Najbolja metoda!**      |

**k-means++ formula:**
$$P(\mu_{k+1} = x^{(i)}) = \frac{\min_j \|\mu_j - x^{(i)}\|^2}{\sum_l \min_j \|\mu_j - x^{(l)}\|^2}$$

> 📌 **Praksa:** Pokreni K-means više puta, uzmi rezultat s najmanjim J!

---

### Algoritam K-medoida (PAM)

**Generalizacija K-means za ne-vektorske podatke!**

**Kada koristiti:**

- Primjeri NISU vektori (npr. tekst, grafovi)
- Imamo samo matricu sličnosti/različitosti

**Razlika od K-means:**

- **Medoid** = reprezentativni primjer iz D (mora biti stvarni primjer!)
- **Centroid** = srednja vrijednost (može biti "virtualni" primjer)

**Kriterijska funkcija:**
$$\tilde{J} = \sum_{i=1}^{N} \sum_{k=1}^{K} b_k^{(i)} \nu(x^{(i)}, \mu_k)$$

gdje je $\nu(x, x')$ mjera različitosti (ne mora biti metrika!)

**Složenost:** $O(T \cdot K \cdot (N-K)^2)$ - **kvadratna u N!**

---

### Provjera grupa (Cluster Validation)

**Glavni problem:** Kako odabrati optimalan broj grupa K?

> ⚠️ **PAZI:** Minimizacija J **NIJE** opcija! J monotono pada s K (minimum za K=N)

#### 1. Metoda koljena (Elbow Method) ⭐

**Postupak:**

1. Za K = 1, 2, ..., K_max izračunaj J
2. Nacrtaj graf J(K)
3. Pronađi "koljeno" - točku gdje J naglo pada pa stagnira

```
J
|\.
|  \.
|    \______ ← koljeno ovdje (npr. K=3)
|           \____
|__________________ K
```

**Interpretacija:** Koljeno označava "prirodno" grupiranje - dodavanje grupa više ne donosi značajno poboljšanje.

#### 2. Analiza siluete (Silhouette Analysis) ⭐

**Vrijednost siluete za primjer $x^{(i)}$:**

$$s^{(i)} = \frac{b^{(i)} - a^{(i)}}{\max(a^{(i)}, b^{(i)})}$$

gdje je:

- $a^{(i)}$ = prosječna udaljenost do primjera **iz iste grupe**
- $b^{(i)}$ = prosječna udaljenost do primjera **iz najbliže susjedne grupe**

**Interpretacija:**
| $s^{(i)}$ | Značenje |
|-----------|----------|
| ≈ 1 | Primjer je dobro grupiran (daleko od susjedne grupe) |
| ≈ 0 | Primjer je na granici između grupa |
| < 0 | Primjer je **pogrešno grupiran**! |

**Kriterij za dobar K:**

- Sve grupe imaju siluete > prosječna silueta
- Siluete su ujednačene veličine (slične veličine grupa)

#### 3. Randov indeks ⭐

**Svrha:** Usporedba dobivenog grupiranja s referentnim (točnim) grupiranjem

**Formula:**
$$R = \frac{a + b}{\binom{N}{2}}$$

gdje je:

- $a$ = broj parova **ispravno u istoj grupi** (TP)
- $b$ = broj parova **ispravno razdvojenih** (TN)
- $\binom{N}{2}$ = ukupan broj parova

**Interpretacija:** Randov indeks = **točnost na razini parova primjera**

> 📌 **Randov indeks je unimodalna funkcija K** - ima maksimum za optimalan K!

---

#### Pretpostavke K-means algoritma

**K-means dobro radi kada:**

1. Grupe su **kuglaste** (sferne)
2. Grupe su **podjednake veličine**
3. Grupe su **podjednake gustoće**

**K-means NE radi dobro za:**

- Koncentrične krugove (koristiti spektralno grupiranje)
- Grupe različitih veličina (manje grupe se "gutaju")
- Grupe s outlierima (outlieri postaju zasebne grupe)

---

### 🎯 Moguća ispitna pitanja (Cjelina 19)

**Q1: Zašto ne možemo odabrati K minimizacijom J?**

> **A:** Jer J monotono pada s K i doseže minimum (J=0) za K=N. Takvo "grupiranje" je beskorisno.

**Q2: Zašto K-means može zaglaviti u lokalnom optimumu?**

> **A:** Jer je algoritam **pohlepan** - u svakom koraku samo smanjuje J, nikad ne prihvaća lošije rješenje. Rezultat ovisi o početnim centroidima.

**Q3: Koja je razlika između centroida i medoida?**

> **A:** **Centroid** je srednja vrijednost vektora u grupi (može biti "virtualni" primjer). **Medoid** mora biti stvarni primjer iz skupa podataka.

**Q4: Što Randov indeks zapravo mjeri?**

> **A:** Točnost grupiranja na razini **parova primjera**. Mjeri koliko se dobiveno grupiranje podudara s referentnim (TP + TN) / ukupno parova.

**Q5: Kada bismo koristili K-medoide umjesto K-means?**

> **A:** Kada primjeri nisu vektori ili kada nemamo euklidsku udaljenost, nego samo matricu sličnosti/različitosti (npr. tekstovi, slike, grafovi).

**Q6: Što znači negativna vrijednost siluete?**

> **A:** Primjer je **pogrešno grupiran** - bliži je primjerima iz druge grupe nego primjerima iz svoje grupe.

---

### 📋 Teorijska pitanja s ispita (Cjelina 19)

**1. (T) Algoritam K-sredina je iterativan algoritam za nalaženje parametara $b_k^{(i)}$ i $\mu_k$ koji minimiziraju kriterijsku funkciju J. Algoritam funkciju J optimizira iterativno, jer rješenje u zatvorenoj formi ne postoji. Zbog čega za problem minimizacije funkcije J ne postoji rješenje u zatvorenoj formi?**

| Odgovor | Tekst                                                                                             |
| ------- | ------------------------------------------------------------------------------------------------- |
| A       | Jer za $b_k^{(i)}$ mora vrijediti ograničenje $\sum_k b_k^{(i)} = 1$ i $b_k^{(i)} \geq 0$         |
| B       | Jer J ovisi o K i inicijalnom odabiru za $\mu_k$, pa rješenje nije jedinstveno                    |
| **✓ C** | **Jer $b_k^{(i)}$ ovisi o vektorima $\mu_k$, a vektor $\mu_k$ ovisi o vrijednostima $b_k^{(i)}$** |
| D       | Jer $b_k^{(i)}$ ovisi o N, broj vektora $\mu_k$ ovisi o K, a K je odozgo ograničen sa N           |

> 📌 **Objašnjenje:** Parametri su **međusobno ovisni**:
>
> - $b_k^{(i)}$ ovisi o $\mu_k$ → primjer ide u grupu s najbližim centroidom
> - $\mu_k$ ovisi o $b_k^{(i)}$ → centroid je srednja vrijednost primjera u grupi
>
> Zato algoritam **alternira** između dva koraka dok ne konvergira!

---

**2. (T) Konvergencija je poželjno svojstvo algoritma grupiranja. Je li točno da algoritam k-sredina uvijek konvergira?**

| Odgovor | Tekst                                                                                                                                                                            |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **✓ A** | **Da, algoritam uvijek konvergira zato što je broj particija N primjera u K skupova ograničen, a optimizacijski postupak definiran je tako da se J u svakoj iteraciji smanjuje** |
| B       | Algoritam konvergira samo ako su početna središta dobro odabrana, inače se može dogoditi da algoritam oscilira između dva rješenja                                               |
| C       | Kako se radi o algoritmu koji grupira primjere u vektorskom prostoru, broj rješenja je neograničen, stoga algoritam ne mora konvergirati                                         |
| D       | Algoritam uvijek konvergira zato što je broj primjera N uvijek veći ili jednak broju grupa K, a kao mjera udaljenosti koristi se euklidska udaljenost, koja je nužno nenegativna |

> 📌 **Objašnjenje:** Algoritam **UVIJEK konvergira** jer:
>
> 1. Broj konfiguracija je **konačan** ($K^N$ particija)
> 2. J se **monotono smanjuje** u svakoj iteraciji
> 3. Algoritam **nikad ne posjećuje istu konfiguraciju dva puta**
>
> ⚠️ Ali to NE znači da nalazi globalni optimum - samo lokalni!

---

**3. (T) Algoritam K-means++ proširenje je algoritma K-sredina heurističkim odabirom početnih središta grupa. Koja je glavna ideja odabira početnih središta grupa kod algoritma K-means++?**

| Odgovor | Tekst                                                                                                                                                 |
| ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| A       | Vjerojatnost da je neki primjer središte grupe proporcionalna je s brojem primjera u toj grupi i udaljenosti tih primjera od centroida skupa podataka |
| B       | Središta grupe su srednje vrijednosti grupa projiciranih na pravac u smjeru prve komponente rastava skupa podataka na glavne komponente (PCA)         |
| C       | Središta grupa su mjesta na kojima graf kriterijske funkcije u ovisnosti o broju grupa naglo opada pa stagnira                                        |
| **✓ D** | **Najvjerojatnije središte grupe jest primjer koji je najviše udaljen od njemu najbližeg središta**                                                   |

> 📌 **Objašnjenje:** K-means++ bira svaki novi centroid tako da je vjerojatnost izbora **proporcionalna kvadratu udaljenosti** od najbližeg već odabranog centroida:
> $$P(\mu_{k+1} = x^{(i)}) \propto \min_j \|\mu_j - x^{(i)}\|^2$$
>
> Primjeri **daleko od postojećih centroida** imaju veću vjerojatnost da budu odabrani → bolje inicijalno "pokrivanje" prostora!

---

**4. (T) Algoritmi grupiranja k-sredina i k-medoida razlikuju se, između ostaloga, i po vremenskoj računalnoj složenosti. Naime, algoritam k-medoida računalno je složeniji od algoritma k-sredina. Zašto je algoritam k-medoida računalno složeniji od algoritma k-sredina?**

| Odgovor | Tekst                                                                                                                                                                                                                 |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A       | Za razliku od algoritma k-sredina koji se zasniva na euklidskoj udaljenosti, čiji je izračun računalno nezahtjevan, algoritam k-medoida koristi funkcije sličnosti čije računanje iziskuje mnogo računalnih operacija |
| **✓ B** | **Budući da algoritam k-medoida ne koristi centroide, nego medoide, na kraju svake iteracije mora kombinatoričkom provjerom po primjerima pronaći medoide koji minimiziraju kriterijsku funkciju J**                  |
| C       | Za razliku od algoritma k-sredina, algoritam k-medoida je algoritam mekog grupiranja, što iziskuje provođenje dodatnih koraka unutar algoritma                                                                        |
| D       | Kriterijska funkcija algoritma k-medoida jest mnogo složenija od one k-sredina, upravo zato što algoritam k-medoide koristi medoide, a ne centroide                                                                   |

> 📌 **Objašnjenje:** Složenost:
>
> - **K-sredina:** $O(T \cdot n \cdot N \cdot K)$ - **linearno** u N
> - **K-medoida:** $O(T \cdot K \cdot (N-K)^2)$ - **kvadratno** u N
>
> K-medoidi mora **isprobati sve primjere** kao kandidate za novi medoid i za svakog izračunati J!

---

**5. (T) Algoritam K-medoida općenitiji je od algoritma K-sredina budući da se može koristiti za primjere koji nisu prikazani kao vektori. Međutim, razmotrite slučaj kada primjeri jesu prikazani kao vektori, ali ih želimo grupirati na temelju mjere udaljenosti koja nije euklidska. Koji bismo algoritam koristili u tom slučaju i zašto?**

| Odgovor | Tekst                                                                                               |
| ------- | --------------------------------------------------------------------------------------------------- |
| **✓ A** | **Algoritam K-medoida, jer kriterijska funkcija algoritma K-sredina koristi euklidsku udaljenost**  |
| B       | Algoritam K-sredina, jer za vektorizirane primjere možemo izračunati centroide grupa                |
| C       | Algoritam K-medoida, jer vektorizirani primjeri također mogu biti medoidi                           |
| D       | Algoritam K-sredina, jer koristi mjeru udaljenosti, dok algoritam K-medoida koristi mjeru sličnosti |

> 📌 **Objašnjenje:**
>
> - **K-sredina:** zahtijeva **euklidsku udaljenost** jer računa centroid kao srednju vrijednost vektora
> - **K-medoida:** može raditi s **bilo kojom mjerom različitosti** ν (ne mora biti metrika!)
>
> Ako želimo npr. Manhattan udaljenost ili kosinusnu sličnost → K-medoida!

---

**6. (T) Algoritam K-medoida proširenje je algoritma K-sredina na neeuklidske ulazne prostore. Kod algoritma K-medoida kao funkciju različitosti ν možemo u načelu koristiti bilo koju funkciju. Specifično, ako je ulazni prostor vektorski, možemo koristiti euklidsku udaljenost. Što bi se dogodilo da kao funkciju različitosti koristimo euklidsku udaljenost?**

| Odgovor | Tekst                                                                                                                 |
| ------- | --------------------------------------------------------------------------------------------------------------------- |
| A       | Algoritam bi bio davao grupe koje bi u prosjeku bile više izdužene nego one dobivene algoritmom K-sredina             |
| B       | Algoritam K-medoida davao bi isto grupiranje kao i algoritam K-sredina, ali s većom vremenskom složenošću             |
| C       | Algoritam bi uz veću prostornu složenost davao grupiranje u manji broj grupa nego algoritam K-sredina                 |
| **✓ D** | **Algoritam bi primjere grupirao slično kao i algoritam K-sredina, pogotovo ako u središtima grupa postoje primjeri** |

> 📌 **Objašnjenje:** Ako koristimo euklidsku udaljenost:
>
> - K-medoidi daje **slično grupiranje** kao K-means
> - Razlika: **medoid mora biti stvarni primjer**, centroid može biti "virtualan"
> - Ako je centroid blizu nekog primjera → rezultati gotovo identični
> - Ali K-medoidi je **sporiji** (kvadratna složenost)!
>
> ⚠️ Odgovor B je **zamka** - grupiranje nije ISTO, samo SLIČNO!

---

### 🧮 Napomene za problemske zadatke (Cjelina 19)

#### Zadatak tip 1: K-means - izračun J nakon iteracije

**Primjer:** D = {(1,1), (1,2), (2,2), (2,3), (3,3)}, K=2, početni centroidi $\mu_1$=(1,2), $\mu_2$=(3,3)

**Postupak:**

1. **Korak pridjeljivanja** - za svaki primjer nađi najbliži centroid:
   - $(1,1)$: $d(\mu_1)=1$, $d(\mu_2)=\sqrt{8}$ → grupa 1
   - $(1,2)$: $d(\mu_1)=0$, $d(\mu_2)=\sqrt{5}$ → grupa 1
   - $(2,2)$: $d(\mu_1)=1$, $d(\mu_2)=\sqrt{2}$ → grupa 1
   - $(2,3)$: $d(\mu_1)=\sqrt{2}$, $d(\mu_2)=1$ → grupa 2
   - $(3,3)$: $d(\mu_1)=\sqrt{5}$, $d(\mu_2)=0$ → grupa 2

2. **Korak ažuriranja** - izračunaj nove centroide:
   - $\mu_1' = \frac{(1,1)+(1,2)+(2,2)}{3} = (\frac{4}{3}, \frac{5}{3})$
   - $\mu_2' = \frac{(2,3)+(3,3)}{2} = (2.5, 3)$

3. **Izračunaj J:**
   $$J = \sum_i \|x^{(i)} - \mu_{k(i)}\|^2$$

---

#### Zadatak tip 2: Globalni vs lokalni minimum

**Postupak:**

1. **Pronađi globalni minimum** $J^*$:
   - Isprobaj sve "razumne" kombinacije centroida
   - Za K=3 s 5 primjera, grupe su npr. {1}, {2,3}, {4,5}

2. **Pronađi lokalni minimum** $J^+$:
   - Pokreni algoritam s nasumiče odabranim centroidima
   - Algoritam konvergira u lokalni (ne nužno globalni) optimum

3. **Razlika:** $J^+ - J^*$

> ⚠️ **Trik:** Globalni minimum često ima intuitivno "prirodne" grupe!

---

#### Zadatak tip 3: Usporedba prostora stanja

**Prostor stanja K-means:**

- Broj mogućih particija: $K^N$ (ali ne sve su dostižne!)
- S nasumičnom init.: može posjetiti više stanja
- S k-means++: manje stanja (bolja inicijalizacija)

**Računanje |S(A)|:**

- Prebroji koliko različitih grupiranja algoritam može dati
- Ovisi o početnim centroidima

---

#### Zadatak tip 4: K-medoidi (PAM) - jedna iteracija

**Primjer:** Matrica različitosti dana, početni medoidi $x^{(1)}$ i $x^{(5)}$

**Postupak:**

1. **Pridijeli primjere** najbližem medoidu (po matrici ν)

2. **Za svaki medoid**, isprobaj sve ne-medoide kao zamjenu:
   - Izračunaj $\tilde{J}$ za svaku zamjenu
   - Odaberi zamjenu koja najviše smanjuje $\tilde{J}$

3. **Novi medoidi** su oni koji daju najmanji $\tilde{J}$

**Primjer izračuna:**

- Grupa 1: {$x^{(1)}, x^{(2)}, x^{(3)}$}, medoid $x^{(1)}$
- $\tilde{J}_1 = \nu(x^{(2)}, x^{(1)}) + \nu(x^{(3)}, x^{(1)})$
- Isprobaj $x^{(2)}$ kao medoid: $\tilde{J}_1' = \nu(x^{(1)}, x^{(2)}) + \nu(x^{(3)}, x^{(2)})$
- Ako $\tilde{J}_1' < \tilde{J}_1$, zamijeni medoid!

---

#### Zadatak tip 5: Randov indeks - ručni izračun

**Primjer:** 10 primjera, $y_{pred}$ i $y_{true}$ dani

**Postupak:**

1. **Prebroji parove** - ukupno $\binom{10}{2} = 45$ parova

2. **Za svaki par** (i,j) odredi:
   - Jesu li u **istoj grupi** po $y_{pred}$?
   - Jesu li u **istoj grupi** po $y_{true}$?

3. **Prebroji:**
   - $a$ = parovi koji su u istoj grupi I po pred I po true (TP)
   - $b$ = parovi koji su u različitim grupama I po pred I po true (TN)

4. **Randov indeks:**
   $$R = \frac{a + b}{\binom{N}{2}}$$

**Brzi trik:** Napravi tablicu 2x2:

|                      | Ista grupa (pred) | Različite (pred) |
| -------------------- | ----------------- | ---------------- |
| **Ista (true)**      | a (TP)            | c (FN)           |
| **Različite (true)** | d (FP)            | b (TN)           |

$R = \frac{a + b}{a + b + c + d}$

---

#### Zadatak tip 6-7: Randov indeks za različite K

**Postupak:**

1. Za svaki K izračunaj Randov indeks R(K)
2. Optimalan $K^* = \arg\max_K R(K)$
3. Razlika: $R(K_1) - R(K_2)$

**Primjer:** Oznake za K=3: {1,2,4,8}, {2,3,7}, {4,5,3,5,6,6,7,8}

1. Prebrojaj parove u svakoj grupi:
   - Grupa 1: $\binom{4}{2} = 6$ parova
   - Grupa 2: $\binom{3}{2} = 3$ para
   - Grupa 3: $\binom{8}{2} = 28$ parova

2. Usporedi s referentnim grupiranjem...

---

#### Brze formule za Randov indeks

| Što                            | Formula                            |
| ------------------------------ | ---------------------------------- |
| Ukupno parova                  | $\binom{N}{2} = \frac{N(N-1)}{2}$  |
| Parovi unutar grupe veličine n | $\binom{n}{2} = \frac{n(n-1)}{2}$  |
| Randov indeks                  | $R = \frac{TP + TN}{\binom{N}{2}}$ |

---

#### Česte greške u zadacima

⚠️ **K-means J:** Ne zaboravi da je J **suma kvadrata**, ne suma udaljenosti!

⚠️ **K-medoidi:** Medoid mora biti **stvarni primjer** iz D!

⚠️ **Randov indeks:** Parovi koji su u **različitim** grupama i trebaju biti u različitim su **TN** (ne TP)!

⚠️ **Matrica različitosti:** Često je **simetrična** i ima **0 na dijagonali** - ne prepisuj dvaput!

---

## Cjelina 20: Grupiranje II

> **🔬 LABOS:** Ova cjelina se ispituje u zadatku 7 laboratorijske vježbe! (GMM, usporedba s K-means)

### Meko vs tvrdo grupiranje

| Vrsta     | Opis                                          | Algoritmi               |
| --------- | --------------------------------------------- | ----------------------- |
| **Tvrdo** | Primjer pripada **jednoj** grupi              | K-means, K-medoids, HAC |
| **Meko**  | Primjer pripada grupama s **vjerojatnostima** | GMM                     |

**Kada koristiti meko grupiranje:**

1. **Preklapanje grupa** - primjeri mogu legitimno pripadati u više grupa (npr. osoba s više crta ličnosti)
2. **Neizvjesnost** - ne znamo kojoj grupi primjer pripada, pa modeliramo vjerojatnost

---

### 1. Model Gaussove mješavine (GMM)

#### Osnovna ideja

GMM modelira gustoću $p(x)$ kao **linearnu kombinaciju K Gaussovih komponenti**:

$$p(x) = \sum_{k=1}^{K} \pi_k \cdot \mathcal{N}(x|\mu_k, \Sigma_k)$$

Gdje je:

- $\pi_k$ = **koeficijent mješavine** (apriorna vjerojatnost grupe k)
- $\mu_k$ = srednji vektor k-te komponente
- $\Sigma_k$ = kovarijacijska matrica k-te komponente

> ⚠️ **KLJUČNO:** $\sum_{k=1}^{K} \pi_k = 1$ (koeficijenti su vjerojatnosti!)

#### Generativna priča GMM-a

1. **Odaberi grupu** $k$ po kategoričkoj distribuciji s vjerojatnostima $\pi_1, ..., \pi_K$
2. **Generiraj primjer** $x$ iz Gaussove distribucije $\mathcal{N}(\mu_k, \Sigma_k)$

#### Odgovornost (ono što nas zanima!)

Za svaki primjer želimo znati **vjerojatnost da pripada grupi k**:

$$h_k^{(i)} = P(y=k|x^{(i)}) = \frac{\pi_k \cdot p(x^{(i)}|\mu_k, \Sigma_k)}{\sum_{j=1}^{K} \pi_j \cdot p(x^{(i)}|\mu_j, \Sigma_j)}$$

> **Bayesovo pravilo!** Odgovornost $h_k^{(i)}$ je aposteriorna vjerojatnost grupe za primjer.

---

### 2. GMM vs K-means - ključne razlike

| Aspekt               | K-means                          | GMM                                                             |
| -------------------- | -------------------------------- | --------------------------------------------------------------- |
| **Pripadnost grupi** | Binarna: $b_k^{(i)} \in \{0,1\}$ | Vjerojatnosna: $h_k^{(i)} \in [0,1]$                            |
| **Parametri grupe**  | Samo centroid $\mu_k$            | Centroid $\mu_k$ + kovarijanca $\Sigma_k$ + udio $\pi_k$        |
| **Oblik grupa**      | Sferični (kružnice)              | Elipsoidni (proizvoljni)                                        |
| **Centroidi**        | Prosjek primjera                 | Težinski prosjek (po odgovornosti)                              |
| **Poseban slučaj**   | -                                | GMM s $\Sigma = \sigma^2 I$ i $h_k^{(i)} \to \{0,1\}$ = K-means |

> ⚠️ **VAŽNO ZA ISPIT:** K-means je **specijalni slučaj GMM-a** s izotropnom kovarijancom i tvrdim grupiranjem!

---

### 3. Problem: Log-izglednost GMM-a

**Nepotpuna log-izglednost** (ono što želimo maksimizirati):

$$\ln L(\theta|D) = \sum_{i=1}^{N} \ln \sum_{k=1}^{K} \pi_k \cdot p(x^{(i)}|\mu_k, \Sigma_k)$$

**Problem:** Logaritam je "zapeo" između suma → **NEMA zatvorene forme!**

---

### 4. EM algoritam (Expectation-Maximization)

#### Latentne varijable

Uvodimo **latentnu varijablu** $z^{(i)}$ za svaki primjer - govori kojoj grupi primjer pripada (one-hot encoding):

$$z^{(i)} = (z_1^{(i)}, ..., z_K^{(i)}), \quad z_k^{(i)} \in \{0,1\}, \quad \sum_k z_k^{(i)} = 1$$

**Potpuna log-izglednost** (s latentnim varijablama):

$$\ln L(\theta|D,Z) = \sum_{i=1}^{N} \sum_{k=1}^{K} z_k^{(i)} \left( \ln \pi_k + \ln p(x^{(i)}|\theta_k) \right)$$

> ✅ **Sada se faktorizira po komponentama!** Ali ne znamo $z_k^{(i)}$...

#### Ideja EM algoritma

**Iterativno:**

1. **E-korak:** Izračunaj **očekivanje** potpune log-izglednosti (koristeći trenutne parametre)
2. **M-korak:** **Maksimizirati** to očekivanje po parametrima

#### E-korak (Expectation)

Izračunaj odgovornosti (očekivanje latentnih varijabli):

$$h_k^{(i)} = E[z_k^{(i)}|x^{(i)}, \theta^{(t)}] = \frac{\pi_k \cdot p(x^{(i)}|\mu_k, \Sigma_k)}{\sum_{j=1}^{K} \pi_j \cdot p(x^{(i)}|\mu_j, \Sigma_j)}$$

> **Zašto?** $z_k^{(i)}$ je Bernoullijeva varijabla, pa je $E[z_k^{(i)}] = P(z_k^{(i)} = 1)$

#### M-korak (Maximization)

Ažuriraj parametre tako da maksimiziraju očekivanje log-izglednosti:

$$\mu_k^{(t+1)} = \frac{\sum_i h_k^{(i)} \cdot x^{(i)}}{\sum_i h_k^{(i)}}$$

$$\Sigma_k^{(t+1)} = \frac{\sum_i h_k^{(i)} \cdot (x^{(i)} - \mu_k^{(t+1)})(x^{(i)} - \mu_k^{(t+1)})^T}{\sum_i h_k^{(i)}}$$

$$\pi_k^{(t+1)} = \frac{1}{N} \sum_{i=1}^{N} h_k^{(i)}$$

---

### 5. Algoritam GMM (kompletno)

```
Algoritam GMM (model GMM + EM-algoritam)
────────────────────────────────────────
1. Inicijaliziraj parametre θ = {πₖ, μₖ, Σₖ} za k = 1,...,K

2. Ponavljaj do konvergencije:

   E-korak:
   Za svaki primjer x⁽ⁱ⁾ i svaku komponentu k:
   h_k^(i) ← πₖ·p(x⁽ⁱ⁾|μₖ,Σₖ) / Σⱼ πⱼ·p(x⁽ⁱ⁾|μⱼ,Σⱼ)

   M-korak:
   Za svaku komponentu k:
   μₖ ← Σᵢ hₖ⁽ⁱ⁾x⁽ⁱ⁾ / Σᵢ hₖ⁽ⁱ⁾
   Σₖ ← Σᵢ hₖ⁽ⁱ⁾(x⁽ⁱ⁾-μₖ)(x⁽ⁱ⁾-μₖ)ᵀ / Σᵢ hₖ⁽ⁱ⁾
   πₖ ← (1/N) Σᵢ hₖ⁽ⁱ⁾

   Izračunaj log-izglednost:
   ln L = Σᵢ ln Σₖ πₖ·p(x⁽ⁱ⁾|μₖ,Σₖ)

3. Zaustavi kad log-izglednost konvergira
```

---

### 6. Tipovi kovarijacijskih matrica

| Tip             | Opis                                                          | Broj param.                | Oblik                    |
| --------------- | ------------------------------------------------------------- | -------------------------- | ------------------------ |
| **Puna**        | Svaka $\Sigma_k$ različita, puna matrica                      | $K \cdot \frac{n(n+1)}{2}$ | Proizvoljne elipse       |
| **Dijeljena**   | Sve $\Sigma_k = \Sigma$ jednake                               | $\frac{n(n+1)}{2}$         | Jednako poravnate elipse |
| **Dijagonalna** | $\Sigma_k = \text{diag}(\sigma_{k,1}^2, ..., \sigma_{k,n}^2)$ | $K \cdot n$                | Elipse uz osi            |
| **Izotropna**   | $\Sigma_k = \sigma_k^2 I$                                     | $K$                        | Krugovi/sfere            |

> ⚠️ **Odabir:** Jednostavniji modeli → manje parametara → manja prenaučenost, ali manja izražajnost!

**Odabir broja grupa K:**

- AIC: $K^* = \arg\min_K \left( -2 \ln L(K) + 2q(K) \right)$, gdje je $q(K)$ broj parametara
- BIC (Bayesian IC): $K^* = \arg\min_K \left( -2 \ln L(K) + q(K) \ln N \right)$

---

### 7. Napomene za GMM

| Napomena             | Detalj                                                          |
| -------------------- | --------------------------------------------------------------- |
| **Konvergencija**    | EM nužno konvergira, ali možda u **lokalni** optimum            |
| **Inicijalizacija**  | Rezultat ovisi o početnim parametrima; koristi K-means za init. |
| **Sporo**            | GMM konvergira sporije od K-means                               |
| **Ograničenja na Σ** | Dijagonalna/izotropna → jednostavniji model, brže               |

---

### 8. Hijerarhijsko aglomerativno grupiranje (HAC)

#### Dendrogram

**Dendrogram** = stablasti prikaz hijerarhije grupa:

- **Listovi** = pojedinačni primjeri (svaki u svojoj grupi)
- **Grane** = spajanje grupa
- **Korijen** = svi primjeri u jednoj grupi
- **Visina grana** = udaljenost na kojoj se grupe spajaju

#### Aglomerativno vs Divizivno

| Pristup           | Smjer              | Opis                                     |
| ----------------- | ------------------ | ---------------------------------------- |
| **Aglomerativno** | Odozdo prema gore  | Spaja najbliže grupe dok ne ostane jedna |
| **Divizivno**     | Odozgo prema dolje | Dijeli veliku grupu na podgrupe          |

---

### 9. Metode povezivanja (Linkage)

Kako računamo udaljenost između **grupa** (ne samo primjera)?

| Metoda                   | Formula                                                     | Opis                  |
| ------------------------ | ----------------------------------------------------------- | --------------------- | --- | --- | ---------------------------------------------- | -------------------- |
| **Jednostruka** (single) | $d_{min}(G_i, G_j) = \min_{x \in G_i, x' \in G_j} d(x, x')$ | Minimalna udaljenost  |
| **Potpuna** (complete)   | $d_{max}(G_i, G_j) = \max_{x \in G_i, x' \in G_j} d(x, x')$ | Maksimalna udaljenost |
| **Prosječna** (average)  | $d\_{avg}(G_i, G_j) = \frac{1}{                             | G_i                   |     | G_j | } \sum*{x \in G_i} \sum*{x' \in G_j} d(x, x')$ | Prosječna udaljenost |
| **Centroida**            | $d_{cent}(G_i, G_j) = \|\bar{x}_i - \bar{x}_j\|$            | Udaljenost centroida  |
| **Wardova**              | Povećanje varijance nakon spajanja                          | Minimalna varijanca   |

#### Karakteristike

| Metoda          | Oblik grupa        | Osjetljivost na šum |
| --------------- | ------------------ | ------------------- |
| **Jednostruka** | Dugački, ulančani  | Visoka              |
| **Potpuna**     | Kompaktni, zbijeni | Visoka              |
| **Prosječna**   | Kompromis          | Srednja             |
| **Wardova**     | Kompaktni          | Niska               |

---

### 10. Algoritam HAC

```
Algoritam HAC
─────────────
1. Inicijaliziraj: k ← N, Gᵢ ← {x⁽ⁱ⁾} za i = 1,...,N

2. Ponavljaj dok k > K:
   a) k ← k - 1
   b) (Gᵢ, Gⱼ) ← argmin d(Gₐ, Gᵦ)  // nađi najbliže grupe
   c) Gᵢ ← Gᵢ ∪ Gⱼ                  // spoji ih

3. Rezultat: K grupa (ili dendrogram za K=1)
```

#### Složenost

| Složenost                             | Vrijednost      | Napomena            |
| ------------------------------------- | --------------- | ------------------- |
| **Prostorna**                         | $O(N^2)$        | Matrica udaljenosti |
| **Vremenska** (naivno)                | $O(N^3)$        | -                   |
| **Vremenska** (s prioritetnom listom) | $O(N^2 \log N)$ | -                   |
| **Vremenska** (single linkage)        | $O(N^2)$        | -                   |

> ⚠️ **Problem:** Kvadratna prostorna složenost može biti problem za velike skupove!

---

### 11. Presijecanje dendrograma

Iz dendrograma možemo dobiti **particijsko grupiranje** presijecanjem na:

1. **Određenoj udaljenosti** → dobijemo određeni broj grupa
2. **Određenom broju grupa K** → nađemo odgovarajuću visinu

---

### 12. GMM vs GBC (Gaussov Bayesov klasifikator)

| Aspekt          | GMM                        | GBC                               |
| --------------- | -------------------------- | --------------------------------- |
| **Tip učenja**  | **Nenadzirano**            | Nadzirano                         |
| **Oznake**      | Nisu dostupne (latentne)   | Dostupne u trening skupu          |
| **Procjena**    | EM algoritam (iterativno)  | MLE (zatvorena forma)             |
| **Odgovornost** | $h_k^{(i)}$ - vjerojatnost | $b_k^{(i)} \in \{0,1\}$ - poznato |

> **Ključna razlika:** Kod GBC **znamo** kojoj klasi primjer pripada, kod GMM **ne znamo** pa moramo koristiti EM!

---

### 📋 Praktične formule za numeričke zadatke

#### GMM - E-korak (izračun odgovornosti)

Za jednodimenzijski slučaj s K=2:

$$h_1^{(i)} = \frac{\pi_1 \cdot \mathcal{N}(x^{(i)}|\mu_1, \sigma_1^2)}{\pi_1 \cdot \mathcal{N}(x^{(i)}|\mu_1, \sigma_1^2) + \pi_2 \cdot \mathcal{N}(x^{(i)}|\mu_2, \sigma_2^2)}$$

Gdje je:
$$\mathcal{N}(x|\mu, \sigma^2) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$$

#### GMM - M-korak

$$\mu_k = \frac{\sum_i h_k^{(i)} x^{(i)}}{\sum_i h_k^{(i)}}, \quad \sigma_k^2 = \frac{\sum_i h_k^{(i)} (x^{(i)} - \mu_k)^2}{\sum_i h_k^{(i)}}, \quad \pi_k = \frac{1}{N} \sum_i h_k^{(i)}$$

#### HAC - Jednostruki primjer

Za 3 primjera $x_1, x_2, x_3$ s udaljenostima $d_{12}=1, d_{13}=3, d_{23}=2$:

1. **Korak 1:** Spoji najbliže: $G_1 = \{x_1, x_2\}$ na udaljenosti 1
2. **Korak 2:** Izračunaj udaljenost $G_1$ do $x_3$:
   - Single: $d_{min} = \min(3, 2) = 2$
   - Complete: $d_{max} = \max(3, 2) = 3$
3. **Korak 3:** Spoji $G_1$ i $\{x_3\}$ na odgovarajućoj udaljenosti

---

### 📝 Teorijska ispitna pitanja (Cjelina 20)

#### Pitanje 1: Što modelira $p(x|\theta_k)$ u modelu miješane gustoće?

Model miješane gustoće: $p(x) = \sum_{k=1}^{K} \pi_k p(x|\theta_k)$

| Odgovor  | Opis                                                |
| -------- | --------------------------------------------------- |
| **✅ A** | **Gustoću vjerojatnosti primjera x unutar grupe k** |
| B        | Vjerojatnost da primjer x pripada grupi k           |
| C        | Stupanj pripadnosti primjera x grupi k              |
| D        | Gustoću vjerojatnosti grupe k za primjer x          |

> **Objašnjenje:** $p(x|\theta_k)$ je **izglednost grupe** (class likelihood) - gustoća vjerojatnosti primjera x **unutar** komponente k. To je distribucija primjera koji pripadaju grupi k. Vjerojatnost da primjer pripada grupi bila bi $P(y=k|x)$ - to je odgovornost $h_k$.

---

#### Pitanje 2: Koju distribuciju pretpostavljamo za latentnu varijablu $z^{(i)}$ i zašto?

| Odgovor  | Opis                                                                                |
| -------- | ----------------------------------------------------------------------------------- |
| A        | Beta-distribuciju koja opisuje s kojom vjerojatnošću primjer pripada svakoj grupi   |
| **✅ B** | **Kategoričku distribuciju koja opisuje kojoj grupi primjer zapravo pripada**       |
| C        | Bernoullijevu distribuciju koja opisuje s kojom vjerojatnošću primjer pripada grupi |
| D        | Gaussovu distribuciju koja opisuje vjerojatnost da je grupa generirala primjer      |

> **Objašnjenje:** $z^{(i)}$ je **one-hot** vektor koji indicira **jednu** od K grupa. To je **kategorička varijabla** s K mogućih vrijednosti. $P(z) = \prod_k \pi_k^{z_k}$ - kategorička distribucija s parametrima $\pi_1, ..., \pi_K$.

---

#### Pitanje 3: Na što se odnosi "očekivanje" u EM algoritmu?

| Odgovor  | Opis                                                                                                                                      |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| A        | Izglednost parametara uz fiksiranu pripadnost svakog primjera najbližoj grupi                                                             |
| B        | Vjerojatnost parametara s fiksiranim dodjeljivanjem primjera grupama                                                                      |
| **✅ C** | **Vjerojatnost skupa podataka pod modelom s fiksiranim parametrima izračunata na temelju vjerojatnosti pripadanja primjera svakoj grupi** |
| D        | Vjerojatnost pripadanja primjera svakoj grupi izračunata Bayesovim pravilom                                                               |

> **Objašnjenje:** "Očekivanje" se odnosi na **očekivanu potpunu log-izglednost** Q(θ|θ^t):
> $$Q(\theta|\theta^{(t)}) = E_{Z|D,\theta^{(t)}}[\ln L(\theta|D,Z)] = \sum_i \sum_k h_k^{(i)} (\ln \pi_k + \ln p(x^{(i)}|\theta_k))$$
> To je vjerojatnost podataka pod modelom, **ponderirana odgovornostima** $h_k^{(i)}$ (vjerojatnostima pripadanja).

---

#### Pitanje 4: Razlika potpune i nepotpune log-izglednosti?

| Odgovor  | Opis                                                                        |
| -------- | --------------------------------------------------------------------------- |
| A        | Potpuna = svi primjeri, nepotpuna = označeni primjeri za evaluaciju         |
| B        | Potpuna = s neopaženim varijablama (centroidi, kovarijance)                 |
| C        | Potpuna = označeni primjeri, nepotpuna = neoznačeni                         |
| **✅ D** | **Potpuna = s latentnim varijablama z; računamo očekivanje jer z ne znamo** |

> **Objašnjenje:**
>
> - **Nepotpuna:** $\ln L = \sum_i \ln \sum_k \pi_k p(x^{(i)}|\theta_k)$ - logaritam "zapeo" između suma → **nema zatvorene forme**
> - **Potpuna:** $\ln L = \sum_i \sum_k z_k^{(i)} (\ln \pi_k + \ln p(x^{(i)}|\theta_k))$ - **faktorizira se** po k!
>
> Problem: ne znamo $z_k^{(i)}$, pa računamo **očekivanje** $E[z_k^{(i)}] = h_k^{(i)}$

---

#### Pitanje 5: Pod kojim uvjetima EM-algoritam konvergira?

| Odgovor  | Opis                                                                                              |
| -------- | ------------------------------------------------------------------------------------------------- |
| A        | Uvijek konvergira do parametara koji maksimiziraju očekivanje, ali ne nužno vjerojatnost podataka |
| B        | Konvergira samo za sferične primjere bez multikolinearnosti                                       |
| **✅ C** | **Uvijek konvergira do (lokalnog) maksimuma log-izglednosti, brzina ovisi o inicijalizaciji**     |
| D        | Konvergira samo ako je broj grupa jednak pravom broju ili broju primjera                          |

> **Objašnjenje:** EM **nužno konvergira** - svaka iteracija povećava log-izglednost. Ali može konvergirati u **lokalni maksimum**, ne nužno globalni! Brzina konvergencije ovisi o **inicijalizaciji parametara**.

---

#### Pitanje 6: Uz koje uvjete GMM degenerira u K-means?

| Odgovor  | Opis                                                                                         |
| -------- | -------------------------------------------------------------------------------------------- |
| A        | Minimizira se negativna log-izglednost, početna središta K-means                             |
| B        | Koeficijenti jednaki, dijagonalne matrice                                                    |
| **✅ C** | **Dijeljena izotropna kovarijanca $\Sigma = \sigma^2 I$ + odgovornosti zaokružene na {0,1}** |
| D        | Jedinična matrica, negativna log-izglednost                                                  |

> **Objašnjenje:** GMM → K-means kad:
>
> 1. **Dijeljena izotropna kovarijanca:** $\Sigma_k = \sigma^2 I$ za sve k (sferične grupe)
> 2. **Tvrdo grupiranje:** $h_k^{(i)} \to b_k^{(i)} \in \{0, 1\}$ (zaokruživanje)
>
> Tada: $\ln L \propto -J$ (log-izglednost proporcionalna negativnoj pogrešci K-means)

---

#### Pitanje 7: GMM s dijeljenom kovarijancom vs K-medoidi - najsličniji rezultati?

| Odgovor  | Opis                                                                                      |
| -------- | ----------------------------------------------------------------------------------------- |
| A        | GMM: $\Sigma_k = \text{diag}(\sigma_1^2, ..., \sigma_n^2)$ i $\pi_k = 1/K$; KM: euklidska |
| B        | GMM: $\Sigma_k = \sigma^2 I$; KM: euklidska udaljenost                                    |
| **✅ C** | **GMM: puna $\Sigma_k$ i $\pi_k = 1/K$; KM: Mahalanobisova udaljenost**                   |
| D        | GMM: $\Sigma_k = \sigma^2 I$ i $\pi_k = 1/K$; KM: Mahalanobisova                          |

> **Objašnjenje:** S **punom dijeljenom kovarijancom** GMM modelira elipsoidne grupe s korelacijama. **Mahalanobisova udaljenost** $d(x,y) = \sqrt{(x-y)^T \Sigma^{-1} (x-y)}$ upravo uzima u obzir kovarijacijsku strukturu, pa K-medoidi s Mahalanobisovom daju najsličnije rezultate.

---

#### Pitanje 8: Akaikeov kriterij (AIC) za odabir broja grupa?

| Odgovor  | Opis                                                                          |
| -------- | ----------------------------------------------------------------------------- |
| A        | Minimizira nepotpunu, maksimizira potpunu log-izglednost                      |
| B        | Maksimizira očekivanje uz izotropnu kovarijancu                               |
| **✅ C** | **Odabire model koji podatke čini najvjerojatnijima sa što manje parametara** |
| D        | Odabire K kod kojeg log-izglednost stagnira                                   |

> **Objašnjenje:** AIC balansira **kvalitetu prilagodbe** (log-izglednost) i **složenost modela** (broj parametara):
> $$K^* = \arg\min_K \left( -2 \ln L(K) + 2q(K) \right)$$
> Penalizira modele s previše parametara (sprječava prenaučenost).

---

#### Pitanje 9: Zašto GMM nema zatvorenu formu, a GBC ima?

| Odgovor  | Opis                                                                                                         |
| -------- | ------------------------------------------------------------------------------------------------------------ |
| A        | GMM je nenadzirani pa log-izglednost nije definirana                                                         |
| B        | GMM treba procijeniti kovarijancijske matrice, za što nema zatvorene forme                                   |
| **✅ C** | **Kod GMM ne znamo koji primjer pripada grupi → $p(x)$ je zbroj gustoća → $\ln(\sum)$ nema zatvorenu formu** |
| D        | Oba imaju zatvorenu formu, ali EM je računski jednostavniji                                                  |

> **Objašnjenje:**
>
> - **GBC:** Znamo oznake y → $\ln L = \sum_i \ln p(x^{(i)}|y^{(i)})$ → **faktorizira se**, zatvorena forma!
> - **GMM:** Ne znamo y → $\ln L = \sum_i \ln \sum_k \pi_k p(x^{(i)}|\theta_k)$ → **logaritam zbroja**, nema zatvorene forme!

---

#### Pitanje 10: K-medoidi vs HAC - sličnosti i razlike?

| Odgovor  | Opis                                                                                             |
| -------- | ------------------------------------------------------------------------------------------------ |
| A        | Oba rade s ne-euklidskom udaljenošću, K-medoidi ima veću složenost                               |
| B        | Oba imaju složenost > O(N), K-medoidi dopušta pripadnost u više grupa                            |
| C        | Oba izvode #grupa iteracija, K-medoidi radi s općenitom mjerom                                   |
| **✅ D** | **Oba mogu grupirati ne-vektorizirane primjere, ali HAC daje hijerarhiju a K-medoidi particiju** |

> **Objašnjenje:**
>
> - **Zajedničko:** Oba rade s **općenitom mjerom sličnosti/različitosti** (ne samo euklidska) → mogu grupirati **ne-vektorizirane** primjere
> - **Razlika:**
>   - **HAC** → **hijerarhija** (dendrogram)
>   - **K-medoidi** → **particija** (ravno grupiranje)

---

### 🧮 Napomene za numeričke/problemske zadatke (Cjelina 20)

#### Zadatak tip 1: GMM - usporedba odgovornosti za različite modele

**Kontekst:** Uspoređujemo modele s različitim K i tipovima kovarijance.

**Ključne napomene:**

- **Više grupa (veći K)** → primjer jasnije pripada jednoj grupi → **veća maksimalna odgovornost** $h_k^{max}$
- **Puna kovarijanca** → bolje modelira oblik klastera → **veća odgovornost** nego izotropna
- **Izotropna kovarijanca** → sferični klasteri → manja fleksibilnost

**Tipični redoslijed:** $h_{K=3,iso} > h_{K=2,full} > h_{K=2,iso}$

---

#### Zadatak tip 2: GMM - usporedba log-izglednosti i iteracija

**Notacija:**

- $LL^0_\alpha$ = **početna** log-izglednost modela $\mathcal{H}_\alpha$
- $LL^*_\alpha$ = **konačna** log-izglednost nakon konvergencije
- $k_\alpha$ = broj iteracija EM-algoritma

**Pravila:**

| Usporedba                   | Očekivani rezultat                                  |
| --------------------------- | --------------------------------------------------- |
| K-means init vs random init | K-means daje **veću** $LL^0$                        |
| Bolja inicijalizacija       | **Manje** iteracija do konvergencije                |
| Veći K                      | Općenito **veća** $LL^*$ (ali oprez: prenaučenost!) |
| Dijeljena vs nedijeljena Σ  | Nedijeljena ima **više** parametara → veća $LL^*$   |

**Tipično:** Ako $LL^0_A > LL^0_B$ (bolja init), onda često $k_A \leq k_B$ i $LL^*_A \geq LL^*_B$

---

#### Zadatak tip 3: GMM - usporedba tipova kovarijance

**Redoslijed fleksibilnosti (i tipično log-izglednosti):**

$$\text{Puna} > \text{Dijagonalna} > \text{Izotropna}$$

**Ali:** Ako je stvarna distribucija izotropna (Σ = σ²I), jednostavniji model može biti bolji!

| Model       | Slobodni parametri za Σ        | Oblik klastera     |
| ----------- | ------------------------------ | ------------------ |
| Puna        | $\frac{n(n+1)}{2}$ po klasteru | Proizvoljne elipse |
| Dijagonalna | $n$ po klasteru                | Elipse uz osi      |
| Izotropna   | 1 po klasteru                  | Krugovi/sfere      |

---

#### Zadatak tip 4: HAC - konstrukcija dendrograma (potpuno povezivanje)

**Algoritam korak-po-korak:**

1. **Izračunaj matricu sličnosti** svih parova
2. **Nađi par s najvećom sličnošću** → spoji ih
3. **Ažuriraj sličnosti** za novi klaster:
   - **Potpuno (complete):** $s(G_i, G_j) = \min_{x \in G_i, y \in G_j} s(x, y)$
4. **Ponovi** dok ne ostane jedan klaster

**Primjer:** Za matricu sličnosti:

```
     x1   x2   x3   x4   x5
x1  1.0  0.4  0.5  0.7  0.5
x2  0.4  1.0  0.9  0.3  0.6
x3  0.5  0.9  1.0  0.7  0.1
x4  0.7  0.3  0.7  1.0  0.8
x5  0.5  0.6  0.1  0.8  1.0
```

**Korak 1:** max = 0.9 (x2-x3) → spoji {x2,x3}
**Korak 2:**

- {x2,x3} do x4: min(0.3, 0.7) = 0.3
- {x2,x3} do x5: min(0.6, 0.1) = 0.1
- x4-x5: 0.8 → **max!** → spoji {x4,x5}

**Korak 3:** {x4,x5} do x1: min(0.7, 0.5) = 0.5 → **max!** → spoji {x1,x4,x5}

**Rezultat:** ((x2,x3), ((x4,x5), x1)) → **Odgovor C**

---

#### Zadatak tip 5: HAC - zbroj sličnosti pri spajanju

**Postupak:** Zabilježi sličnost na kojoj se spajaju grupe u svakoj iteraciji, pa zbroji.

**Primjer:** Za matricu:

```
1.0  0.2  0.8  0.1  0.4
0.2  1.0  0.9  0.3  0.7
0.8  0.9  1.0  0.6  0.5
0.1  0.3  0.6  1.0  0.4
0.4  0.7  0.5  0.4  1.0
```

| Iteracija | Spajanje         | Sličnost |
| --------- | ---------------- | -------- |
| 1         | {x2,x3}          | 0.9      |
| 2         | {x2,x3,x5}       | 0.5      |
| 3         | {x2,x3,x4,x5}    | 0.3      |
| 4         | {x1,x2,x3,x4,x5} | 0.1      |

**Zbroj:** 0.9 + 0.5 + 0.3 + 0.1 = **1.8** → **Odgovor A**

---

#### Zadatak tip 6: HAC s Jaccardovom sličnošću (tekst/skupovi)

**Jaccardova sličnost:** $\kappa(x_1, x_2) = \frac{|x_1 \cap x_2|}{|x_1 \cup x_2|}$

**Primjer za riječi (skupovi slova):**

- "water" = {w, a, t, e, r}
- "watering" = {w, a, t, e, r, i, n, g}
- "earth" = {e, a, r, t, h}
- "air" = {a, i, r}

**Izračun:**
$$\kappa(\text{water}, \text{earth}) = \frac{|\{a,t,e,r\}|}{|\{w,a,t,e,r,h\}|} = \frac{4}{6} \approx 0.667$$

**Prosječno povezivanje:** Sličnost između klastera = **prosjek** svih parova

Ako se u 1. iteraciji spoje "water" i "earth", u 2. iteraciji:
$$s(\{water, earth\}, watering) = \frac{\kappa(water, watering) + \kappa(earth, watering)}{2} = \frac{0.625 + 0.444}{2} \approx 0.535$$

---

#### Brze napomene za ispitne zadatke

| Situacija                | Očekuj                                           |
| ------------------------ | ------------------------------------------------ |
| K-means++ vs random init | K-means++ → bolja početna LL, manje iteracija    |
| Veći K                   | Veća LL (ali možda prenaučenost)                 |
| Potpuno povezivanje      | Kompaktni klasteri, min sličnost između klastera |
| Prosječno povezivanje    | Prosjek svih parova, robusniji na outliere       |
| Dijeljena Σ              | Svi klasteri istog oblika                        |
| GMM → K-means            | Izotropna dijeljena Σ + tvrdo grupiranje         |

⚠️ **Česte greške:**

- **Complete linkage:** Koristi **MIN** sličnosti (ili MAX udaljenosti)!
- **Single linkage:** Koristi **MAX** sličnosti (ili MIN udaljenosti)!
- **Jaccard:** Presijek/unija **skupova**, ne duljina stringova!

---

## Cjelina 21: Vrednovanje modela

> **📚 TEORIJA:** Ova cjelina se NE ispituje direktno u laboratorijskoj vježbi 4, ali je važna za razumijevanje evaluacije modela i pojavljuje se na ispitu!

### 1. Matrica zabune (Confusion Matrix)

Za binarne klasifikatore ($y \in \{0, 1\}$):

|                | $y_{true} = 1$        | $y_{true} = 0$        |
| -------------- | --------------------- | --------------------- |
| $y_{pred} = 1$ | **TP** (stvarno poz.) | **FP** (lažno poz.)   |
| $y_{pred} = 0$ | **FN** (lažno neg.)   | **TN** (stvarno neg.) |

**Definicije:**

- **TP** = predikcija 1, stvarna oznaka 1 ✓
- **FP** = predikcija 1, stvarna oznaka 0 ✗ (lažni alarm)
- **FN** = predikcija 0, stvarna oznaka 1 ✗ (promašaj)
- **TN** = predikcija 0, stvarna oznaka 0 ✓

---

### 2. Osnovne mjere vrednovanja

| Mjera              | Formula                             | Što mjeri?                                   | Idealno |
| ------------------ | ----------------------------------- | -------------------------------------------- | ------- |
| **Točnost (Acc)**  | $\frac{TP + TN}{TP + FP + FN + TN}$ | Udio točno klasificiranih                    | 1       |
| **Preciznost (P)** | $\frac{TP}{TP + FP}$                | Od predviđenih poz., koliko je stvarno poz.? | 1       |
| **Odziv (R, TPR)** | $\frac{TP}{TP + FN}$                | Od stvarno poz., koliko smo detektirali?     | 1       |
| **FPR**            | $\frac{FP}{FP + TN}$                | Stopa lažnog alarma                          | 0       |
| **Specifičnost**   | $\frac{TN}{TN + FP}$                | Od stvarno neg., koliko smo detektirali?     | 1       |

> ⚠️ **PROBLEM S TOČNOŠĆU:** Kod neuravnoteženih klasa, trivijalni klasifikator (uvijek predviđa većinsku klasu) ima visoku točnost!

**Primjer:** 100 pozitivnih, 900 negativnih → klasifikator koji uvijek kaže "0" ima Acc = 90%!

---

### 3. Mjera F1

**F1** = harmonijska sredina preciznosti i odziva:

$$F_1 = \frac{2}{\frac{1}{P} + \frac{1}{R}} = \frac{2PR}{P + R}$$

**Zašto harmonijska, a ne aritmetička sredina?**

- P i R imaju **različite skale** (različiti nazivnici)
- Harmonijska sredina je **stroža** - bliža manjoj vrijednosti
- Aritmetička bi dala preoptimističnu procjenu

**Primjer:** P = 0.1, R = 0.8 → F1 = 0.178, aritmetička = 0.45

| Situacija       | F1                          |
| --------------- | --------------------------- |
| P = R           | F1 = P = R                  |
| P ≠ R           | F1 bliže manjoj vrijednosti |
| P = 0 ili R = 0 | F1 = 0                      |

---

### 4. Višeklasna klasifikacija (K > 2)

#### Matrica zabune K × K

Za K klasa, matrica je dimenzija K × K. Primjer za K = 3:

|              | $y_{true}=1$ | $y_{true}=2$ | $y_{true}=3$ |
| ------------ | ------------ | ------------ | ------------ |
| $y_{pred}=1$ | 1            | 1            | 0            |
| $y_{pred}=2$ | 2            | 6            | 2            |
| $y_{pred}=3$ | 1            | 0            | 1            |

**Točnost:** $Acc = \frac{\text{trag matrice}}{\text{suma svih elemenata}} = \frac{1+6+1}{14} = 0.571$

#### Dekompozicija u K binarnih matrica

Za klasu $y = j$, izvlačimo binarnu matricu 2×2:

- $TP_j$ = element [j,j] (dijagonala)
- $FP_j$ = suma retka j bez dijagonale
- $FN_j$ = suma stupca j bez dijagonale
- $TN_j$ = N - TP_j - FP_j - FN_j

---

### 5. Mikro i makro uprosječivanje

| Metoda    | Postupak                                     | Formula                                               |
| --------- | -------------------------------------------- | ----------------------------------------------------- |
| **Makro** | Izračunaj mjeru za svaku klasu, pa uprosječi | $m^M = \frac{1}{K} \sum_j m_j$                        |
| **Mikro** | Zbroji sve matrice, pa izračunaj mjeru       | $m^\mu = m\left(\sum_j TP_j, \sum_j FP_j, ...\right)$ |

**Ključna činjenica:**
$$P^\mu = R^\mu = F_1^\mu = Acc$$

> **Kada koristiti što:**
>
> - **Makro** → sve klase jednako važne (neovisno o broju primjera)
> - **Mikro** → svaki primjer jednako važan (veće klase dominiraju)
> - Tipično: $F_1^M < F_1^\mu$ (jer klasifikatori lošije rade na manjim klasama)

---

### 6. Klasifikatori s pragom

Mnogi klasifikatori daju **vjerojatnost** $P(y=1|x)$, ne samo oznaku.

**Standardni prag:** 0.5

| Prag                | Efekt                                       |
| ------------------- | ------------------------------------------- |
| **Viši** (npr. 0.8) | Manje FP → **veća preciznost**, manji odziv |
| **Niži** (npr. 0.3) | Manje FN → **veći odziv**, manja preciznost |

#### Krivulja Preciznost-Odziv (PR curve)

- X-os: Odziv (R)
- Y-os: Preciznost (P)
- Smanjujemo prag od 1 do 0
- **Bolje:** krivulja bliža točki (P=1, R=1)
- **Prosječna preciznost:** integral ispod krivulje

#### Krivulja ROC

- X-os: FPR (stopa lažnog alarma)
- Y-os: TPR (odziv)
- **Bolje:** krivulja bliža točki (FPR=0, TPR=1)
- **Nasumični klasifikator:** pravac od (0,0) do (1,1), AUC = 0.5

**AUC (Area Under Curve):**

- Površina ispod ROC krivulje
- AUC ∈ [0, 1], više = bolje
- AUC = 0.5 → nasumični klasifikator
- AUC < 0.5 → lošije od nasumičnog!

---

### 7. Procjena pogreške modela

#### Nepoštene procjene ❌

- **Treniranje i testiranje na istom skupu** → mjeri pogrešku učenja, ne generalizacije!

#### Metoda izdvajanja (Holdout)

Podijeli D na:

- $D_{train}$ (tipično 70-80%)
- $D_{test}$ (tipično 20-30%)

**Problem:** Bacamo primjere, procjena ovisi o podjeli.

#### k-struka unakrsna provjera (k-fold CV)

```
1. Podijeli D na k preklopa
2. Za i = 1 do k:
   - Treniraj na (k-1) preklopa
   - Testiraj na i-tom preklopu
3. Procjena = prosjek k pogrešaka
```

**Tipično:** k = 5 ili k = 10

**Stratifikacija:** Očuvaj omjer klasa u svakom preklopu!

#### LOOCV (Leave-One-Out)

k = N (broj primjera)

- Treniraj na N-1 primjera, testiraj na 1
- Koristi kad je N mali

---

### 8. Ugniježđena unakrsna provjera (k × l)

Kada trebamo **i** odabir modela (hiperparametara) **i** procjenu pogreške:

**Tri skupa:**

- $D_{train}$ - učenje modela
- $D_{val}$ - odabir hiperparametara
- $D_{test}$ - konačna procjena

**Algoritam:**

```
VANJSKA PETLJA (k iteracija):
  D_train = k-1 preklopa, D_test = 1 preklop

  UNUTARNJA PETLJA (l iteracija, za svaki α):
    D_train' = l-1 preklopa, D_val = 1 preklop
    Treniraj model(α) na D_train', procijeni na D_val

  Odaberi α* koji minimizira pogrešku na D_val
  Treniraj model(α*) na cijelom D_train
  Procijeni pogrešku na D_test

Rezultat = prosjek k pogrešaka na D_test
```

> ⚠️ **VAŽNO:** $D_{test}$ NIKAD ne smije biti korišten za:
>
> - Treniranje modela
> - Odabir hiperparametara
> - Bilo kakve odluke!

---

### 📋 Praktične formule za ispitne zadatke

#### Iz matrice zabune izračunaj sve mjere:

Za matricu: $\begin{pmatrix} TP & FP \\ FN & TN \end{pmatrix}$

| Mjera | Formula           |
| ----- | ----------------- |
| N     | TP + FP + FN + TN |
| Acc   | (TP + TN) / N     |
| P     | TP / (TP + FP)    |
| R     | TP / (TP + FN)    |
| F1    | 2PR / (P + R)     |
| FPR   | FP / (FP + TN)    |

#### Makro vs Mikro - brzi primjer

Za 3 klase s matricama:

- Klasa 1: TP=1, FP=2, FN=3, TN=9
- Klasa 2: TP=6, FP=4, FN=1, TN=4
- Klasa 3: TP=1, FP=1, FN=3, TN=10

**Makro-P:** $(P_1 + P_2 + P_3) / 3 = (0.33 + 0.6 + 0.5) / 3 = 0.48$

**Mikro-P:** $(1+6+1) / ((1+6+1) + (2+4+1)) = 8 / 15 = 0.53$

---

### 📝 Teorijska ispitna pitanja (Cjelina 21)

#### Pitanje 1: Zašto F1-mjera koristi harmonijsku, a ne aritmetičku sredinu?

| Odgovor  | Opis                                                                                    |
| -------- | --------------------------------------------------------------------------------------- |
| A        | Jer su P i R obrnuto proporcionalni, ali definirani na istom intervalu                  |
| B        | Jer niti P niti R ne uzimaju u obzir broj stvarno negativnih primjera                   |
| **✅ C** | **Jer P i R nisu definirani na istoj skali, ali njihove recipročne vrijednosti jesu**   |
| D        | Jer P nije definiran za trivijalan klasifikator koji sve primjere klasificira negativno |

> **Objašnjenje:**
>
> - P = TP / (TP + **FP**) i R = TP / (TP + **FN**) imaju **različite nazivnike** → različite skale
> - Recipročne vrijednosti 1/P i 1/R imaju istu skalu (TP u nazivniku)
> - Harmonijska sredina = recipročna vrijednost aritmetičke sredine recipročnih vrijednosti
> - Zato možemo "usrednjavati" P i R na smislen način

---

#### Pitanje 2: Kada F1-mjera nije prikladna (previše optimistična)?

Pretpostavka: F1 = 0 kad je harmonijska sredina nedefinirana.

| Odgovor  | Opis                                                                                    |
| -------- | --------------------------------------------------------------------------------------- |
| **✅ A** | **Ako je većina primjera pozitivna, a klasifikator sve primjere klasificira pozitivno** |
| B        | Ako je većina primjera pozitivna, a klasifikator sve primjere klasificira negativno     |
| C        | Ako je većina primjera negativna, a klasifikator sve primjere klasificira pozitivno     |
| D        | Ako je većina primjera negativna i klasifikator sve primjere klasificira negativno      |

> **Objašnjenje:** Ako je većina pozitivna i klasifikator sve klasificira pozitivno:
>
> - TP = veliki (većina primjera)
> - FP = mali (manjina primjera)
> - FN = 0 (sve je predviđeno pozitivno)
> - **P = TP/(TP+FP) = visoka** (jer je FP mali)
> - **R = TP/(TP+FN) = 1** (jer je FN = 0)
> - **F1 = visoka!** → ali klasifikator je trivijalan!

---

#### Pitanje 3: Očekivani odnos $F_1^M$ i $F_1^\mu$?

| Odgovor  | Opis                                                                                                             |
| -------- | ---------------------------------------------------------------------------------------------------------------- |
| **✅ A** | **$F_1^M < F_1^\mu$, jer makro daje jednak utjecaj svim klasama, a klasifikator na manjim klasama više griješi** |
| B        | $F_1^M > F_1^\mu$, jer mikro zbraja matrice, pa manje klase manje doprinose                                      |
| C        | $F_1^M > F_1^\mu$, jer makro zbraja matrice, pa veće klase više doprinose                                        |
| D        | $F_1^M < F_1^\mu$, jer mikro računa prosjek, a klasifikator na većim klasama manje griješi                       |

> **Objašnjenje:**
>
> - **Makro:** Svaka klasa ima **jednak utjecaj** → male klase (s lošijom točnošću) "vuku" prosjek dolje
> - **Mikro:** Veće klase **dominiraju** (više primjera) → bolja ukupna mjera
> - Klasifikatori tipično rade **lošije na manjim klasama** (manje primjera za učenje)
> - Zato je uobičajeno: $F_1^M < F_1^\mu$

---

#### Pitanje 4: Nedostatak LOOCV metode?

| Odgovor  | Opis                                                                                 |
| -------- | ------------------------------------------------------------------------------------ |
| A        | Procjena je pristrana jer se ispitni skupovi preklapaju u 1/N primjera               |
| **✅ B** | **Varijanca procjene je visoka jer klasifikatori dijele (N-2)/N primjera za učenje** |
| C        | Procjena može biti pesimistična jer ispitani model može biti suboptimalne složenosti |
| D        | Procjena je pristrana jer se svaki primjer u skupu za ispitivanje koristi N puta     |

> **Objašnjenje:**
>
> - Kod LOOCV, svaka dva klasifikatora dijele **(N-2)/N** primjera za učenje
> - Za veliki N, to je skoro 100% → klasifikatori su **gotovo identični**
> - To dovodi do **visoke korelacije** između N procjena pogreške
> - Posljedica: **visoka varijanca** ukupne procjene (procjene nisu nezavisne)

---

#### Pitanje 5: Motivacija za ugniježđenu unakrsnu provjeru?

| Odgovor  | Opis                                                                                                      |
| -------- | --------------------------------------------------------------------------------------------------------- |
| **✅ A** | **Omogućava procjenu prediktivne moći modela optimalne složenosti uz maksimalno iskorištavanje podataka** |
| B        | Provodi optimizaciju hiperparametara na uniji skupa za provjeru i testiranje                              |
| C        | Razdvaja skup za učenje od skupa za ispitivanje                                                           |
| D        | Omogućava određivanje točnosti za različite vrijednosti klasifikacijskog praga                            |

> **Objašnjenje:** Ugniježđena CV kombinira:
>
> - **Unutarnja petlja:** Odabir optimalnih hiperparametara (na validation skupu)
> - **Vanjska petlja:** Procjena pogreške generalizacije optimalnog modela (na test skupu)
> - Maksimalno iskorištava podatke za oboje!

---

#### Pitanje 6: Prednost ugniježđene k-struke CV nad običnom CV?

| Odgovor  | Opis                                                                     |
| -------- | ------------------------------------------------------------------------ |
| A        | Procjenjujemo pogrešku generalizacije, a ne pogrešku učenja              |
| B        | Model ispitujemo na cijelom raspoloživom skupu primjera                  |
| C        | Procjenjujemo ispitnu pogrešku modela s najmanjom pogreškom učenja       |
| **✅ D** | **Procjenjujemo očekivanu ispitnu pogrešku modela optimalne složenosti** |

> **Objašnjenje:**
>
> - Obična CV: Procjenjuje pogrešku **fiksnog** modela (bez optimizacije hiperparametara)
> - Ugniježđena CV: Procjenjuje pogrešku modela **optimalne složenosti**
> - Unutarnja petlja pronalazi optimalne hiperparametre
> - Vanjska petlja procjenjuje pogrešku tako optimiziranog modela
> - To je realističnija procjena jer u praksi uvijek optimiziramo hiperparametre!

---

### 🧮 Napomene za numeričke/problemske zadatke (Cjelina 21)

#### Zadatak tip 1: Mikro-F1 vs Makro-F1 iz matrice K×K

**Postupak:**

1. **Mikro-F1 = Točnost** = trag(matrica) / N
   $$F_1^\mu = \frac{TP_1 + TP_2 + ... + TP_K}{N}$$

2. **Makro-F1:**
   - Za svaku klasu j izračunaj P_j, R_j, F1_j
   - $F_1^M = \frac{1}{K} \sum_j F_{1,j}$

3. **Razlika:** $F_1^\mu - F_1^M$ (tipično pozitivna!)

**Primjer:** Za matricu 3×3, prvo izračunaj dijagonalne elemente (TP), pa retke (TP+FP), stupce (TP+FN).

---

#### Zadatak tip 2: MLR vs RAND klasifikator

**RAND klasifikator:** Predviđa klasu j s vjerojatnošću proporcionalnom broju primjera klase j.

Za klasu s $n_j$ primjera od ukupno N:

- $P(\text{pred}=j) = n_j / N$
- Očekivani $TP_j = n_j \cdot (n_j / N) = n_j^2 / N$

**Mikro-F1 za RAND:**
$$F_1^\mu(\text{RAND}) = \frac{\sum_j n_j^2 / N}{N} = \frac{\sum_j n_j^2}{N^2}$$

---

#### Zadatak tip 3: AUC iz parova (y, h(x))

**Postupak:**

1. **Sortiraj** primjere po h(x) silazno
2. **Izračunaj** TPR i FPR za svaki prag:
   - TPR = TP / (ukupno pozitivnih)
   - FPR = FP / (ukupno negativnih)
3. **Nacrtaj** ROC: točke (FPR, TPR)
4. **AUC** = suma trapeza između točaka

**Formula za trapez:**
$$AUC = \sum_i \frac{(TPR_i + TPR_{i+1})}{2} \cdot (FPR_{i+1} - FPR_i)$$

**Razlika od nasumičnog:** AUC - 0.5

---

#### Zadatak tip 4: Usporedba klasifikatora po ROC

**Pravila:**

- Klasifikator je **bolji od nasumičnog** ako je ROC iznad dijagonale (AUC > 0.5)
- Klasifikator je **lošiji od nasumičnog** ako je ROC ispod dijagonale (AUC < 0.5)

**Popravak lošeg klasifikatora:**

- Ako AUC < 0.5, koristi **1 - h(x)** umjesto h(x)
- Nova ROC: (FPR, TPR) → (1-FPR, 1-TPR)
- Novi AUC = 1 - stari AUC

**Usporedba:** Bolji klasifikator ima ROC **bliže točki (0, 1)**.

---

#### Zadatak tip 5: Dominacija ROC krivulja

$h_1 > h_2$ (h1 striktno dominira h2) znači:
$$\forall \theta: \text{FPR}_\theta(h_1) = \text{FPR}_\theta(h_2) \Rightarrow \text{TPR}_\theta(h_1) > \text{TPR}_\theta(h_2)$$

**Posljedica:** Ako $h_1 > h_2$, onda $AUC(h_1) > AUC(h_2)$

---

#### Zadatak tip 6-7: Ugniježđena CV - broj treniranja

**Parametri:**

- k = vanjski preklopi, l = unutarnji preklopi
- H = broj kombinacija hiperparametara

**Broj treniranja modela:**

- Unutarnja petlja: $k \times H \times l$ treniranja
- Vanjska petlja (finalni modeli): $k$ treniranja
- **Ukupno:** $k \times (H \times l + 1)$

**Primjer:** k=10, l=5, H=992 (SVM s C i γ)

- Unutarnja: 10 × 992 × 5 = 49,600
- Vanjska: 10
- Ukupno: ≈ 49,610

**Povećanje l:** Ako l: 5→10, unutarnji dio se udvostručuje!

---

#### Zadatak tip 8: Greške u ugniježđenoj CV

**Tipične greške:**

1. **Korištenje test skupa za hiperparametre** → preoptimistična procjena
2. **Fiksni fold u unutarnjoj petlji** → loša procjena optimalnih hiperparametara
3. **Trening na cijelom skupu** u vanjskoj petlji → manja varijanca ali pristrana

**Očekivanja:**

- Ispravna CV daje bolju procjenu pogreške generalizacije
- Model optimalne složenosti ima manju pogrešku na novim podacima

---

#### Brze formule za ROC/AUC zadatke

| Situacija                    | Formula/Vrijednost       |
| ---------------------------- | ------------------------ |
| AUC nasumičnog klasifikatora | 0.5                      |
| AUC savršenog klasifikatora  | 1.0                      |
| AUC lošijeg od nasumičnog    | < 0.5 (invertiraj!)      |
| Inverzija klasifikatora      | AUC_novi = 1 - AUC_stari |
| TPR (odziv)                  | TP / (TP + FN)           |
| FPR                          | FP / (FP + TN)           |

---

#### Česte greške u zadacima

⚠️ **ROC sortiranje:** Sortiraj po h(x) **SILAZNO** (od najvećeg praga)!

⚠️ **AUC trapezi:** Ne zaboravi točke (0,0) i (1,1)!

⚠️ **Mikro vs Makro:** Mikro = Acc, Makro = prosjek po klasama!

⚠️ **RAND klasifikator:** Predviđa proporcionalno distribuciji klasa!

⚠️ **Ugniježđena CV:** Unutarnja bira hiperparametre, vanjska procjenjuje pogrešku!

---

### ⚠️ Česte greške na ispitu

1. **Miješanje P i R:** Preciznost = od predviđenih poz., Odziv = od stvarno poz.

2. **Točnost kod neuravnoteženih klasa:** Visoka točnost ≠ dobar klasifikator!

3. **Mikro = Točnost:** $P^\mu = R^\mu = F_1^\mu = Acc$

4. **Testiranje na trening skupu:** NIKAD! Mjeri pogrešku učenja, ne generalizacije.

5. **Hiperparametri na test skupu:** NIKAD koristiti test skup za odabir hiperparametara!

6. **ROC za nasumični klasifikator:** Dijagonala (0,0)→(1,1), AUC = 0.5

---

_Dokument pripremljen za ispit i laboratorijsku vježbu 4. Sretno! 🍀_
