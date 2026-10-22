# Strojno Učenje 1 - Gradivo za Međuispit

**Fakultet elektrotehnike i računarstva, Sveučilište u Zagrebu**
**Akademska godina 2025./2026.**

---

## Sadržaj

- [Cjelina 2: Osnovni koncepti](#cjelina-2-osnovni-koncepti)
- [Cjelina 3: Linearna regresija](#cjelina-3-linearna-regresija)
- [Cjelina 4: Linearna regresija II](#cjelina-4-linearna-regresija-ii)
- [Cjelina 5: Linearni diskriminativni modeli](#cjelina-5-linearni-diskriminativni-modeli)
- [Cjelina 6: Logistička regresija](#cjelina-6-logistička-regresija)
- [Cjelina 7: Logistička regresija II](#cjelina-7-logistička-regresija-ii)
- [Cjelina 8: Stroj potpornih vektora](#cjelina-8-stroj-potpornih-vektora)
- [Cjelina 9: Stroj potpornih vektora II](#cjelina-9-stroj-potpornih-vektora-ii)
- [Cjelina 10: Jezgrene metode](#cjelina-10-jezgrene-metode)
- [Cjelina 11: Neparametarske metode](#cjelina-11-neparametarske-metode)

---

## Cjelina 2: Osnovni koncepti

### 1. Primjena algoritma strojnog učenja (9 koraka)

| Korak | Opis |
|-------|------|
| 1. Priprema podataka | Upoznavanje s podatcima, preliminarna analiza |
| 2. Ručno označavanje | Označavanje primjera za učenje i ispitivanje (nije uvijek potrebno) |
| 3. Ekstrakcija značajki | Svaki primjer prikazujemo kao vektor značajki - najkreativniji korak |
| 4. Redukcija dimenzionalnosti | Smanjenje broja značajki (ako ih ima previše) |
| **5. Odabir modela** | Ključan korak koji početnici često propuste ili pogrešno naprave |
| **6. Učenje modela** | Algoritam optimizira parametre modela |
| **7. Vrednovanje modela** | Provjera koliko dobro model radi |
| 8. Dijagnostika | Debugiranje modela koji ne radi dovoljno dobro |
| 9. Instalacija (deployment) | Ugradnja u produkciju |

> **Fokus kolegija:** Koraci 5-7 (odabir modela, učenje, vrednovanje)

---

### 2. Prostor primjera i značajke

**Primjer** (instance) = jedna podatkovna točka (npr. jedna osoba, jedan putnik, jedna kuća)

**Vektor značajki:**
$$x = (x_1, x_2, \ldots, x_n)$$

- n = broj značajki (dimenzija ulaznog prostora)
- Pretpostavka: sve značajke su numeričke, x ∈ R^n

**Prostor primjera** (ulazni prostor) X = R^n

> **Napomena:** Koristimo veliko **N** za broj primjera, a malo **n** za broj značajki. Idealno: N >> n

---

### 3. Označeni primjeri

**Oznaka** y ∈ Y:
- **Klasifikacija** u K klasa: Y = {0, ..., K-1}
- **Binarna klasifikacija:** Y = {0, 1} ili Y = {-1, +1}
- **Regresija:** Y = R

**Skup označenih primjera:**
$$D = \{(x^{(i)}, y^{(i)})\}_{i=1}^{N} \subset X \times Y$$

**Matrični zapis:** D = (X, y) gdje je:
- **X** = matrica dizajna (N × n) - retci su primjeri, stupci su značajke
- **y** = vektor oznaka (N × 1)

| Notacija | Značenje |
|----------|----------|
| x^(i) | i-ti primjer (vektor značajki) |
| x_j | j-ta značajka |
| x^(i)_j | j-ta značajka i-tog primjera |

---

### 4. Hipoteza

**Hipoteza** h je funkcija koja primjerima dodjeljuje oznake:
$$h : X \rightarrow Y$$

Hipoteza je **parametrizirana** vektorom parametara θ:
$$h(x; \theta)$$

**Primjer (regresija):** h(x; θ₀, θ₁) = θ₁x + θ₀ (jednadžba pravca)

**Primjer (binarna klasifikacija):**
$$h(x_1, x_2; \theta_0, \theta_1, \theta_2) = 1\{\theta_1 x_1 + \theta_2 x_2 + \theta_0 \geq 0\}$$

Funkcija 1{P} vraća 1 ako je P istinit, inače 0.

---

### 5. Model

**Model** H = skup hipoteza (skup funkcija parametriziranih sa θ):
$$H = \{h(x; \theta)\}_\theta$$

- Svaki θ jednoznačno određuje jednu hipotezu h ∈ H
- **Učenje = pretraživanje skupa H** u potrazi za najboljom hipotezom
- Učenje je **optimizacijski problem**

---

### 6. Empirijska pogreška i funkcija gubitka

#### Funkcija gubitka

L : Y × Y → R⁺ - mjeri pogrešku na **jednom** primjeru:
$$L(y, h(x))$$

**Gubitak nula-jedan** (za klasifikaciju):
$$L(y, h(x)) = 1\{h(x) \neq y\}$$

#### Empirijska pogreška

Srednja vrijednost funkcije gubitka na skupu D:
$$E(h|D) = \frac{1}{N} \sum_{i=1}^{N} L(y^{(i)}, h(x^{(i)}))$$

Za **pogrešku klasifikacije:**
$$E(h|D) = \frac{1}{N} \sum_{i=1}^{N} 1\{h(x^{(i)}) \neq y^{(i)}\}$$

#### Tipovi grešaka (binarna klasifikacija)

| Predikcija \ Stvarno | y = 1 | y = 0 |
|----------------------|-------|-------|
| h(x) = 1 | **TP** (istinito pozitivan) | **FP** (lažno pozitivan) |
| h(x) = 0 | **FN** (lažno negativan) | **TN** (istinito negativan) |

Empirijska pogreška = (FP + FN) / N

---

### 7. Tri komponente algoritma SU ⚠️

Svaki algoritam strojnog učenja ima tri komponente:

| Komponenta | Formula | Opis |
|------------|---------|------|
| **1. Model** | H = {h(x; θ)}_θ | Skup hipoteza parametriziranih sa θ |
| **2. Funkcija gubitka/pogreške** | E(θ\|D) = 1/N Σ L(y^(i), h(x^(i); θ)) | Mjeri koliko hipoteza griješi |
| **3. Optimizacijski postupak** | θ* = argmin_θ E(θ\|D) | Nalazi parametre koji minimiziraju pogrešku |

> **Ključno:** θ* su parametri naučenog/treniranog modela, h* je naučena hipoteza

---

### 8. Složenost modela

**Problem:** Ako model nema dovoljnu složenost (kapacitet), ne može ostvariti E(h|D) = 0.

Ali: Ako je model **presložen**, prilagodi se **šumu** u podatcima!

#### Izvori šuma u podatcima:
- Nepreciznost pri mjerenju značajki
- Pogreške u označavanju (teacher noise)
- Skrivene značajke (latentne varijable)
- Nejasne granice između klasa (subjektivnost)

#### Podnačenost vs prenačenost

| Pojam | Eng. | Opis | Pogreška učenja | Ispitna pogreška |
|-------|------|------|-----------------|------------------|
| **Podnačenost** | Underfitting | Model **prejednostavan** | Visoka | Visoka |
| **Prenačenost** | Overfitting | Model **presložen** | Niska | Visoka |
| **Optimalan model** | - | Ni presložen ni prejednostavan | Umjerena | Niska |

> **Ključno:** Presložen model nauči šum → loša generalizacija na neviđenim primjerima

#### Prednosti jednostavnijih modela:
1. **Bolja generalizacija** - manja šansa za prenačenost
2. **Lakše učenje** - manje parametara, brže treniranje
3. **Lakše tumačenje** - razumljivi rezultati, nije "crna kutija"

---

### 9. Odabir modela (Model Selection)

**Familija modela:** {H₁, H₂, ..., H_k} - od jednostavnijih do složenijih

**Hiperparametar** = parametar koji određuje **koji model** koristimo (npr. stupanj polinoma)

| Pojam | Što određuje | Tko optimizira |
|-------|-------------|----------------|
| **Parametri** (θ) | Hipotezu h unutar modela H | Algoritam SU |
| **Hiperparametri** | Koji model H koristimo | Mi (čovjek) |

> **Redosljed:** Prvo odabir modela (hiperparametri) → pa učenje (parametri)

> **Važno:** Algoritam SU **nije** zadužen za optimizaciju hiperparametara! To je naša odgovornost.

---

### 10. Unakrsna provjera (Cross-Validation)

**Cilj:** Procijeniti sposobnost generalizacije modela.

**Ideja:** Podijeliti skup primjera na dva dijela:
$$D = D_{train} \cup D_{test}, \quad D_{train} \cap D_{test} = \emptyset$$

Tipična podjela: 70:30 ili 60:40

#### Dvije pogreške:

| Pogreška | Na čemu se mjeri | Što govori |
|----------|------------------|------------|
| **Pogreška učenja** E(h\|D_train) | Skup za učenje | Koliko je model naučio podatke |
| **Ispitna pogreška** E(h\|D_test) | Skup za ispitivanje | Koliko dobro model **generalizira** |

> **Općenito:** Ispitna pogreška ≥ pogreška učenja (jer je model optimiziran na D_train)

#### Odnos pogrešaka za različite modele:

| Model | Pogreška učenja | Ispitna pogreška | Status |
|-------|-----------------|------------------|--------|
| Prejednostavan | Visoka | Visoka | Podnačenost |
| Optimalan | Umjerena | Niska | ✅ |
| Presložen | Niska (≈0) | Visoka | Prenačenost |

#### k-struka unakrsna provjera (k-fold CV)

```
1. Podijeli D na k jednakih dijelova (preklopa)
2. Za i = 1 do k:
   - Treniraj na (k-1) preklopa
   - Testiraj na i-tom preklopu
3. Konačna procjena = prosjek k ispitnih pogrešaka
```

- Tipično k = 5 ili k = 10
- Svaki primjer točno jednom bude u ispitnom skupu
- Daje bolju procjenu jer koristi sve podatke i za učenje i za ispitivanje

#### Stratificirana k-struka CV

- Osigurava da svaki preklop ima **isti omjer klasa** kao cijeli D
- Posebno važno kod neuravnoteženih klasa

#### Postupak odabira modela s CV:

```
Za svaki model Hi iz familije {H1, H2, ..., Hk}:
  1. Provedi k-struku CV
  2. Izračunaj prosječnu ispitnu pogrešku
Odaberi model s najmanjom prosječnom ispitnom pogreškom
```

---

### 11. Ključni pojmovi - sažetak

| Pojam | Definicija |
|-------|-----------|
| **Primjer** x | Vektor značajki, x ∈ X |
| **Oznaka** y | Klasa (klasifikacija) ili ciljna vrijednost (regresija), y ∈ Y |
| **Skup primjera** D | Parovi (x, y), N primjera |
| **Hipoteza** h | Funkcija h: X → Y, parametrizirana sa θ |
| **Model** H | Skup hipoteza {h(x; θ)}_θ |
| **Funkcija gubitka** L | Pogreška na jednom primjeru |
| **Empirijska pogreška** E(h\|D) | Prosječna pogreška na skupu D |
| **Hiperparametar** | Određuje model H (optimizira čovjek) |
| **Parametar** θ | Određuje hipotezu h (optimizira algoritam) |
| **Podnačenost** | Prejednostavan model → visoka pogreška na svemu |
| **Prenačenost** | Presložen model → niska pogreška učenja, visoka ispitna |
| **Generalizacija** | Sposobnost modela da radi dobro na neviđenim primjerima |

---

### 📝 Teorijska ispitna pitanja (Cjelina 2)

#### Pitanje 1: Zašto pogrešku modela aproksimiramo empirijskom pogreškom i na kojoj se pretpostavci temelji ta aproksimacija?

| Odgovor | Opis |
|---------|------|
| A | Različitih primjera iz X × Y potencijalno ima beskonačno mnogo, pa pogrešku računamo na uzorku D za koji pretpostavljamo da je reprezentativan |
| **✅ B** | **Ne možemo izračunati očekivanje gubitka jer nam nije poznata distribucija primjera iz X × Y, no pretpostavljamo da je D reprezentativan uzorak iz te distribucije** |
| C | Očekivanje gubitka ne možemo izračunati jer primjera iz X × Y ima potencijalno beskonačno, stoga pogrešku računamo na temelju skupa D za koji pretpostavljamo da je konačan |
| D | Funkciju gubitka jednostavnije je definirati nego funkciju pogreške, a aproksimacija je točna uz pretpostavku i.i.d. |

> **Objašnjenje:** Prava pogreška je očekivanje funkcije gubitka po distribuciji P(X, Y), ali tu distribuciju **ne poznajemo**. Zato koristimo empirijsku pogrešku na D, uz pretpostavku da je D **reprezentativan uzorak** iz te (nepoznate) distribucije. Odgovor A govori o beskonačnosti, ali to nije ključni razlog - ključno je da ne poznajemo distribuciju.

---

#### Pitanje 2: H = {h(x; θ)}_θ - Što to zapravo znači?

| Odgovor | Opis |
|---------|------|
| A | Da model sadrži beskonačno mnogo funkcija h čija konkretna definicija ovisi o vrijednostima parametara θ |
| **✅ B** | **Da različite funkcije h imaju različite parametre θ, i da su sve one sadržane u modelu, to jest za sve njih vrijedi h ∈ H** |
| C | Da za različite parametre θ dobivamo različite funkcije h, i da su sve one sadržane u modelu, to jest za sve njih vrijedi h ∈ H |
| D | Da su funkcije h definirane sa slobodnim parametrima θ i da broj različitih funkcija odgovara broju parametara |

> **Objašnjenje:** Model H je **indeksiran** sa θ. Svaki različiti θ daje različitu hipotezu h, i sve te hipoteze čine model H. Odgovor C zvuči slično, ali B preciznije kaže da različite **funkcije** imaju različite **parametre** (θ → h preslikavanje). A nije točan jer H ne mora biti beskonačan, D miješa pojmove.

---

#### Pitanje 3: Koja je razlika između parametara i hiperparametara?

| Odgovor | Opis |
|---------|------|
| **✅ A** | **Parametre optimira algoritam strojnog učenja, dok optimizacija hiperparametara nije u nadležnosti tog algoritma** |
| B | Hiperparametri određuju jačinu regularizacije, a parametri stupanj nelinearnosti hipoteze |
| C | Parametri određuju iznos empirijske pogreške na skupu za učenje, a hiperparametri iznos te pogreške na skupu za provjeru |
| D | Hiperparametri mogu biti diskretni ili kontinuirani, dok su parametri uvijek kontinuirani |

> **Objašnjenje:** Ključna razlika: **parametre** optimizira algoritam SU (npr. gradijentni spust), a **hiperparametre** odabiremo mi (čovjek) ili automatskim postupkom (npr. grid search). B je preusko (hiperparametri nisu samo regularizacija), C miješa uzroke i posljedice, D nije točno (parametri ne moraju biti kontinuirani).

---

#### Pitanje 4: Model je skup funkcija H indeksiran parametrima θ. Što to znači?

| Odgovor | Opis |
|---------|------|
| **✅ A** | **Svaki θ jednoznačno određuje funkciju koja primjer x preslikava u oznaku y u ovisnosti o parametrima θ** |
| B | Svaki skup funkcija H ima svoj vektor parametara θ i svaki vektor parametara θ određuje skup funkcija H |
| C | Svaki x određuje parametar θ kojim se oznaka y preslikava u primjer x |
| D | Svaka funkcija koja primjeru x dodjeljuje oznaku y jednoznačno određuje točku θ u višedimenzijskome prostoru parametara |

> **Objašnjenje:** θ → h je preslikavanje: za zadani θ dobijemo jednu konkretnu hipotezu h koja za svaki x daje y. B miješa model i parametre, C je obrnuto, D govori o inverznom preslikavanju (h → θ) koje ne mora biti jednoznačno.

---

#### Pitanje 5: Za h kažemo da je definirana "do na parametre θ". Što to znači?

| Odgovor | Opis |
|---------|------|
| A | Funkcija h jednoznačno određuje parametre θ iz skupa svih mogućih parametara, koji nazivamo prostor parametara |
| B | Svaka vrijednost parametara θ daje jednu konkretnu funkciju h koja se razlikuje od svih drugih funkcija u modelu H |
| C | Funkcija h definirana je bez parametara, i njih treba odrediti naknadno postupkom odabira modela H |
| **✅ D** | **Različite vrijednosti za θ mogu dati različite funkcije h, a skup svih takvih različitih funkcija definira model H** |

> **Objašnjenje:** "Do na parametre" znači da je oblik funkcije zadan, ali konkretno ponašanje ovisi o θ. Npr. h(x) = θ₁x + θ₀ definira oblik (pravac), ali tek kad fiksiramo θ₀ i θ₁ dobijemo konkretnu funkciju. Skup svih takvih funkcija (za sve moguće θ) čini model H. A je obrnuto (h ne određuje θ jednoznačno), B je gotovo isto ali D je precizniji, C je netočno.

---

#### Pitanje 6: Zašto strojno učenje bez induktivne pristranosti nije moguće?

| Odgovor | Opis |
|---------|------|
| A | Model bi bio prejednostavan te ne bi postojala hipoteza s empirijskom pogreškom nula |
| B | Primjeri ne bi nužno bili linearno odvojivi |
| **✅ C** | **Oznaka niti jednog neviđenog primjera ne bi bila jednoznačno određena** |
| D | Prostor parametara bio bi neograničen, tj. postojalo bi beskonačno mnogo vektora parametara |

> **Objašnjenje:** Bez induktivne pristranosti (bez pretpostavki o obliku h), za svaki skup za učenje postoji **beskonačno mnogo** hipoteza koje savršeno klasificiraju trening podatke ali se **razlikuju na neviđenim primjerima**. Bez pretpostavki, nemamo osnovu za odabir između tih hipoteza, pa ne možemo predvidjeti oznaku neviđenog primjera.

---

#### Pitanje 7: Zašto šum u podatcima za učenje može dovesti do prenaučenosti klasifikacijskog modela?

| Odgovor | Opis |
|---------|------|
| A | Zbog šuma granica između klasa izgleda nelinearnijom nego što ona to zapravo jest, pa primjeri blizu granice znatno više doprinose pogrešci učenja nego primjeri koji su udaljeni od granice |
| **✅ B** | **Efekt šuma je slučajan, pa će hipoteza koja se previše prilagodi šumu na skupu za učenje očekivano imati veliku pogrešku na ispitnom skupu gdje je šum drugačiji ili ga nema** |
| C | Povećanjem količine šuma granica između klasa postaje sve nelinearnija, pa raste i složenost modela te dobivena hipoteza očekivano neće odgovarati granici između klasa na ispitnom skupu |
| D | Zbog šuma su oznake nekih primjera u skupu za učenje pogrešne, pa sve hipoteze iz modela imaju na tom skupu pogrešku koja je veća od nula, a još veća na ispitnom skupu |

> **Objašnjenje:** Šum je **stohastičke prirode** - slučajan je i različit u svakom uzorku. Presložen model prilagodi se konkretnom šumu u D_train. Na D_test šum je drugačiji → hipoteza griješi. A i C govore o nelinearnosti granice što je posljedica a ne uzrok. D nije točno jer ne moraju sve hipoteze imati pogrešku > 0.

---

#### Pitanje 8: Što je induktivna pristranost?

| Odgovor | Opis |
|---------|------|
| A | Kriterij koji, na temelju modela, jednoznačno određuje hipotezu s minimalnom empirijskom pogreškom |
| B | Svaka pretpostavka koja jednoznačno određuje model na temelju hipoteze i skupa za učenje |
| C | Odstupanje procjene parametra na temelju podataka u odnosu na pravu vrijednost parametra u populaciji |
| **✅ D** | **Minimalan skup pretpostavki koje, uz skup za učenje, jednoznačno određuju klasifikaciju svakog primjera** |

> **Objašnjenje:** Induktivna pristranost (inductive bias) su pretpostavke koje algoritam SU koristi da bi mogao generalizirati. Npr. pretpostavka da je granica između klasa linearna. Bez tih pretpostavki, sam D_train nije dovoljan da se odredi klasifikacija neviđenih primjera (vidi pitanje 6). A opisuje optimizacijski postupak, B je obrnuto, C opisuje statističku pristranost procjenitelja.

---

#### Pitanje 9: Model H je skup hipoteza h(·; θ) indeksiranih vektorom parametara θ ∈ R^(n+1). Može li skup H biti beskonačan?

| Odgovor | Opis |
|---------|------|
| **✅ A** | **Da, primjerice ako je X = R^n i h(x; θ) = θ^T x** |
| B | Ne, jer je skup primjera D uvijek konačan, neovisno o dimenzionalnosti ulaznog prostora n |
| C | Da, primjerice ako je X = {0,1}^n i h(x; θ) = 1{θ^T x ≥ 0} |
| D | Ne, jer za beskonačan skup H optimizacijski problem argmax E(h|D) nije definiran |

> **Objašnjenje:** Ako je θ ∈ R^(n+1), postoji **beskonačno mnogo** mogućih vektora θ (jer R je beskonačan skup). Svaki θ daje drugačiju hipotezu h(x) = θ^T x, pa je H beskonačan. B je netočno (konačnost D ne ograničava H), C - za X = {0,1}^n indikatorska funkcija daje konačno mnogo različitih klasifikacija, D je netočno (argmin je definiran i za beskonačne skupove).

---

### 🧮 Napomene za problemske zadatke (Cjelina 2)

#### Zadatak tip 1: Linearni klasifikator nad X = {0,1}^n

- Hipoteza: h(x; θ) = 1{θ₀ + θ₁x₁ + ... + θₙxₙ ≥ 0}
- **Dimenzija prostora parametara** = n + 1 (jedan θ za svaku značajku + θ₀)
- Za n = 3 → 4 parametra
- **Broj hipoteza |H|** ≠ beskonačno! Prostor ulaza je **konačan** ({0,1}^n ima 2^n točaka), pa razne θ daju **iste** klasifikacije
- Treba prebrojiti koliko **različitih klasifikacija** linearna granica može napraviti nad 2^n binarnih točaka

#### Zadatak tip 2: Box klasifikator nad X = {0,1}^n

- Pravokutnik u prostoru značajki - primjer je pozitivan ako je unutar "kutije"
- Za svaku značajku xⱼ biramo interval [aⱼ, bⱼ] gdje su aⱼ, bⱼ ∈ {0, 1}
- Mogućnosti za svaku dimenziju: prazan, {0}, {1}, {0,1} → treba pažljivo prebrojiti
- |H| = umnožak broja mogućnosti po dimenzijama (+ eventualno prazna hipoteza)

#### Zadatak tip 3: Prebrojavanje hipoteza s E(h|D) = 0

- Za zadani skup D, prebrojiti koliko hipoteza iz modela H ima empirijsku pogrešku nula
- Postupak: za svaku hipotezu (ili sustavno) provjeriti poklapa li se s oznakama svih primjera u D
- Trik: razmisli koje značajke/parametri su **ograničeni** danim primjerima, a koji ostaju slobodni

#### Zadatak tip 4: Usporedba modela (Ha vs Hb = ha · ha)

- Ako je Hb definiran kao **produkt** dviju hipoteza iz Ha → Hb je složeniji model
- Vrijedi: Ha ⊆ Hb (svaki ha se može dobiti kao ha · 1)
- Zato: min E(h|D) za Hb ≤ min E(h|D) za Ha (složeniji model može postići manju ili jednaku pogrešku na treningu)
- Ali: složeniji model ne znači nužno bolju generalizaciju!

#### Zadatak tip 5: Odnosi između modela (podskupovi)

- Ako je H₁ ⊆ H₂, tada svaka hipoteza iz H₁ postoji i u H₂
- Posljedica: minimalna empirijska pogreška na H₂ ≤ ona na H₁
- Treba prepoznati kad je jedan model **podskup** drugog (npr. linearni je podskup kvadratnog)
- Pazi: H₁ ⊆ H₂ **ne znači** da je H₁ bolji ili lošiji za generalizaciju

#### Zadatak tip 6: Klasifikacija linearnim modelom + induktivna pristranost

- Za zadane primjere odrediti parametre θ koji daju E(h|D) = 0
- Induktivna pristranost = pretpostavka o obliku hipoteze (npr. da je granica linearna)
- Pitanje je uvijek: kako model klasificira **neviđene** primjere - to određuje induktivna pristranost, ne sami podatci

#### Zadatak tip 7-8: Asimetrična funkcija gubitka

- Standardni gubitak 0-1: L = 1{h(x) ≠ y} → svaka pogreška košta jednako
- **Asimetrični gubitak:** FP i FN imaju **različite** cijene (npr. u medicini: propustiti bolest je skuplje od lažnog alarma)
- L(y, ŷ) može biti npr. L(1,0) = c₁ i L(0,1) = c₂ gdje c₁ ≠ c₂
- Min empirijska pogreška: hipoteza koja sve klasificira kao klasu s manjom "cijenom pogreške"
- Max empirijska pogreška: hipoteza koja sve klasificira kao klasu s većom "cijenom pogreške"

#### Zadatak tip 9: Usporedba minimalnih empirijskih pogrešaka

- Ako je H₁ ⊆ H₂ ⊆ ... → E₁* ≥ E₂* ≥ ...
- Ako modeli **nisu** u odnosu podskupa, poredak pogrešaka ovisi o konkretnim podatcima
- Ključno: **sposobnost modela da se prilagodi podatcima** raste s kompleksnošću

#### Zadatak tip 10: Model + preslikavanje značajki (feature mapping)

- Preslikavanje ϕ transformira ulazni prostor: x → ϕ(x)
- Model radi u **transformiranom** prostoru: h(ϕ(x); θ)
- Različite kombinacije (model, ϕ) mogu dati različit broj hipoteza s E(h|D) = 0
- Trik: primijeni ϕ na sve primjere, pa provjeri koji model u novom prostoru ima točno jednu hipotezu s nula pogreškom

---

## Cjelina 3: Linearna regresija

### 1. Uvod u regresiju

**Regresija** = predviđanje numeričkih vrijednosti (Y = R)

- Oznake y su realni brojevi (npr. cijena nekretnine)
- Hipoteza h : R^n → R preslikava primjere u brojčane vrijednosti

**Terminologija:**

| Pojam | Sinonimi |
|-------|---------|
| **Ulazne varijable** x | Nezavisne varijable, prediktorske varijable, kovarijati |
| **Izlazna varijabla** y | Zavisna varijabla, kriterijska varijabla |

> **Razlika statistika vs SU:** U statistici regresija služi za **objašnjavanje** odnosa među varijablama. U strojnom učenju nas zanima prije svega **predviđanje**.

---

### 2. Model linearne regresije

Izlaz je **linearna kombinacija** ulaznih varijabli:

$$h(x; w) = w_0 + w_1 x_1 + w_2 x_2 + \cdots + w_n x_n$$

- Parametri w₀, ..., wₙ nazivaju se **težine** (u statistici: regresijski koeficijenti, beta-koeficijenti)
- w₀ = **slobodni član** (intercept/bias)

#### Jednostavna regresija (n = 1)

$$h(x; w_0, w_1) = w_0 + w_1 x$$

- Hipoteza opisuje **pravac**
- Samo jedna ulazna varijabla

#### Višestruka regresija (n > 1)

- Za n = 2: hipoteza opisuje **ravninu**
- Za n > 2: hipoteza opisuje **hiperravninu**

#### Matrični zapis (s dummy značajkom)

Dodajemo dummy značajku x₀ = 1 svakom primjeru, pa model postaje:

$$h(x; w) = w^T x$$

gdje je w^T x skalarni produkt vektora w i x.

---

### 3. Vrste regresije

| | Jedan izlaz (y) | Više izlaza (y) |
|---|---|---|
| **Jedan ulaz (x)** | (Univarijatna) jednostavna | Multivarijatna jednostavna |
| **Više ulaza (x)** | (Univarijatna) višestruka | Multivarijatna višestruka |

- **Prema broju ulaza:** jednostavna (n=1) vs višestruka (n>1)
- **Prema broju izlaza:** univarijatna (y skalar) vs multivarijatna (y vektor)
- Podrazumijeva se univarijatna; fokus kolegija je na **univarijatnoj višestrukoj regresiji**

---

### 4. Tri komponente algoritma linearne regresije

#### Komponenta 1: Model

$$h(x; w) = w^T x$$

(uz dummy značajku x₀ = 1)

#### Komponenta 2: Funkcija gubitka i pogreška

**Kvadratni gubitak** (quadratic loss):

$$L(y, h(x)) = (y - h(x))^2$$

- Razlika y - h(x) naziva se **rezidual**
- Gubitak = kvadrat reziduala

**Zašto kvadrat, a ne apsolutna vrijednost?**
- Apsolutna vrijednost **nije derivabilna** (u nuli)
- Kvadratna funkcija **jest derivabilna** → možemo optimizirati
- Postoji i dublje probabilističko opravdanje (vidi sekciju 7)

**Funkcija kvadratne pogreške:**

$$E(h|D) = \frac{1}{2} \sum_{i=1}^{N} (y^{(i)} - h(x^{(i)}))^2$$

> **Napomena:** Umjesto 1/N koristimo **1/2** radi matematičke jednostavnosti pri deriviranju. Minimizator ostaje isti jer konstanta ne utječe na argmin.

#### Komponenta 3: Optimizacijski postupak

$$w^* = \arg\min_w E(w|D)$$

Kod linearne regresije s kvadratnim gubitkom, ovo se naziva **postupak najmanjih kvadrata** (Ordinary Least Squares, OLS).

---

### 5. Egzaktno rješenje vs rješenje najmanjih kvadrata

#### Egzaktno rješenje (krivi put)

Idealno bismo htjeli: h(x^(i)) = y^(i) za sve primjere, tj. sustav Xw = y.

**Problemi:**
- Sustav može biti **preodređen** (N > n+1) → nema rješenja (šum!)
- Sustav može biti **pododređen** (N < n+1) → beskonačno mnogo rješenja
- Rang matrice X mora biti n+1 za jedinstveno rješenje
- U praksi: šum u podatcima čini sustav nekonzistentnim

| Situacija | Rang X = Rang X\|y = n+1 | Rezultat |
|-----------|--------------------------|----------|
| N = n+1 | Da | Jedinstveno rješenje |
| N > n+1 | Obično ne | Nekonzistentan sustav |
| N < n+1 | Ne (rang < n+1) | Beskonačno rješenja |

> **Zaključak:** Egzaktno rješenje pretpostavlja savršen svijet bez šuma. U praksi tražimo **približno** rješenje.

#### Rješenje najmanjih kvadrata (pravi put)

Umjesto egzaktnog rješenja, minimiziramo kvadratna odstupanja.

**Funkcija pogreške u matričnom obliku:**

$$E(w|D) = \frac{1}{2}(Xw - y)^T(Xw - y)$$

**Raspisivanje:**

$$E(w|D) = \frac{1}{2}(w^T X^T X w - 2y^T X w + y^T y)$$

> **Ključni korak:** Srednja dva člana (w^T X^T y i y^T Xw) su jednaki jer su skalari, pa se transponiranjem jednog dobiva drugi.

**Deriviranje i izjednačavanje s nulom:**

$$\nabla_w E = w^T(X^T X) - y^T X = 0$$

**Normalne jednadžbe:**

$$X^T X w = X^T y$$

**Rješenje:**

$$w = (X^T X)^{-1} X^T y = X^+ y$$

---

### 6. Pseudoinverz i računalni aspekti

#### Pseudoinverz (Moore-Penroseov inverz)

$$X^+ = (X^T X)^{-1} X^T$$

- **Pooopćenje** inverza matrice - postoji za **svaku** matricu
- Ako je X kvadratna i punog ranga: X⁺ = X⁻¹
- Daje rješenje koje minimizira ||Xw - y||₂ (L2-normu)
- Ako postoji više rješenja, daje ono s **najmanjom normom** ||w||₂

#### Gramova matrica

$$G = X^T X$$

- Dimenzije: (n+1) × (n+1)
- Složenost invertiranja: **O(n³)**
- Na složenost utječe **samo broj značajki n**, ne broj primjera N!
- Rang Gramove matrice = rang matrice dizajna X
- Ako rang(X) < n+1 → koristimo **SVD** za pseudoinverz

#### Rješenje u zatvorenoj formi (closed form)

- Rješenje je dano **formulom** (ne iterativnim postupkom)
- Izračunljivo u konačnom broju koraka
- Vrlo poželjno u SU jer je optimizacija egzaktna i jednostavna

---

### 7. Probabilistička interpretacija regresije ⚠️

#### Model šuma

Pretpostavljamo da su oznake generirane nekom funkcijom f plus šum:

$$y^{(i)} = f(x^{(i)}) + \varepsilon_i$$

gdje je šum normalno distribuiran:

$$\varepsilon \sim N(0, \sigma^2)$$

#### Vjerojatnost oznaka (likelihood)

Za zadani x, oznaka y distribuirana je kao:

$$p(y|x) = N(f(x), \sigma^2)$$

Uz IID pretpostavku, vjerojatnost cijelog skupa oznaka:

$$p(y|X) = \prod_{i=1}^{N} p(y^{(i)}|x^{(i)})$$

#### Maksimizacija vjerojatnosti (Maximum Likelihood)

Zamjenjujemo f(x) s h(x; w) i prelazimo u log-domenu:

$$\ln p(y|w) = -N\ln(\sqrt{2\pi}\sigma) - \frac{1}{2\sigma^2} \sum_{i=1}^{N} (y^{(i)} - h(x^{(i)}; w))^2$$

- Prvi član je **konstanta** (ne ovisi o w)
- Maksimizacija log-vjerojatnosti → **minimizacija** sume kvadrata

> **Ključan zaključak:** Uz pretpostavku normalno distribuiranog šuma, **maksimizacija vjerojatnosti podataka** ekvivalentna je **minimizaciji kvadratne pogreške**. To je probabilističko opravdanje za kvadratni gubitak!

#### IID pretpostavka

- **Independently and Identically Distributed** (nezavisno i identično distribuirane varijable)
- Oznake primjera su međusobno nezavisne i dolaze iz iste distribucije
- Zato je ukupna vjerojatnost = **umnožak** pojedinačnih vjerojatnosti

---

### 8. Ključni pojmovi - sažetak (Cjelina 3)

| Pojam | Definicija |
|-------|-----------|
| **Linearna regresija** | Model gdje je izlaz linearna kombinacija ulaznih varijabli |
| **Težine** w | Parametri linearnog modela (regresijski koeficijenti) |
| **Dummy značajka** | x₀ = 1, dodaje se da bi se w₀ jednako tretirao |
| **Kvadratni gubitak** | L = (y - h(x))² |
| **Rezidual** | y - h(x), odstupanje stvarne od predviđene vrijednosti |
| **OLS** | Ordinary Least Squares - postupak najmanjih kvadrata |
| **Normalne jednadžbe** | X^T X w = X^T y |
| **Pseudoinverz** X⁺ | (X^T X)⁻¹ X^T - daje rješenje najmanjih kvadrata |
| **Gramova matrica** | X^T X, dimenzija (n+1)×(n+1) |
| **Zatvorena forma** | Rješenje dano formulom, izračunljivo u konačnom broju koraka |
| **IID** | Nezavisno i identično distribuirane varijable |
| **Maximum Likelihood** | Princip: traži parametre koji maksimiziraju vjerojatnost podataka |

---

### 📝 Teorijska ispitna pitanja (Cjelina 3)

#### Pitanje 1: Kako glasi induktivna pristranost preferencije (neregulariziranog) modela linearne regresije?

| Odgovor | Opis |
|---------|------|
| A | Hipoteza h je linearna kombinacija težina w i značajki x |
| B | Težine w maksimiziraju iznos \|\|Xw - y\|\|² |
| **✅ C** | **Težine w minimiziraju iznos \|\|Xw - y\|\|²** |
| D | Hipoteza h je funkcija iz R^n u R |

> **Objašnjenje:** Induktivna pristranost ima dva dijela: **pristranost jezika** (oblik modela - to je A i D) i **pristranost preferencije** (kako biramo hipotezu). Pristranost preferencije linearne regresije je da biramo težine koje **minimiziraju** kvadratno odstupanje. B je obrnuto (maksimizira umjesto minimizira).

---

#### Pitanje 2: Rješenje najmanjih kvadrata je w = (X^TX)^{-1} X^T y. Pod kojim uvjetima ćemo težine moći izračunati na ovaj način, i o čemu dominantno ovisi složenost?

| Odgovor | Opis |
|---------|------|
| A | Ako je rang matrice X jednak N+1, složenost dominantno ovisi o N |
| B | Ako je rang matrice X^TX jednak N, složenost dominantno ovisi o n |
| **✅ C** | **Ako je rang matrice X jednak n+1, složenost dominantno ovisi o n** |
| D | Ako je matrica X^TX kvadratna i punog ranga, složenost dominantno ovisi o N |

> **Objašnjenje:** Da bi X^TX bila invertibilna, matrica X mora imati rang n+1 (puni rang stupaca). Gramova matrica X^TX je dimenzije (n+1)×(n+1), pa složenost invertiranja je **O(n³)** - ovisi o broju značajki n, ne o broju primjera N. D je netočan jer X^TX je **uvijek** kvadratna, a složenost ne ovisi o N.

---

#### Pitanje 3: Koja je razlika između induktivnih pristranosti regularizirane i nereguliarizirane linearne regresije?

| Odgovor | Opis |
|---------|------|
| A | Algoritmi imaju različite pristranosti, jer je model neregularizirane regresije nadskup modela regularizirane regresije |
| **✅ B** | **Oba algoritma imaju isti model (linearnu kombinaciju značajki i težina), dakle istu pristranost jezika, ali se razlikuju u pristranosti preferencije jer imaju različito definiranu empirijsku pogrešku (osim ako je regularizacijski faktor jednak nuli)** |
| C | Algoritmi se ne razlikuju po pristranosti preferencijom budući da koriste istu funkciju gubitka, međutim regularizirana regresija ima jaču induktivnu pristranost jezika |
| D | Regulariziirana regresija preferira jednostavnije hipoteze, međutim pristranosti su im identične jer su oba algoritma definirana kao linearna kombinacija |

> **Objašnjenje:** Model je isti (h = w^Tx), pa je **pristranost jezika identična**. Razlika je u funkciji pogreške: regularizirana dodaje λ||w||², pa je **pristranost preferencije različita** - regularizirana preferira manje težine. A je netočan jer modeli su isti (isti skup hipoteza). C i D miješaju pojmove.

---

#### Pitanje 4: Kako formalno glasi probabilistička pretpostavka modela linearne regresije?

| Odgovor | Opis |
|---------|------|
| A | p(x\|y) = N(f(x), σ²) |
| B | p(y\|x) = N(0, σ²) |
| **✅ C** | **p(y\|x) = N(h(x), σ²)** |
| D | p(y) = N(0, σ²) |

> **Objašnjenje:** Pretpostavka je da je oznaka y normalno distribuirana oko predviđanja hipoteze h(x), s varijancom σ². B je kriv jer srednja vrijednost nije 0 nego h(x). A ima obrnute varijable (x\|y umjesto y\|x). D nema uvjetovanje na x.

---

#### Pitanje 5: Što je induktivna pristranost preferencije linearnog modela regresije?

| Odgovor | Opis |
|---------|------|
| A | Pretpostavka P(y\|w) = ∏P(y^(i)\|w) |
| **✅ B** | **Minimizacija iznosa \|\|Xw - y\|\|₂** |
| C | Odabir linearnog modela h(w; y) = w^Tx |
| D | Maksimizacija iznosa -ln L(w\|y) |

> **Objašnjenje:** Isto kao pitanje 1 ali drugačije formulirano. **Pristranost preferencije** = kako biramo hipotezu = minimizacija L2 norme odstupanja. C je pristranost **jezika** (oblik modela). A je IID pretpostavka. D je ekvivalentno ali neprecizno formulirano.

---

#### Pitanje 6: Koliko redaka odnosno stupaca ima matrica koju invertiramo kod L2-regularizirane regresije u prostoru značajki?

| Odgovor | Opis |
|---------|------|
| **✅ A** | **m + 1** |
| B | m + λ |
| C | n + λ |
| D | N |

> **Objašnjenje:** Kod regresije u prostoru značajki, matrica dizajna Φ ima m+1 stupaca (m značajki + dummy). Gramova matrica Φ^TΦ je dimenzije **(m+1) × (m+1)**, pa invertiramo matricu veličine m+1. Gdje je m broj značajki u prostoru značajki (ne n iz ulaznog prostora). λ je regularizacijski faktor i nema veze s dimenzijom matrice.

---

#### Pitanje 7: U kojoj situaciji je rješenje dobiveno pseudoinverzom identično rješenju dobivenom običnim inverzom?

| Odgovor | Opis |
|---------|------|
| A | Kada je broj primjera veći od broja značajki |
| **✅ B** | **Kada je broj primjera jednak broju značajki plus jedan i nema multikolinearnosti** |
| C | Kada je broj značajki manji od broja primjera i nema multikolinearnosti |
| D | Kada nema multikolinearnosti i matrica dizajna je dobro kondicionirana |

> **Objašnjenje:** Pseudoinverz X⁺ = X⁻¹ samo kada je X **kvadratna** i **punog ranga**. Matrica X je N × (n+1), pa je kvadratna kada je N = n+1. Punog ranga je kada nema multikolinearnosti. A i C ne zahtijevaju kvadratnost. D ne zahtijeva kvadratnost eksplicitno.

---

#### Pitanje 8: Pod kojim uvjetom vrijedi korespondencija minimizacije kvadratne pogreške i maksimizacije log-izglednosti?

| Odgovor | Opis |
|---------|------|
| A | Primjeri (x, y) u skupu D nezavisno su uzorkovani iz zajedničke distribucije P(x, y) |
| B | Funkcija pogreške E(w\|D) je neprekidna i unimodalna |
| C | Matrica dizajna X nije singularna ili je regularizacijski faktor λ veći od 0 |
| **✅ D** | **Oznaka y primjera (x, y) je normalna varijabla sa srednjom vrijednošću w^Tx** |

> **Objašnjenje:** Korespondencija OLS ↔ MLE vrijedi uz pretpostavku da je **šum normalno distribuiran**, tj. y ~ N(w^Tx, σ²). Upravo ta pretpostavka dovodi do toga da log-izglednost sadrži sumu kvadrata odstupanja. A (IID) je potreban ali nedovoljan uvjet. B i C nisu relevantni za ovu korespondenciju.

---

### 🧮 Napomene za problemske zadatke (Cjelina 3)

#### Zadatak tip 1: Matrični zapis funkcije kvadratne pogreške

- Polazi se od E(w|D) = 1/2 Σ(w^T x^(i) - y^(i))²
- Matrični oblik: E = 1/2 (Xw - y)^T (Xw - y)
- Nakon raspisivanja: **1/2 (w^T X^T Xw - 2y^T Xw + y^T y)**
- Ključno: srednja dva člana su jednaki (skalari!) pa se spajaju u -2y^T Xw
- Pazi na redoslijed matrica i transpozicije - dimenzije moraju biti konzistentne

#### Zadatak tip 2: Pogrešno definirana funkcija gubitka (y + h(x))²

- Ako je gubitak L = (y + h(x))² umjesto (y - h(x))², OLS minimizira sumu (y^(i) + w^T x^(i))²
- To znači da model traži hipotezu za koju je w^T x ≈ **-y** (umjesto y)
- Ako bi s ispravnim gubitkom rješenje bilo (w₀, w₁), s pogrešnim gubitkom očekujemo **(-w₀, -w₁)**
- Provjera: ako su oznake iz N(-1 + 2x, σ²), ispravni OLS daje (w₀, w₁) ≈ (-1, 2), pa pogrešni daje **(1, -2)**

#### Zadatak tip 3: Gubici po pojedinim primjerima nakon OLS

- Izračunaj w = (X^T X)^{-1} X^T y za zadani skup D
- Za svaki primjer izračunaj predikciju h(x^(i)) = w^T x^(i)
- Gubitak: L^i = (y^(i) - h(x^(i)))²
- Primjeri koji leže bliže regresijskoj hiperravnini imaju manji gubitak
- Pazi: dummy značajka x₀ = 1 mora biti uključena u matricu dizajna!

#### Zadatak tip 4: Izračun log-izglednosti ln L(w|Φ, y)

- Log-izglednost: ln L(w|Φ, y) = -N ln(√(2π)σ) - 1/(2σ²) Σ(y^(i) - w^T ϕ(x^(i)))²
- Ako je σ² = 1: ln L = -N ln(√(2π)) - 1/2 Σ(y^(i) - w^T ϕ(x^(i)))²
- Postupak: za svaki primjer izračunaj w^T ϕ(x^(i)), pa rezidual y^(i) - w^T ϕ(x^(i)), pa kvadriraj
- Konstantni dio: -N ln(√(2π)) ≈ -N · 0.9189
- Ne zaboravi primijeniti preslikavanje ϕ na primjere **prije** množenja s w

---

## Cjelina 4: Linearna regresija II

### 1. Nelinearna regresija

Često je veza između ulaznih i izlazne varijable **nelinearna**. Linearni model to ne može uhvatiti.

**Rješenje:** Koristiti polinomijalne ili druge nelinearne modele.

#### Primjeri nelinearnih modela

**Jednostruka polinomijalna regresija (n=1):**

h(x; w) = w₀ + w₁x + w₂x² + ... + w_d x^d

- d = stupanj polinoma (hiperparametar)
- H₁ ⊂ H₂ ⊂ ... (linearni model je podskup kvadratnog itd.)

**Višestruka polinomijalna regresija (n=2, d=2):**

h(x; w) = w₀ + w₁x₁ + w₂x₂ + w₃x₁x₂ + w₄x₁² + w₅x₂²

- **Interakcijska značajka** x₁x₂ (cross-term) - modelira interakciju između varijabli
- Osim kvadratnih, mogu se dodati i viši stupnjevi

---

### 2. Preslikavanje u prostor značajki (Feature Mapping) ⚠️

Ključna ideja: **umjesto da mijenjamo model, mijenjamo podatke!**

Preslikavamo primjere iz ulaznog prostora (n dim.) u prostor značajki (m dim., tipično m > n):

$$\phi : \mathbb{R}^n \rightarrow \mathbb{R}^{m+1}$$
$$\phi(x) = (\phi_0(x), \phi_1(x), \ldots, \phi_m(x))$$

gdje je φ₀(x) = 1 (dummy značajka).

**Model u prostoru značajki:**

$$h(x; w) = w^T \phi(x) = \sum_{j=0}^{m} w_j \phi_j(x)$$

> **Ključno:** Model je **linearan u parametrima** w, ali može biti **nelinearan u izvornim značajkama** x! Ovo se zove **model linearne regresije** (ne isto što i linearna regresija).

#### Konkretne funkcije preslikavanja

| Tip | φ(x) | Dimenzije |
|-----|-------|-----------|
| Linearna višestruka | (1, x₁, x₂, ..., xₙ) | m = n |
| Jednostruka polinomijalna (n=1) | (1, x, x², ..., x^d) | m = d |
| Višestruka polinomijalna (n=2, d=2) | (1, x₁, x₂, x₁x₂, x₁², x₂²) | m = 5 |

> **Napomena:** Linearna regresija = poseban slučaj modela linearne regresije gdje je φ(x) = (1, x) (identitetno preslikavanje).

---

### 3. Optimizacija s preslikavanjem

Optimizacija je **identična** kao kod linearne regresije, samo zamjenjujemo X s Φ:

**Matrica dizajna u prostoru značajki:**

$$\Phi = \begin{pmatrix} \phi(x^{(1)})^T \\ \phi(x^{(2)})^T \\ \vdots \\ \phi(x^{(N)})^T \end{pmatrix}_{N \times (m+1)}$$

**Rješenje:**

$$w = (\Phi^T \Phi)^{-1} \Phi^T y = \Phi^+ y$$

Jedina razlika: dimenzija Gramove matrice sada je **(m+1) × (m+1)** umjesto (n+1) × (n+1).

---

### 4. Prenauučenost i načini sprječavanja

Stupanj polinoma d (ili općenito odabir φ) je **hiperparametar** koji određuje složenost modela.

#### Načini sprječavanja prenauučenosti

| Tehnika | Opis | Napomena |
|---------|------|----------|
| **Više primjera** | Više podataka → teže se prenauučiti | Često nije izvedivo |
| **Unakrsna provjera** | Odabir hiperparametra d na ispitnom skupu | Razdvaja odabir modela od učenja |
| **Odabir značajki** | Izbaciti beskorisne značajke | Feature selection |
| **Redukcija dimenzionalnosti** | Preslikati u prostor niže dimenzije | Nove značajke ≠ izvorne |
| **Regularizacija** | Kažnjavati složenost modela pri optimizaciji | Spaja odabir i učenje modela |
| **Bayesovska regresija** | Apriorne distribucije nad parametrima | Izvan opsega kolegija |

---

### 5. Regularizacija ⚠️

**Opaažanje:** Što je model složeniji, to su **veće magnitude težina** w.

**Ideja:** Kažnjavati hipoteze s velikim težinama → smanjiti efektivnu složenost modela.

**Regularizirana funkcija pogreške:**

$$E_R(w|D) = E(w|D) + \lambda \Omega(w)$$

- Ω(w) = **regularizacijski izraz** (funkcija težina)
- λ = **regularizacijski faktor** (hiperparametar)
- λ = 0 → neregularizirana pogreška
- Veći λ → jače kažnjavanje → jednostavniji model

> **Važno:** Težina w₀ se **NE regularizira** (jer ona određuje odsječak, ne složenost modela).

#### Tri vrste regularizacije

| Tip | Ω(w) | Svojstva |
|-----|-------|----------|
| **L2 (Ridge)** | \|\|w\|\|₂² = Σwⱼ² | Zatvorena forma, ne daje rijetke modele |
| **L1 (LASSO)** | \|\|w\|\|₁ = Σ\|wⱼ\| | Daje rijetke modele, nema zatvorenu formu |
| **L0** | Σ1{wⱼ ≠ 0} = broj ne-nul težina | Odabir značajki, NP-potpun problem |

#### Usporedba L1 vs L2

- **L2** kažnjava proporcionalno kvadratu magnitude → velike težine kažnjava jako, male jedva → teško pritegne na **točno** nulu
- **L1** kažnjava proporcionalno apsolutnoj vrijednosti → male težine kažnjava relativno više → lakše ih pritegne na **točno** nulu → **rijetki modeli** (sparse)

**Geometrijska interpretacija:**
- L2 izokonture = kružnica (hipersfera) → minimum rijetko pada na os
- L1 izokonture = kvadrat (hiperoktaedar) s **vrhovima na osima** → minimum češće pada na os (= nula za neke težine)

#### Preferancija regularizacije

L0 > L1 > L2 (po rjetkosti modela), ali:
- L0: NP-potpun, nepraktično
- L1: traktabilno, ali nema zatvorenu formu (iterativna optimizacija)
- **L2: jedino s rješenjem u zatvorenoj formi** → najčešće se koristi

---

### 6. Hrbatna regresija (Ridge Regression)

L2-regularizirana regresija (Tikhonovljeva regularizacija):

$$E_R(w|D) = \frac{1}{2} \sum_{i=1}^{N} (w^T\phi(x^{(i)}) - y^{(i)})^2 + \frac{\lambda}{2} \|w\|_2^2$$

#### Izvod rješenja

Polazište (dodaje se λ/2 · w^T w):

$$E_R(w|D) = \frac{1}{2}(\Phi w - y)^T(\Phi w - y) + \frac{\lambda}{2} w^T w$$

Gradijent i izjednačavanje s nulom:

$$\nabla_w E_R = \Phi^T\Phi w - \Phi^T y + \lambda w = (\Phi^T\Phi + \lambda I)w - \Phi^T y = 0$$

**Rješenje:**

$$w = (\Phi^T\Phi + \lambda I)^{-1} \Phi^T y$$

> **Napomena:** λI je matrica s λ na dijagonali, ali **gornji lijevi element je 0** (jer w₀ ne regulariziramo), tj. λI = diag(0, λ, ..., λ).

---

### 7. Regularizacija i multikolinearnost

#### Multikolinearnost

**Multikolinearnost** = dvije ili više značajki su međusobno korelirane (jedna se može predvidjeti kao linearna kombinacija drugih).

**Posljedice:**
- Rang matrice Φ < m+1 → Gramova matrica singularna ili gotovo singularna
- Rješenje za w postaje **nestabilno** (male promjene u podatcima → velike promjene u težinama)
- Loše kondicionirana matrica → prenauučenost

**Kada se događa:** Posebno kad je m ≥ N (više značajki nego primjera) → matrica dizajna "široka i plitka"

#### Kako regularizacija rješava multikolinearnost

$$w = (\Phi^T\Phi + \lambda I)^{-1} \Phi^T y$$

- λI dodaje λ na dijagonalu Gramove matrice → **smanjuje kolinearnost stupaca**
- Veći λ → matrica bliža dijagonalnoj → **dalje od singularne** → stabilnije rješenje
- Regularizacija **rekondicionira** Gramovu matricu (smanjuje kondicijski broj)

**Geometrijska interpretacija:**
- Neregularizirana pogreška može imati "hrbat" (udolina u prostoru parametara) = beskonačno mnogo minimuma
- Regularizacija čini funkciju "konveksnijom" → jedan stabilan minimum

> **Odakle naziv "hrbatna regresija":** Ridge regression može raditi s "hrptovima" u funkciji pogreške.

---

### 8. Napomene o linearnom modelu regresije

- **Magnituda wᵢ** = važnost značajke; **predznak** = smjer utjecaja (pozitivan/negativan)
- Ali: ako je model prenauučen (multikolinearnost), magnituda **ne znači ništa**!
- Regularizacija smanjuje nelinearnost nelinearnog modela
- L2 teško pritegne težine na **točno** nulu → ne daje rijetke modele
- L1 lakše daje rijetke modele, ali nema zatvorenu formu
- λ se odabire **unakrsnom provjerom** (ne na skupu za učenje, jer bi uvijek bio λ = 0!)

---

### 9. Ključni pojmovi - sažetak (Cjelina 4)

| Pojam | Definicija |
|-------|-----------|
| **Prostor značajki** | Prostor u koji preslikavamo primjere baznim funkcijama φ |
| **Bazne funkcije** φⱼ | Nelinearne funkcije koje definiraju preslikavanje |
| **Model linearne regresije** | Linearan u parametrima, ali može biti nelinearan u značajkama |
| **Interakcijska značajka** | Cross-term, npr. x₁x₂, modelira interakciju varijabli |
| **Regularizacija** | Kažnjavanje složenosti modela dodavanjem Ω(w) u funkciju pogreške |
| **λ (regularizacijski faktor)** | Hiperparametar koji kontrolira jačinu regularizacije |
| **L2 / Ridge / Hrbatna** | Ω = \|\|w\|\|₂², ima zatvorenu formu, ne daje rijetke modele |
| **L1 / LASSO** | Ω = \|\|w\|\|₁, daje rijetke modele, nema zatvorenu formu |
| **L0** | Ω = broj ne-nul težina, NP-potpun |
| **Rijetki modeli** | Modeli s mnogo wⱼ = 0, poželjni u SU |
| **Multikolinearnost** | Korelirane značajke → nestabilno rješenje |
| **Kondicijski broj** | Mjera stabilnosti rješenja, velik = loše kondicionirana matrica |
| **Rekondicioniranje** | Dodavanje λI na Gramovu matricu → poboljšanje kondicije |

---

### 📝 Teorijska ispitna pitanja (Cjelina 4)

#### Pitanje 1: Rješenje hrbatne regresije je w = (X^TX + λI)^{-1} X^T y. Koji je efekt regularizacije na Gramovu matricu?

| Odgovor | Opis |
|---------|------|
| **✅ A** | **Dodavanje vrijednosti λ na dijagonale Gramove matrice povećava njezin rang** |
| B | Dodavanje vrijednosti λ na dijagonale Gramove matrice povećava normu težina \|w\| |
| C | Minimizacija norme težina \|w\| čini Gramovu matricu kvadratnom i singularnom |
| D | Minimizacija norme težina \|w\| povećava multikolinearnost Gramove matrice i smanjuje složenost modela |

> **Objašnjenje:** Ako je Gramova matrica bila singularna (rang < m+1), dodavanje λ na dijagonalu je čini **punog ranga** → invertibilnom. To je rekondicioniranje. B je obrnuto (regularizacija **smanjuje** normu). C i D su obrnuto (regularizacija **smanjuje** multikolinearnost i singularnost).

---

#### Pitanje 2: Na kojoj se činjenici temelji korištenje norme kao regularizacijskog izraza?

| Odgovor | Opis |
|---------|------|
| A | Ako su težine hipoteze velike magnitude, model je prenaučen |
| **✅ B** | **Ako je model prenaučen, hipoteza će imati velike magnitude težina** |
| C | Ako je model optimalne složenosti, hipoteza će imati male magnitude težina |
| D | Ako su težine hipoteze male magnitude, model je podnačen |

> **Objašnjenje:** Ključna razlika A vs B: **B** kaže da prenaučenost → velike težine (opažanje iz prakse), dok A kaže velike težine → prenaučenost (obrnuti smjer, nije nužno istinito). Regularizacija se temelji na opažanju da prenaučeni modeli imaju velike magnitude, pa kažnjavamo velike težine. C nije nužno istinito, D je netočno.

---

#### Pitanje 3: Što je prednost a što nedostatak L1-regularizacije?

| Odgovor | Opis |
|---------|------|
| A | Prednost: možemo minimizirati gradijentnim spustom. Nedostatak: rezultira rijetkim modelima |
| **✅ B** | **Prednost: izbacuje značajke iz modela. Nedostatak: L1-regularizirana pogreška nema minimizator u zatvorenoj formi** |
| C | Prednost: zadržava sve značajke u modelu. Nedostatak: Gramova matrica može biti blizu singularne |
| D | Prednost: postoji rješenje u zatvorenoj formi. Nedostatak: izračun ovisi o broju značajki i broju primjera |

> **Objašnjenje:** L1 **prednost** = daje rijetke modele (pritegne mnoge wⱼ na nulu = efektivno izbacuje značajke = feature selection). L1 **nedostatak** = nema rješenje u zatvorenoj formi, mora se koristiti iterativna optimizacija. A je krivo jer rijetki modeli su prednost a ne nedostatak. C opisuje L2. D opisuje OLS bez regularizacije.

---

#### Pitanje 4: Kako je definirana L2-regularizirana pogreška kod linearne regresije?

| Odgovor | Opis |
|---------|------|
| A | Zbroj očekivanja funkcije gubitka unakrsne entropije i druge norme vektora težina |
| B | Zbroj prosjeka kvadratnog gubitka na svim primjerima i kvadrata druge norme vektora težina bez težine w₀ |
| **✅ C** | **Zbroj neregularizirane pogreške i izraza propocionalnog s kvadratom norme vektora težina bez težine w₀** |
| D | Zbroj funkcije gubitka po svim primjerima i neregularizirane pogreške bez težine w₀ |

> **Objašnjenje:** E_R(w|D) = E(w|D) + λ/2 · ||w||₂². Dakle: neregularizirana pogreška + izraz **proporcionalan** s kvadratom L2 norme (faktor proporcionalnosti je λ/2). Ključno: w₀ je **izuzeta** iz regularizacije. A koristi krivi gubitak (unakrsna entropija je za klasifikaciju). B kaže "prosjek" ali koristimo 1/2 sumu, ne 1/N. D miješa pojmove.

---

#### Pitanje 5: Kakve parametre modela nalazi optimizacija L2-regularizirane pogreške?

| Odgovor | Opis |
|---------|------|
| A | Parametre koji uz što veću magnitudu daju što manje očekivanje gubitka na skupu za ispitivanje |
| **✅ B** | **Parametre koji uz što manju magnitudu daju što manje očekivanje gubitka na skupu za učenje** |
| C | Parametre koji uz što veću magnitudu daju što veće očekivanje gubitka na skupu za učenje |
| D | Parametre koji uz što manju magnitudu daju što veće očekivanje gubitka na skupu za ispitivanje |

> **Objašnjenje:** Regularizirana pogreška = empirijska pogreška (na skupu za **učenje**) + λ · norma. Minimiziramo oboje: **mala pogreška** (empirijska komponenta) + **male težine** (regularizacijska komponenta). To je kompromis. A želi velike magnitude (kontraproduktivno). C i D žele veliku pogrešku (besmisleno).

---

#### Pitanje 6: Koji je efekt savršene multikolinearnosti kod postupka OLS?

| Odgovor | Opis |
|---------|------|
| **✅ A** | **rang(Φ) < m+1, G nema puni rang i nema inverz, no ima pseudoinverz koji nije numerički stabilan** |
| B | Φ nema puni rang, rang(G) < m+1 i G nema pseudoinverz |
| C | Φ ima puni rang, rang(G) > m i G ima inverz, ali s visokim kondicijskim brojem |
| D | rang(Φ) = N, no rang(G) < N, pa G ima pseudoinverz, ali nema numerički stabilan inverz |

> **Objašnjenje:** Savršena multikolinearnost: stupci Φ su linearno zavisni → rang(Φ) < m+1 → rang(G) = rang(Φ) < m+1 → G je **singularna** (nema inverz). Pseudoinverz se može izračunati SVD-om, ali rješenje je **numerički nestabilno**. B je netočan jer pseudoinverz **uvijek** postoji. C je obrnuto (nema puni rang). D miješa dimenzije.

---

### 🧮 Napomene za problemske zadatke (Cjelina 4)

#### Zadatak tip 1: Izračun L1-regularizirane pogreške

- E_R(w|D) = E(w|D) + λ/2 · ||w||₁
- E(w|D) = 1/2 Σ(w^T x^(i) - y^(i))² → izračunaj predikciju za svaki primjer, pa rezidual, pa kvadriraj, pa zbroji
- ||w||₁ = Σ|wⱼ| (apsolutne vrijednosti svih težina **osim w₀**)
- Konačni rezultat: E_R = 1/2 · (suma kvadrata reziduala) + λ/2 · (suma apsolutnih vrijednosti težina bez w₀)
- Pazi: w₀ se NE uključuje u regularizacijski izraz!

#### Zadatak tip 2: Usporedba modela različite složenosti i regularizacije

- H_{d,λ} = polinom stupnja d s regularizacijskim faktorom λ
- Viši stupanj d → složeniji model → manja pogreška učenja, ali moguća prenauučenost
- Veći λ → jača regularizacija → efektivno jednostavniji model
- Ako podatci dolaze iz polinoma stupnja 3: modeli d < 3 su podnauučeni, d >> 3 bez regularizacije su prenauučeni
- Optimalan: model dovoljno složen (d ≥ 3) s umjerenom regularizacijom
- H₂ je uvijek podnauučen (ne može uhvatiti kubnu funkciju)
- H₅ s λ=0 može biti prenauučen ako je malo podataka, H₅ s umjerenim λ može dobro generalizirati

#### Zadatak tip 3: Minimalan broj primjera za stabilno rješenje

- Za rješenje bez regularizacije treba: rang(Φ) = m+1, a nužan uvjet je **N ≥ m+1**
- m+1 = ukupan broj značajki u prostoru značajki (uključujući dummy)
- Za polinomijalno preslikavanje s interakcijama, prebroji sve članove:
  - Linearni: n članovi
  - Kvadratni: n(n+1)/2 članovi (n kvadratnih + C(n,2) interakcijskih parova)
  - Interakcije trojki: C(n,3) članovi
  - + dummy (1)
- Ukupan m+1 = 1 + (linearni) + (kvadratni) + (interakcije trojki)
- Ne moramo koristiti sve značajke - zadatak specificira koje koristimo

---

## Cjelina 5: Linearni diskriminativni modeli

### 1. Uvod u klasifikaciju i linearne diskriminativne modele

**Klasifikacija** = predviđanje diskretnih oznaka primjera (npr. spam/ne-spam, pozitivan/negativan/neutralan sentiment)

**Linearni diskriminativni modeli** — familija modela s dva ključna svojstva:
- **Linearni:** modeliraju linearnu granicu između klasa (pravac, ravnina, hiperravnina)
- **Diskriminativni:** parametri opisuju **samo granicu** između klasa, ništa više

**Diskriminativni vs. generativni modeli:**

| Svojstvo | Diskriminativni | Generativni |
|----------|----------------|-------------|
| Što modeliraju | Samo granicu između klasa | Vjerojatnosne gustoće svake klase |
| Granica | Direktno opisana parametrima | Indirektno izvedena iz distribucija |
| Broj parametara | Manji | Veći |
| Primjeri | Logistička regresija, SVM, perceptron | Naivni Bayes, Gaussov generativni model |

---

### 2. Binarni linearni klasifikator

Polazimo od linearnog modela regresije $h(x; w) = w^T x$ i definiramo binarni klasifikator:

$$h(x; w) = \mathbf{1}\{w^T x \geq 0\}$$

- $\mathbf{1}\{\cdot\}$ je indikacijska funkcija
- Granica između klasa: $h(x) = 0$, tj. $w^T x = 0$
- Granica je **(n-1)-dimenzijska hiperravnina** u n-dimenzijskom ulaznom prostoru
  - n=2 → pravac, n=3 → ravnina, n>3 → hiperravnina

**Nelinearna granica** — koristi se nelinearno preslikavanje $\phi: \mathbb{R}^n \to \mathbb{R}^{m+1}$:

$$h(x; w) = w^T \phi(x)$$

- Granica je linearna u prostoru značajki, ali **nelinearna u ulaznom prostoru**
- Model je i dalje **linearan u parametrima** (tehnički linearan model)
- Primjer: XOR problem — preslikavanje $\phi(x) = (1, x_1, x_2, x_1 x_2)$ čini problem linearno odvojivim

---

### 3. Geometrija linearnog modela

Model s odvojenim biasom:

$$h(x; w_0, w) = w^T x + w_0$$

**Vektor težina w je normala hiperravnine:**
- Dokaz: za dva primjera $x^{(1)}, x^{(2)}$ na hiperravnini vrijedi $w^T(x^{(1)} - x^{(2)}) = 0$
- Razlika vektora leži na hiperravnini, a skalarni produkt s w je 0 → w je okomit na hiperravninu

**Predznačena udaljenost** primjera x od hiperravnine:

$$d = \frac{h(x)}{\|w\|}$$

- d > 0 → x je na strani u smjeru normale w (pozitivna strana)
- d < 0 → x je na suprotnoj strani
- d = 0 → x je točno na hiperravnini
- Udaljenost hiperravnine od ishodišta: $-w_0 / \|w\|$

**Skaliranje težina:** množenje $(w_0, w)$ s faktorom $\alpha$ ne mijenja hiperravninu — ista granica, isti smjer, iste udaljenosti (jer se normira s $\|w\|$). Beskonačno mnogo vektora težina definira istu hiperravninu.

---

### 4. Višeklasna klasifikacija

Mnogi linearni diskriminativni modeli su inherentno binarni → za K > 2 klasa koristimo dekompoziciju na binarne probleme.

#### Shema OVO (One-vs-One)

- Treniramo $\binom{K}{2}$ binarnih klasifikatora, po jedan za svaki par klasa
- Klasifikator $h_{ij}$ razlikuje klasu i od klase j (ignorira ostale)
- Odluka **većinskim glasanjem:**

$$h(x) = \arg\max_i \sum_{i \neq j} \text{sgn}(h_{ij}(x)), \quad h_{ij}(x) = -h_{ji}(x)$$

- Problem: moguće izjednačenje glasova (rješenje: koristiti pouzdanost, tj. udaljenost od hiperravnine)

#### Shema OVR (One-vs-Rest)

- Treniramo **K** binarnih klasifikatora, po jedan za svaku klasu
- Klasifikator $h_j$ razlikuje klasu j od svih ostalih
- Odluka prema **najpouzdanijem** klasifikatoru:

$$h(x) = \arg\max_j h_j(x)$$

- Granica između klasa i i j je gdje $h_i(x) = h_j(x)$

#### Usporedba OVO i OVR

| Svojstvo | OVO | OVR |
|----------|-----|-----|
| Broj klasifikatora | $\binom{K}{2}$ (kvadratno) | K (linearno) |
| Neuravnoteženost klasa | Manja | Veća (omjer 1:(K-1)) |
| Nejednoznačnost odluke | Moguća (izjednačeni glasovi) | Rijetka |
| Preporuka | Bolje ako K nije prevelik | Bolje za mnogo klasa (efikasnost) |

> **Problem neuravnoteženosti klasa** (class imbalance): kod OVR svaki klasifikator ima puno više negativnih nego pozitivnih primjera → optimizacija ih može sve klasificirati u većinsku klasu.

---

### 5. Klasifikacija regresijom — naivan pristup

Ideja: tretiramo klasifikaciju kao regresiju — primjerima klase 1 dajemo y=1, klase 0 dajemo y=0, treniramo OLS model.

$$h(x; w) = \mathbf{1}\{w^T x \geq 0.5\}$$

Granica između klasa: $h(x) = 0.5$

**Postoji rješenje u zatvorenoj formi** (pseudoinverz), ali pristup ima ozbiljne probleme.

---

### 6. Problemi klasifikacije regresijom

1. **Izlazi nemaju vjerojatnosnu interpretaciju** — domena $h(x)$ nije ograničena na [0, 1]
2. **Nerobusnost** — model je osjetljiv na primjere daleko od granice:
   - Primjeri "duboko" u ispravnom području generiraju velike rezidualne → OLS pomiče granicu prema njima
   - Posljedica: pogrešna klasifikacija primjera blizu granice, čak i kad je problem linearno odvojiv

**Uzrok problema:** funkcija kvadratnog gubitka **kažnjava i točno klasificirane primjere** — što je primjer "točnije" klasificiran (dalje od granice), to je veći gubitak.

---

### 7. Analiza funkcija gubitka

Koristimo oznake $y \in \{-1, +1\}$ i analiziramo gubitak kao funkciju od $w^T\phi(x) \cdot y$:
- $w^T\phi(x) \cdot y > 0$ → točna klasifikacija
- $w^T\phi(x) \cdot y < 0$ → netočna klasifikacija

| Funkcija gubitka | Ponašanje | Problem |
|------------------|-----------|---------|
| **Gubitak 0-1** | 1 za netočne, 0 za točne | Nije derivabilna, konstantna osim u 0 → ne može se optimizirati |
| **Kvadratni gubitak** | Parabola s minimumom u $w^T\phi(x)y = 1$ | Kažnjava i točno klasificirane primjere (raste za velike pozitivne vrijednosti) |
| **Gubitak perceptrona** | 0 za točne, linearno raste za netočne | Derivabilan na negativnoj strani → može se optimizirati gradijentnim spustom |

> **Ključan uvid:** želimo funkciju gubitka što sličniju gubitku 0-1, ali koja je derivabilna i ima nagib. Gubitak perceptrona je takva aproksimacija.

---

### 8. Perceptron

**Model:**

$$h(x; w) = f(w^T \phi(x))$$

gdje je f funkcija praga (step-funkcija / aktivacijska funkcija):

$$f(\alpha) = \begin{cases} +1 & \text{ako } \alpha \geq 0 \\ -1 & \text{inače} \end{cases}$$

**Funkcija gubitka perceptrona:**

$$L(y, h(x)) = \max(0, -w^T\phi(x) \cdot y)$$

- Kažnjava samo netočno klasificirane primjere, proporcionalno koliko su netočni
- Gubitak = 0 za točno klasificirane primjere

**Funkcija pogreške:**

$$E(w|D) = \sum_{i=1}^{N} \max(0, -w^T\phi(x^{(i)}) y^{(i)}) = -\sum_{i: f(w^T\phi(x^{(i)})) \neq y^{(i)}} w^T\phi(x^{(i)}) y^{(i)}$$

- Drugi izraz: suma samo po **netočno klasificiranim** primjerima
- Funkcija je po dijelovima linearna i **konveksna**

**Gradijent gubitka** (za netočno klasificirane primjere):

$$\nabla_w(-w^T\phi(x)y) = -\phi(x)y$$

**Pravilo ažuriranja (Widrow-Hoffovo delta-pravilo):**

$$w \leftarrow w + \eta \phi(x) y$$

- $\eta$ = stopa učenja (learning rate)
- Ažuriramo samo za **netočno klasificirane** primjere

**Algoritam perceptrona:**
1. Inicijaliziraj $w \leftarrow (0, \ldots, 0)$
2. Ponavljaj do konvergencije:
3. Za svaki primjer i = 1, ..., N:
4. Ako $f(w^T\phi(x^{(i)})) \neq y^{(i)}$ → $w \leftarrow w + \eta\phi(x^{(i)})y^{(i)}$

**Konvergencija:** ako su primjeri **linearno odvojivi**, perceptron nalazi rješenje u konačnom broju koraka. Ako **nisu linearno odvojivi** → ne konvergira.

---

### 9. Usporedba klasifikacije regresijom i perceptrona

| Svojstvo | Klasifikacija regresijom | Perceptron |
|----------|--------------------------|------------|
| Robusnost | Nerobusna (kažnjava točne primjere) | Robusna (ignorira točne primjere) |
| Rješenje | Zatvorena forma (pseudoinverz) | Iterativno (gradijentni spust) |
| Konvergencija | Uvijek (zatvorena forma) | Samo za linearno odvojive probleme |
| Vjerojatnosni izlaz | Ne | Ne |
| Determinizam | Da | Ne (ovisi o inicijalizaciji i redoslijedu) |

> **Zaključak:** ni regresija ni perceptron nisu idealni klasifikatori. Želimo: robusnost (kao perceptron) + konvergenciju (kao regresija) + vjerojatnosni izlaz → **logistička regresija** (sljedeća cjelina).

---

### 10. Ključni pojmovi

| Pojam | Opis |
|-------|------|
| **Diskriminativni model** | Model koji direktno opisuje granicu između klasa |
| **Generativni model** | Model koji modelira distribucije klasa, granicu izvodi indirektno |
| **Diskriminantna funkcija / decizijska granica** | Hiperravnina $h(x) = 0$ koja dijeli prostor na klase |
| **Normala hiperravnine** | Vektor w — okomit na granicu, pokazuje u smjer pozitivne klase |
| **Predznačena udaljenost** | $d = h(x)/\|w\|$ — udaljenost i strana primjera od granice |
| **OVO (One-vs-One)** | Višeklasna shema: $\binom{K}{2}$ klasifikatora, glasanje |
| **OVR (One-vs-Rest)** | Višeklasna shema: K klasifikatora, najpouzdaniji pobjeđuje |
| **Neuravnoteženost klasa** | Problem kad jedna klasa ima puno više primjera od druge |
| **Gubitak 0-1** | Idealna funkcija gubitka za klasifikaciju, ali neoptimizabilna |
| **Gubitak perceptrona** | $\max(0, -w^T\phi(x)y)$ — derivabilna aproksimacija gubitka 0-1 |
| **Aktivacijska funkcija** | Funkcija praga f(α) kod perceptrona |
| **Delta-pravilo** | Pravilo ažuriranja težina perceptrona: $w \leftarrow w + \eta\phi(x)y$ |
| **Stopa učenja (η)** | Veličina koraka u gradijentnom spustu |

---

### 📝 Teorijska ispitna pitanja (Cjelina 5)

#### Pitanje 1: Koje minimalne preinake trebale u algoritmu linearne regresije za klasifikaciju?

| Odgovor | Opis |
|---------|------|
| A | Promijeniti funkciju gubitka |
| B | Promijeniti model i funkciju gubitka |
| **✅ C** | **Promijeniti funkciju gubitka i optimizacijski postupak** |
| D | Promijeniti model, funkciju gubitka i optimizacijski postupak |

> **Objašnjenje:** Problem klasifikacije regresijom leži u **funkciji gubitka** (kvadratni gubitak kažnjava i točne primjere). Mijenjamo gubitak (npr. u gubitak perceptrona), ali onda OLS (zatvorena forma) više ne radi → treba i novi **optimizacijski postupak** (npr. gradijentni spust). Model (linearni) ostaje isti. A je nepotpuno (treba i optimizaciju). B mijenja model nepotrebno. D mijenja sve tri, ali model ne treba mijenjati.

---

#### Pitanje 2: Zašto gubitak 0-1 ne možemo koristiti za optimizaciju?

| Odgovor | Opis |
|---------|------|
| **✅ A** | **Gradijent gubitka 0-1 svugdje je nula osim za h(x) = 0, pa funkcija pogreške ima zaravni po kojima se gradijentni spust ne može spuštati** |
| B | Gubitak 0-1 pored neispravno klasificiranih primjera kažnjava i ispravno klasificirane primjere, i to tim više što su oni dalje od granice između klasa |
| C | Funkcija gubitka 0-1 nije diferencijabilna, pa ne postoji rješenje u zatvorenoj formi i ne postoji gradijent |
| D | Funkcija gubitka 0-1 nije konveksna, pa ni funkcija pogreške nije konveksna već ima lokalne minimume te ne postoji minimizator u zatvorenoj formi |

> **Objašnjenje:** Gubitak 0-1 je **konstantan** (0 ili 1) gotovo svugdje → gradijent je 0 → gradijentni spust nema nagiba za spuštanje. Nije problem da gradijent "ne postoji" (C) — gradijent postoji, samo je nula. B opisuje problem **kvadratnog** gubitka, ne gubitka 0-1. D — konveksnost nije glavni problem; problem je ravnina.

---

#### Pitanje 3: Koje tri komponente algoritma bi dale bolju klasifikaciju od regresije, a drugačije od logističke regresije?

| Odgovor | Opis |
|---------|------|
| A | M: h(x) = σ(w^T x); G: L = -y ln h(x) - (1-y) ln(1-h(x)); O: w* = X⁺y |
| B | M: h(x) = w^T x; G: L = -y ln h(x) - (1-y) ln(1-h(x)); O: w* gradijentnim spustom |
| C | M: h(x) = w^T x; G: L = (y - h(x))²; O: w* = X⁺y |
| **✅ D** | **M: h(x) = σ(w^T x); G: L = (y - h(x))²; O: w* gradijentnim spustom** |

> **Objašnjenje:** A ima model i gubitak logističke regresije ali s pseudoinverzom (nekonzistentno — cross-entropy nema zatvorenu formu). B koristi cross-entropy na linearnom modelu bez sigmoide (h(x) nije u [0,1], ln neće raditi). C je identično linearna regresija (ništa nije promijenjeno). D: sigmoidni model + kvadratni gubitak + gradijentni spust — valjana kombinacija, različita od logističke regresije (koja koristi cross-entropy).

---

#### Pitanje 4: Prednosti i nedostatci OVO i OVR sheme za K klasa s N/K primjera po klasi?

| Odgovor | Opis |
|---------|------|
| A | OVR treba K puta više klasifikatora nego OVO, ali su kod OVO pozitivne klase K/2 puta manje zastupljene nego OVR |
| **✅ B** | **OVO iziskuje (K-1)/2 puta više klasifikatora nego OVR, ali svaki OVR klasifikator ima K-1 puta manje pozitivnih primjera nego negativnih** |
| C | OVR iziskuje K-1 puta više klasifikatora od sheme OVO, ali kod OVO pozitivne klase imaju K-1 puta manje primjera |
| D | OVO svaki klasifikator trenira s K/2 puta manje primjera nego OVR, ali pozitivne klase kod OVR imaju K puta manje primjera nego kod OVO |

> **Objašnjenje:** OVO ima C(K,2) = K(K-1)/2 klasifikatora, OVR ima K. Omjer: (K-1)/2 — OVO treba (K-1)/2 puta više. Kod OVR: svaki klasifikator ima N/K pozitivnih i N(K-1)/K negativnih → omjer negativnih/pozitivnih = **(K-1):1**. A tvrdi da OVR treba više (obrnuto). C tvrdi da OVR treba K-1 puta više (obrnuto). D miješa veličine.

---

#### Pitanje 5: Što je specifično za gubitak perceptrona u odnosu na gubitke LR-a i SVM-a?

| Odgovor | Opis |
|---------|------|
| A | Svaki primjer nanosi gubitak, ali manji za točno klasificirane nego za netočno klasificirane |
| **✅ B** | **Gubitak za sve točno klasificirane primjere je nula, a za netočno klasificirane može biti manji od 1** |
| C | Točno klasificirani primjer nanosi gubitak manji od 1 te gubitak opada što je primjer bliže granici |
| D | Gubitak netočno klasificiranih primjera raste linearno s udaljenošću od granice |

> **Objašnjenje:** Gubitak perceptrona: max(0, -w^T φ(x)y). Za točne: 0. Za netočne: -w^T φ(x)y > 0, ali za **jedva netočne** primjere (w^T φ(x)y malo negativan) gubitak je mali, npr. 0.3 < 1. Kod SVM (hinge loss): za netočne gubitak je uvijek ≥ 1. Kod LR: gubitak nikad nije 0. A je netočno (točni imaju gubitak 0, ne "mali"). C je netočno (točni imaju gubitak 0, ne < 1). D je istinito ali nije **specifično** za perceptron — isto vrijedi i za SVM.

---

#### Pitanje 6: Po čemu se gubitak zglobnice (SVM) razlikuje od gubitka perceptrona?

| Odgovor | Opis |
|---------|------|
| A | Za ispravno klasificirane primjere gubitak zglobnice je manji od gubitka za neispravno klasificirane primjere |
| B | Gubitak zglobnice je nula za primjere koji su ispravno klasificirani i daleko od granice |
| C | Za neispravno klasificirane primjere gubitak zglobnice raste linearno s udaljenošću od hiperravnine |
| D | **Gubitak zglobnice kažnjava sve primjere koji se nalaze unutar margine, čak i one koji su ispravno klasificirani** |

| Odgovor | ✅ |
|---------|---|
| **✅ D** | **Gubitak zglobnice kažnjava primjere unutar margine, čak i ispravno klasificirane** |

> **Objašnjenje:** Hinge loss (SVM): max(0, 1 - w^T φ(x)y). Gubitak = 0 tek kad w^T φ(x)y ≥ 1 (izvan margine). Za 0 ≤ w^T φ(x)y < 1 primjer JE ispravno klasificiran ali je unutar margine → gubitak > 0. Perceptron: gubitak = 0 čim je w^T φ(x)y ≥ 0 (na ispravnoj strani). Ovo je **ključna razlika**. B je istinito ali nije specifično — i perceptron ima to svojstvo. C je istinito ali vrijedi i za perceptron.

---

### 🧮 Napomene za problemske zadatke (Cjelina 5)

#### Zadatak tip 1: Određivanje težina linearnog diskriminativnog modela iz primjera

- Model: h(x; w) = w^T x + w₀, granica: h(x) = 0
- Ako model ispravno klasificira oba primjera i h(x) = neka zadana vrijednost, postavi sustav jednadžbi
- Induktivna pristranost "maksimizira minimalnu udaljenost" → traži se SVM-ovski pristup (margina)
- Predznačena udaljenost: d = h(x) / ||w|| → iz zadanih uvjeta izvuci težine
- Za 2D: w₁x₁ + w₂x₂ + w₀ = h(x) daje sustav od 2 jednadžbe za 2 primjera → riješi za nepoznatu težinu

#### Zadatak tip 2: OVO vs OVR za višeklasni problem s neuravnoteženim klasama

- OVO: C(K,2) klasifikatora, svaki treniran samo na primjerima iz dviju klasa
- OVR: K klasifikatora, svaki treniran na svim primjerima (klasa i vs. sve ostale)
- OVO koristi manje primjera po klasifikatoru (samo 2 klase) → manje značajki efikasno korišteno
- OVR: neuravnoteženost = 1:(K-1) za uravnotežene klase; gora za male klase
- Pazi na specifičnosti pojedinih klasa: ako je neka klasa slična drugoj (npr. "politika" i "znanost"), OVR može imati problema jer trpa sve ostale zajedno
- Ključ: razmisli koliko primjera svaki klasifikator dobiva i kakav je omjer klasa

#### Zadatak tip 3: Stabilnost OVO vs OVR s obzirom na kondiciju matrice dizajna

- Bez regularizacije (λ=0): rješenje ovisi o inverzu Gramove matrice Φ^T Φ
- Kondicija matrice ovisi o broju primjera N i broju značajki m+1
- OVO: svaki klasifikator trenira na podskupu primjera (samo 2 klase) → manje primjera → veći rizik da N < m+1 → loša kondicija
- OVR: svaki klasifikator koristi sve primjere → N ostaje velik → bolja kondicija
- Usporedi N_ovo = N_i + N_j (zbroj primjera dviju klasa) vs N_ovr = N (svi primjeri)
- Model je nestabilniji kad ima više značajki u odnosu na primjere

#### Zadatak tip 4: Izračun empirijske pogreške perceptrona s početnim težinama

- Preslikaj svaki primjer x^(i) u prostor značajki: φ(x^(i))
- Izračunaj w^T φ(x^(i)) za svaki primjer
- Primijeni funkciju praga: f(α) = +1 ako α ≥ 0, inače -1
- Usporedi predikciju s oznakom y^(i)
- Gubitak perceptrona za svaki primjer: max(0, -w^T φ(x^(i)) · y^(i))
- Empirijska pogreška E(w|D) = Σ max(0, -w^T φ(x^(i)) y^(i)) — zbroj po svim primjerima
- Pazi: nema faktora 1/N ispred sume kod perceptrona!

#### Zadatak tip 5: Tehnički razlog nekonvergencije perceptrona

- Konceptualni razlog: podatci nisu linearno odvojivi
- Tehnički razlog: u prostoru parametara **ne postoji točka** u kojoj je gradijent empirijske pogreške jednak nuli
- Za svaku kombinaciju težina, uvijek postoji barem jedan netočno klasificiran primjer → gradijent gubitka za taj primjer ≠ 0
- Razlikuj: "funkcija nije derivabilna" (krivo) vs. "ne postoji točka s gradijentom 0" (točno)
- Pogreška perceptrona je konveksna i po dijelovima linearna — ali minimum ne doseže 0 ako primjeri nisu odvojivi

---

## Cjelina 6: Logistička regresija

### 1. Model logističke regresije

**Poopćeni linearni model (GLM):** nelinearna funkcija omotana oko skalarnog umnoška:

$$h(x; w) = f(w^T \phi(x))$$

gdje je f **aktivacijska funkcija** (squashing function) — preslikava $(-\infty, +\infty)$ na ograničen interval.

**Sigmoidna (logistička) funkcija:**

$$\sigma(\alpha) = \frac{1}{1 + \exp(-\alpha)}$$

Tri ključna svojstva sigmoide:
1. Kodomena je **otvoreni interval (0, 1)** → izlaz se može tumačiti kao vjerojatnost
2. Oblik sličan funkciji praga (step-funkciji) → blizu 1 za pozitivnu klasu, blizu 0 za negativnu
3. **Derivabilna** na cijeloj domeni → pogodna za optimizaciju

**Derivacija sigmoide:**

$$\sigma'(\alpha) = \sigma(\alpha)(1 - \sigma(\alpha))$$

**Model logističke regresije:**

$$h(x; w) = \sigma(w^T \phi(x)) = \frac{1}{1 + \exp(-w^T \phi(x))} = P(y = 1|x)$$

- Izlaz = **vjerojatnost** da primjer pripada pozitivnoj klasi → **probabilistički klasifikator**
- Granica između klasa: $h(x) = 0.5$, tj. $w^T \phi(x) = 0$
- Diskriminativan model: parametri opisuju samo granicu

**Nagib sigmoide:** množenje ulaza faktorom $\alpha > 1$ povećava nagib (sigmoida "otvrdnjava" prema step-funkciji).

---

### 2. Pogreška unakrsne entropije — izvod

**Postupak:** isti recept kao kod regresije — negativan logaritam vjerojatnosti oznaka (MLE).

**Korak 1 — distribucija oznaka:** kod klasifikacije $y \in \{0, 1\}$ → **Bernoullijeva distribucija:**

$$P(y|\mu) = \mu^y (1 - \mu)^{1-y}$$

- $y = 1 \Rightarrow P = \mu$
- $y = 0 \Rightarrow P = 1 - \mu$

**Korak 2 — parametar μ = izlaz modela:**

$$P(y|x) = h(x; w)^y (1 - h(x; w))^{1-y}$$

**Korak 3 — zajednička vjerojatnost (IID pretpostavka):**

$$P(y|X) = \prod_{i=1}^{N} P(y^{(i)}|x^{(i)})$$

**Korak 4 — log-vjerodostojnost:**

$$\ln P(y|X) = \sum_{i=1}^{N} \left[ y^{(i)} \ln h(x^{(i)}) + (1 - y^{(i)}) \ln(1 - h(x^{(i)})) \right]$$

**Korak 5 — empirijska pogreška = negativna log-vjerodostojnost:**

$$E(w|D) = \frac{1}{N} \sum_{i=1}^{N} \left[ -y^{(i)} \ln h(x^{(i)}) - (1 - y^{(i)}) \ln(1 - h(x^{(i)})) \right]$$

Ovo je **pogreška unakrsne entropije** (cross-entropy error).

---

### 3. Gubitak unakrsne entropije

**Funkcija gubitka** (unutar sume):

$$L(y, h(x)) = -y \ln h(x) - (1 - y) \ln(1 - h(x))$$

Provjera smislenosti:
- y=1, h(x)≈1 → gubitak ≈ 0 (točna klasifikacija, istinito pozitivan)
- y=1, h(x)≈0 → gubitak → ∞ (netočna, lažno negativan)
- y=0, h(x)≈0 → gubitak ≈ 0 (točna klasifikacija, istinito negativan)
- y=0, h(x)≈1 → gubitak → ∞ (netočna, lažno pozitivan)

> **Napomena:** izlaz sigmoide nikad nije točno 0 ili 1 (otvoreni interval), pa gubitak nikada nije točno 0 ni ∞. Čak i točno klasificirani primjeri nanose mali gubitak.

**Logistički gubitak** (kao funkcija jedne varijable, za oznake $\{-1, +1\}$):

$$L(w^T\phi(x) \cdot y) = \ln(1 + \exp(-w^T\phi(x) \cdot y))$$

(Skaliran s $1/\ln 2$ da bude $L(0) = 1$ za usporedbu s ostalim gubicima.)

---

### 4. Usporedba svih funkcija gubitaka

| Gubitak | Točno klasificirani (daleko od granice) | Točno klasificirani (blizu granice) | Netočno klasificirani | Derivabilan? |
|---------|----------------------------------------|-------------------------------------|----------------------|-------------|
| **0-1** | 0 | 0 | 1 | Ne |
| **Kvadratni** | Velik! (raste kvadratno) | Mali | Velik | Da |
| **Perceptron** | 0 | 0 | Raste linearno | Djelomično |
| **Logistički** | ≈0 (teži k 0, ali nikad 0) | Mali | Raste (>1) | **Da** |

> **Ključno:** logistički gubitak je jedini koji: (1) minimalno kažnjava točno klasificirane, (2) jako kažnjava netočno klasificirane, i (3) je potpuno derivabilan.

---

### 5. Gradijentni spust

**Problem:** za logističku regresiju **ne postoji rješenje u zatvorenoj formi** (nelinearna ovisnost o w zbog sigmoide) → koristimo gradijentni spust.

**Pravilo ažuriranja:**

$$w \leftarrow w - \eta \nabla E(w|D)$$

#### Konveksnost

- Funkcija pogreške unakrsne entropije je **konveksna** → ima samo jedan (globalni) minimum
- Konveksnost je aditivna: zbroj konveksnih funkcija je konveksan → dovoljno da je gubitak konveksan
- Gradijentni spust sigurno nalazi globalni minimum (nema lokalnih minimuma)

#### Stopa učenja η

- Prevelika → divergencija
- Premala → spora konvergencija
- **Linijsko pretraživanje** (line search): u svakom koraku odabiremo optimalan η minimizacijom $g(\eta) = f(x + \eta \Delta x)$ → garantira **globalnu konvergenciju**

---

### 6. Standardni vs. stohastički gradijentni spust

#### Standardni (batch) gradijentni spust

$$w \leftarrow w - \eta \sum_{i=1}^{N} \nabla_w L(y^{(i)}, h(x^{(i)}))$$

- Zbroji gradijente za **sve** primjere, pa tek napravi jedan korak
- Koristi linijsko pretraživanje za η

#### Stohastički gradijentni spust (SGD)

$$w \leftarrow w - \eta \nabla_w L(y^{(i)}, h(x^{(i)}))$$

- Ažurira težine za **svaki primjer zasebno**
- Prije svake epohe **slučajno permutira** primjere
- **Ne koristi** linijsko pretraživanje

#### Minibatch gradijentni spust

- Kompromis: gradijent na manjoj slučajnoj grupi primjera
- U praksi radi **najbolje**

| Svojstvo | Batch | SGD | Minibatch |
|----------|-------|-----|-----------|
| Računalna zahtjevnost | Velika | Mala | Srednja |
| Stabilnost smjera | Visoka | Niska (stohastično) | Srednja |
| Izbjegavanje lokalnih min. | Loše | Dobro | Dobro |

---

### 7. Gradijent logističke regresije

**Gradijent gubitka** (za jedan primjer):

$$\nabla_w L(y, h(x)) = (h(x) - y) \cdot \phi(x)$$

- Izvod koristi pravilo ulančavanja + derivaciju sigmoide $\sigma'(\alpha) = \sigma(\alpha)(1-\sigma(\alpha))$, koja se pokrati
- Intuitivno: što je veća razlika predikcije i oznake $(h(x) - y)$, to je veći gradijent

**Gradijent ukupne pogreške** (za batch):

$$\nabla_w E(w|D) = \sum_{i=1}^{N} (h(x^{(i)}) - y^{(i)}) \cdot \phi(x^{(i)})$$

**Algoritam (SGD):**
1. Inicijaliziraj $w \leftarrow (0, ..., 0)$
2. Ponavljaj do konvergencije:
3. Slučajno permutiraj primjere
4. Za svaki primjer i:
5. $h \leftarrow \sigma(w^T \phi(x^{(i)}))$
6. $w \leftarrow w - \eta(h - y^{(i)}) \phi(x^{(i)})$

---

### 8. Regularizirana logistička regresija

**Problem prenauučenosti** kod logističke regresije — tri uzroka:
1. Presložen model (nelinearno preslikavanje φ)
2. Previše značajki
3. **Otvrdnjavanje sigmoide** (specifično za LR): ako je problem linearno odvojiv, algoritam beskonačno povećava ||w|| → sigmoida postaje step-funkcija → loša generalizacija

**L2-regularizirana pogreška:**

$$E_R(w|D) = \sum_{i=1}^{N} \left[ -y^{(i)} \ln h(x^{(i)}) - (1-y^{(i)}) \ln(1-h(x^{(i)})) \right] + \frac{\lambda}{2} w^T w$$

**Gradijent:**

$$\nabla_w E_R = \sum_{i=1}^{N} (h(x^{(i)}) - y^{(i)}) \phi(x^{(i)}) + \lambda w$$

**Ažuriranje težina (s efektom propadanja težina / weight decay):**

$$w \leftarrow w(1 - \eta\lambda) - \eta \sum_{i=1}^{N} (h(x^{(i)}) - y^{(i)}) \phi(x^{(i)})$$

> **VAŽNO:** težinu $w_0$ **NE regulariziramo!** Ako bismo je regularizirali, hiperravnina bi uvijek morala prolaziti kroz ishodište (jer $w_0 \to 0$ → udaljenost od ishodišta $= -w_0/\|w\| \to 0$).

---

### 9. Ključni pojmovi

| Pojam | Opis |
|-------|------|
| **Logistička regresija** | Diskriminativni probabilistički klasifikator sa sigmoidnom aktivacijom |
| **Sigmoidna funkcija** | $\sigma(\alpha) = 1/(1+e^{-\alpha})$, kodomena (0,1), derivacija = $\sigma(1-\sigma)$ |
| **Poopćeni linearni model (GLM)** | Model oblika $h(x) = f(w^T\phi(x))$ s nelinearnom aktivacijom f |
| **Bernoullijeva distribucija** | $P(y|\mu) = \mu^y(1-\mu)^{1-y}$, modelira binarnu oznaku |
| **Gubitak unakrsne entropije** | $L = -y\ln h(x) - (1-y)\ln(1-h(x))$ |
| **Logistički gubitak** | $\ln(1+\exp(-w^T\phi(x)y))$ — za oznake {-1,+1} |
| **Konveksna funkcija** | Funkcija oblika "zdjele" — ima samo globalni minimum |
| **Linijsko pretraživanje** | Optimizacija stope učenja u svakom koraku gradijentnog spusta |
| **Batch gradijentni spust** | Ažurira težine nakon zbrajanja gradijenata za sve primjere |
| **SGD** | Ažurira težine za svaki primjer zasebno, s permutacijom po epohama |
| **Minibatch** | Kompromis: gradijent na manjim slučajnim grupama primjera |
| **Otvrdnjavanje sigmoide** | Rast ||w|| → sigmoida postaje step-funkcija → prenauučenost |
| **Weight decay** | Efekt L2-regularizacije: $w \leftarrow w(1-\eta\lambda)$ u svakom koraku |
| **Epoha** | Jedan prolaz kroz sve primjere u skupu za učenje |

---

### 📝 Teorijska ispitna pitanja (Cjelina 6)

#### Pitanje 1: Koji uvjet je dovoljan da granica između klasa u ulaznom prostoru bude linearna?

| Odgovor | Opis |
|---------|------|
| A | f je afina funkcija |
| **✅ B** | **φ(x) = (1, x)** |
| C | f je afina funkcija i φ(x) = (1, x) |
| D | f(x) = x |

> **Objašnjenje:** Model je h(x) = f(w^T φ(x)). Granica je definirana s w^T φ(x) = c (neka konstanta). Ako je φ(x) = (1, x), onda je w^T φ(x) = w₀ + w^T x — linearan izraz u x → granica je hiperravnina u ulaznom prostoru, **neovisno o tome koja je f** (dokle god je monotona). Ako je f afina ali φ nelinearna, granica je nelinearna. Stoga je dovoljno samo φ(x) = (1, x).

---

#### Pitanje 2: Na koji način smo modelirali distribuciju vjerojatnosti oznake y pojedinog primjera?

| Odgovor | Opis |
|---------|------|
| A | P(y|x) = (y - h(x))x |
| **✅ B** | **P(y|x) = h(x)^y (1 - h(x))^(1-y)** |
| C | P(y|x) = y^h(x) (1 - y)^h(x) |
| D | P(y|x) = h(x)(1 - h(x)) |

> **Objašnjenje:** Oznaku y modeliramo **Bernoullijevom distribucijom** s parametrom μ = h(x;w): P(y|μ) = μ^y (1-μ)^(1-y). Uvrštavanjem μ = h(x) dobivamo B. Za y=1: P = h(x). Za y=0: P = 1-h(x). A je besmisleno (nije vjerojatnost). C zamjenjuje uloge y i h(x). D je derivacija sigmoide, ne distribucija.

---

#### Pitanje 3: Što nam osigurava uporaba linijskog pretraživanja kod optimizacije logističke regresije?

| Odgovor | Opis |
|---------|------|
| A | Da postupak uvijek konvergira, neovisno o odabranoj stopi učenja η i početnim težinama w |
| **✅ B** | **Da postupak uvijek konvergira, pod uvjetom da su primjeri linearno neodvojivi ili da regulariziramo sa λ > 0** |
| C | Da postupak ne može zaglaviti u lokalnom minimumu, pod uvjetom da u skupu D nema multikolinearnosti |
| D | Da postupak konvergira brže, pod uvjetom da su primjeri linearno odvojivi i da stopa učenja nije prevelika |

> **Objašnjenje:** Linijsko pretraživanje daje **globalnu konvergenciju** — ali samo ako minimum postoji u konačnom. Ako su primjeri **linearno odvojivi** i nema regularizacije, težine rastu u beskonačnost (otvrdnjavanje sigmoide) → nema konačnog minimuma → nema konvergencije. Ako su primjeri **neodvojivi** ili koristimo **regularizaciju**, minimum postoji → linijsko pretraživanje garantira konvergenciju. A je netočno jer linijsko pretraživanje samo određuje η. C je nepotrebno — pogreška je konveksna, lokalnih minimuma ionako nema.

---

#### Pitanje 4: Zbog čega dolazi do prenauučenosti neregularizirane logističke regresije na linearno odvojivim podatcima?

| Odgovor | Opis |
|---------|------|
| A | Empirijska pogreška logističke regresije smanjuje se s porastom broja primjera |
| B | Ispravno klasificirani primjeri koji su vrlo udaljeni od granice nanose malen gubitak |
| **✅ C** | **S porastom norme vektora težina gubitak na točnim primjerima teži prema nuli** |
| D | Netočno klasificirani primjeri nanose gubitak koji je proporcionalan normi vektora težina |

> **Objašnjenje:** Kad su primjeri linearno odvojivi, rast ||w|| povećava w^T φ(x)y za sve primjere → logistički gubitak ln(1+exp(-w^T φ(x)y)) teži k 0. Algoritam zato **beskonačno povećava** ||w|| → sigmoida otvrdnjava → prenauučenost. B je istinit ali nije **uzrok** prenauučenosti — B opisuje normalno ponašanje, C opisuje mehanizam koji pokreće beskonačan rast težina. A govori o broju primjera (irelevantno). D opisuje nešto drugo.

---

#### Pitanje 5: Što globalna konvergencija znači za neregulariziranu logističku regresiju na linearno neodvojivom problemu?

| Odgovor | Opis |
|---------|------|
| A | Optimizacijski algoritam će konvergirati prema parametrima koji minimiziraju pogrešku na skupu za učenje, ali neće doseći miniminum |
| B | Gradijentni spust neće krivudati u prostoru parametara jer optimizacijski algoritam koristi informaciju o zakrivljenosti površine pogreške |
| C | Optimizacijski algoritam će konvergirati do minimuma, ali nema garancije da će to biti globalni minimum funkcije pogreške |
| **✅ D** | **Neovisno o inicijalizaciji, optimizacijski će algoritam pronaći parametre koji minimiziraju pogrešku na skupu za učenje** |

> **Objašnjenje:** Globalna konvergencija = konvergencija do minimuma **neovisno o početnoj točki**. Budući da je pogreška unakrsne entropije **konveksna**, svaki minimum je globalni → globalna konvergencija znači da ćemo sigurno naći globalni optimum. A tvrdi da neće doseći minimum (netočno — hoće). B govori o zakrivljenosti (to je Newtonova metoda, ne linijsko pretraživanje). C negira globalnost minimuma (netočno za konveksnu funkciju).

---

### 🧮 Napomene za problemske zadatke (Cjelina 6)

#### Zadatak tip 1: Utjecaj skaliranja značajki na gubitak unakrsne entropije

- Gubitak: L(y, h(x)) = -y ln h(x) - (1-y) ln(1 - h(x))
- h(x) = σ(w^T x + w₀), ako pomnožimo značajke s 2: novi argument sigmoide = w^T(2x) + w₀ = 2w^T x + w₀
- Iz poznatog gubitka L(0, h(x)) = 0.274 → izračunaj h(x): za y=0 gubitak je -ln(1-h(x)) → 1-h(x) = exp(-0.274) → h(x) = 1 - exp(-0.274)
- Iz h(x) izračunaj w^T x (pomoću inverzne sigmoide: α = ln(h/(1-h)))
- Novi α' = 2·(α - w₀) + w₀ → novi h(x') = σ(α') → novi gubitak

#### Zadatak tip 2: Gubitak nakon promjene oznake (ispravak pogrešno označenog primjera)

- Gubitak unakrsne entropije: L(y, h(x)) = -y ln h(x) - (1-y) ln(1-h(x))
- Ako je primjer pogrešno označen s y, nova oznaka je 1-y
- Poznato: L(y, h(x)) = 1.20, traži se L(1-y, h(x))
- Veza: L(y, h(x)) + L(1-y, h(x)) = -ln h(x) - ln(1-h(x)) = -ln[h(x)(1-h(x))]
- Za y=1: L = -ln h(x) = 1.20 → h(x) = exp(-1.20). Za y=0: L = -ln(1-h(x)) → izračunaj
- Alternativno: ako znamo da je pogrešno klasificiran (velik gubitak), nova oznaka daje mali gubitak

#### Zadatak tip 3: Izračun L2-norme gradijenta gubitka u jednoj iteraciji SGD-a

- Gradijent gubitka: ∇L = (h(x) - y) · φ(x)
- Koraci: (1) preslikaj x u φ(x), (2) izračunaj w^T φ(x), (3) primijeni sigmoidu: h = σ(w^T φ(x)), (4) izračunaj h - y, (5) pomnoži s φ(x) → to je gradijent
- L2-norma gradijenta: ||∇L||₂ = |h - y| · ||φ(x)||₂
- Pazi na interakcijske članove u φ (npr. x₁x₂)

#### Zadatak tip 4: Odabir početnih parametara za najbrže konvergiranje (analiza kontura)

- Gradijentni spust s linijskim pretraživanjem konvergira u minimum po najkraćem "putu"
- Na konturnom grafu: minimizator je u sredini kontura
- Počnite od svake w₁...w₄ i vizualizirajte koliko koraka treba do minimuma
- Bliži početni parametri minimumu → manje koraka (ali smjer gradijenta također igra ulogu)
- Kad je početna točka na osi jedne od glavnih smjerova kontura, spust ide ravno → manje koraka
- Najgori slučaj: početna točka pod 45° od osi → cik-cak kretanje → više koraka

#### Zadatak tip 5: Ponašanje pogreške NR vs L2R kroz iteracije

- NR (neregularizirana LR): na linearno odvojivim podatcima pogreška pada asimptotski prema 0 (ali nikad ne doseže 0 jer gubitak nikad nije točno 0)
- L2R (L2-regularizirana LR): pogreška pada do nekog konačnog minimuma i tu stagnira (regularizacija sprječava beskonačan rast težina)
- Perceptron: konvergira u konačnom broju koraka (ako linearno odvojivo)
- Ključna razlika: NR pogreška monotono pada ali nikad ne stane, L2R doseže stabilnu točku

#### Zadatak tip 6: Koji algoritam (model + preslikavanje) pronalazi minimizator empirijske pogreške

- Perceptron konvergira samo za linearno odvojive probleme u prostoru značajki
- LR (neregularizirana) na linearno odvojivim: težine rastu u beskonačnost → nema konačnog minimizatora
- LR na linearno neodvojivim: konveksna pogreška → minimizator postoji i GD ga nalazi
- Provjeri za svaki φ: jesu li podatci linearno odvojivi u prostoru značajki?
  - Ako jesu → perceptron konvergira, ali LR nema konačan minimizator (težine → ∞)
  - Ako nisu → perceptron ne konvergira, ali LR ima minimizator
- Odgovor je kombinacija LR + preslikavanje koje NE daje linearnu odvojivost

#### Zadatak tip 7: Izračun promjene jedne težine u regulariziranom SGD-u

- Pravilo ažuriranja za w (bez w₀): w ← w(1 - ηλ) + η·(y - h(x))·φ(x)
- Promjena Δw_j = -ηλ·w_j + η·(y^(i) - h(x^(i)))·φ_j(x^(i)) = η·[-(λ·w_j) + (y-h)·φ_j]
- Alternativno iz gradijenta: Δw_j = -η·[(h-y)·φ_j + λ·w_j]
- Koraci: (1) izračunaj φ(x), (2) izračunaj w^T φ(x), (3) h = σ(w^T φ(x)), (4) primijeni formulu
- Pazi: w₀ se NE regularizira! Ako se pita za Δw₀, izostavi član λ·w₀
- Pazi koji indeks težine se traži (w₁ odgovara φ₁ = x₁, ne nužno drugoj komponenti vektora w)

---

## Cjelina 7: Logistička regresija II

### 1. Alternative gradijentnom spustu

**Problem s gradijentnim spustom:** koristi samo gradijent (prvu derivaciju) → može krivudati ("cik-cak") posebno kod elongiranih kontura → spora konvergencija.

**Rješenje:** koristiti i **zakrivljenost** (drugu derivaciju) → **optimizacija drugog reda**.

---

### 2. Newtonov postupak

**Ideja:** u trenutnoj točki $x_t$ napraviti **kvadratnu aproksimaciju** funkcije (Taylorov razvoj 2. reda), pa skočiti u minimum te aproksimacije.

**Taylorova aproksimacija 2. reda** (za funkciju više varijabli):

$$f(x) \approx f(x_t) + \nabla f(x_t)^T (x - x_t) + \frac{1}{2} (x - x_t)^T H_f(x_t) (x - x_t)$$

**Hesseova matrica** $H_f$ — kvadratna matrica parcijalnih derivacija drugog reda:

$$(H_f)_{i,j} = \frac{\partial^2 f}{\partial x_i \partial x_j}$$

- Dimenzija: $(m+1) \times (m+1)$
- Simetrična matrica (komutativnost parcijalnih derivacija)
- **Pozitivno semidefinitna** $\Leftrightarrow$ $f$ je konveksna
- Za inverz treba biti **pozitivno definitna**

**Pravilo ažuriranja:**

$$x_{t+1} = x_t - \eta \cdot H_f(x_t)^{-1} \nabla f(x_t)$$

- Ako je Hesseova matrica egzaktna: $\eta = 1$ (korak točno u minimum kvadratne aproksimacije)
- Konvergira **brže** od gradijentnog spusta (manje iteracija)

---

### 3. Newtonov postupak za logističku regresiju

**Hesseova matrica** pogreške unakrsne entropije:

$$H_E = \Phi^T S \Phi$$

gdje je $S = \text{diag}(h(x^{(i)})(1 - h(x^{(i)})))$ — dijagonalna matrica s derivacijama sigmoide.

- Dimenzija: $(m+1) \times (m+1)$
- Uvijek **pozitivno definitna** (ima inverz u svakoj točki w)
- Ali može biti **loše kondicionirana** (multikolinearnost) → potrebna regularizacija

**IRLS** (Iteratively Reweighted Least Squares) — naziv za primjenu Newtonovog postupka na logističku regresiju.

---

### 4. Kvazi-Newtonov postupak

**Problem:** izračun Hesseove matrice i njenog inverza je skup (posebno za velik m).

| Postupak | Opis |
|----------|------|
| **BFGS** | Aproksimira Hesseovu matricu koristeći gradijente iz trenutnog i prethodnog koraka |
| **L-BFGS** | "Komprimirani" BFGS — aproksimacija matricom nižeg ranga, za velike m |

**Hijerarhija brzine konvergencije:** L-BFGS > BFGS > gradijentni spust (manje iteracija, ali svaka iteracija skuplja)

---

### 5. Regularizacija u Newtonovom postupku

**L2-regularizacija** — jednostavno proširenje:
- Gradijent: $\nabla E_R = \nabla E + \lambda w$
- Hesseova matrica: $H_R = H + \lambda I$ (dodaj λ na dijagonalu, osim za $w_0$)

**L1-regularizacija** — kompliciranije:
- L1-norma nije diferencijabilna → računamo **podgradijent** (subgradient)
- Koristi se **koordinatni spust** ili proksimalni postupci
- Implementirano u standardnim alatima, ali složenije od L2

---

### 6. Višeklasna (multinomijalna) logistička regresija

#### Softmax funkcija

Za K klasa, aktivacijska funkcija je **softmax** umjesto sigmoide:

$$\text{softmax}_k(x_1, \ldots, x_n) = \frac{\exp(x_k)}{\sum_j \exp(x_j)}$$

- Normalizira sve vrijednosti tako da se zbrajaju u 1
- **Pojačava** veće vrijednosti, smanjuje manje ("meka" verzija funkcije max)
- Derivabilna i neprekidna

#### Model

Zasebni vektor težina $w_k$ za svaku od K klasa:

$$h_k(x; W) = \frac{\exp(w_k^T \phi(x))}{\sum_j \exp(w_j^T \phi(x))} = P(y = k | x, W)$$

- $W = (w_1, w_2, \ldots, w_K)$ — matrica svih težina
- Izlaz za klasu k uzima u obzir izlaze **svih** klasa (kroz normalizaciju)
- Vjerojatnosti se zbrajaju u 1 (za razliku od OVO/OVR pristupa)

#### Kategorička (multinoullijeva) varijabla

Oznaka se kodira kao **one-hot vektor**: $y = (y_1, \ldots, y_K)^T$ gdje je $y_k = 1$ za pravu klasu, ostale 0.

**Distribucija:**

$$P(y|\mu) = \prod_{k=1}^{K} \mu_k^{y_k}$$

gdje je $\mu_k = h_k(x; W)$.

#### Funkcija pogreške (višeklasna unakrsna entropija)

$$E(W|D) = -\sum_{i=1}^{N} \sum_{k=1}^{K} y_k^{(i)} \ln h_k(x^{(i)}; W)$$

#### Gradijent (za klasu k)

$$\nabla_{w_k} E = \sum_{i=1}^{N} (h_k(x^{(i)}) - y_k^{(i)}) \cdot \phi(x^{(i)})$$

> **Ključno:** isti oblik gradijenta kao kod binarne LR: $(h(x) - y) \cdot \phi(x)$

---

### 7. Poopćeni linearni modeli — unificirani pogled

Sva tri algoritma dijele **isto pravilo ažuriranja** (LMS / Widrow-Hoffovo pravilo):

$$w \leftarrow w - \eta (h(x) - y) \phi(x)$$

| Algoritam | Aktivacijska f | Distribucija oznake | Gubitak |
|-----------|---------------|-------------------|---------|
| **Linearna regresija** | Identitet: $f(\alpha) = \alpha$ | Normalna $N(\mu, \sigma^2)$ | Kvadratni: $(h(x)-y)^2$ |
| **Logistička regresija** | Sigmoida: $\sigma(\alpha)$ | Bernoullijeva | Unakrsna entropija (binarna) |
| **Multinomijalna LR** | Softmax | Multinoullijeva (kategorička) | Unakrsna entropija (višeklasna) |

**Zašto isti gradijent?** Jer sve tri distribucije (normalna, Bernoullijeva, multinoullijeva) pripadaju **eksponencijalnoj familiji** distribucija.

---

### 8. Eksponencijalna familija

Široka grupa distribucija s oblikom:

$$p(x|\theta) = h(x) \exp(\theta^T \phi(x) - A(\theta))$$

- Pripadaju: Gaussova, Bernoullijeva, multinoullijeva, binomna, Studentova, uniformna, beta, gamma, Dirichletova...
- Za svaku distribuciju iz eksponencijalne familije postoji **funkcija sredine** (mean function) koja definira aktivacijsku funkciju f:
  - Gaussova → identitet
  - Bernoullijeva → sigmoida
  - Multinoullijeva → softmax

---

### 9. Adaptivne bazne funkcije i neuronske mreže

**Fiksne bazne funkcije** (dosad): $\phi(x) = (1, x_1, x_2, x_1 x_2, x_1^2, x_2^2)$ — unaprijed definirane, ne prilagođavaju se podacima.

**Problem:** ne znamo unaprijed koje bazne funkcije su dobre za naš problem.

**Rješenje — parametrizirane bazne funkcije:** svaka bazna funkcija je mali poopćeni linearni model:

$$h(x; w) = f\left(\sum_{j=0}^{m} w_j^{(2)} \cdot f\left(\sum_{i=0}^{n} w_{ji}^{(1)} x_i\right)\right) = f(w^{(2)T} f(W^{(1)} x))$$

- $W^{(1)}$ — matrica težina prvog sloja (bazne funkcije)
- $w^{(2)}$ — vektor težina drugog sloja (kombinacija baznih funkcija)

> **Ovo je neuronska mreža!** Može biti dublja (više slojeva). Funkcija preslikavanja φ se **uči iz podataka**.

**Cijena složenosti:**
- Funkcija pogreške je **nekonveksna** (lokalni minimumi)
- Veća mogućnost prenauučenosti
- Složeniji optimizacijski postupak

---

### 10. Ključni pojmovi

| Pojam | Opis |
|-------|------|
| **Optimizacija drugog reda** | Koristi i gradijent i zakrivljenost (Hesseovu matricu) |
| **Newtonov postupak** | Kvadratna aproksimacija + skok u njezin minimum |
| **Hesseova matrica** | Matrica parcijalnih derivacija drugog reda, $(m+1) \times (m+1)$ |
| **IRLS** | Newtonov postupak primijenjen na logističku regresiju |
| **BFGS / L-BFGS** | Kvazi-Newtonovi postupci s aproksimiranom Hesseovom matricom |
| **Softmax** | Aktivacijska funkcija za višeklasnu klasifikaciju, normalizira na zbroj 1 |
| **Multinomijalna LR** | Višeklasna logistička regresija sa softmax aktivacijom |
| **Kategorička varijabla** | One-hot kodirana oznaka za K klasa |
| **LMS pravilo** | $(h(x)-y)\phi(x)$ — zajedničko pravilo ažuriranja za sve GLM-ove |
| **Eksponencijalna familija** | Grupa distribucija s zajedničkim oblikom → daju iste gradijente |
| **Funkcija sredine** | Aktivacijska funkcija f koja proizlazi iz distribucije oznake |
| **Adaptivne bazne funkcije** | Parametrizirane φ koje se uče iz podataka → neuronske mreže |

---

### 📝 Teorijska ispitna pitanja (Cjelina 7)

#### Pitanje 1: Prednosti i nedostatci gradijentnog spusta u odnosu na Newtonov postupak kod logističke regresije?

| Odgovor | Opis |
|---------|------|
| A | GD se može koristiti za L2-regulariziranu LR, ali ako je η prevelika može divergirati, dok Newton nema taj problem |
| **✅ B** | **GD se može koristiti za online (pojedinačno) učenje, no može krivudati i zato sporije konvergirati od Newtonovog postupka** |
| C | Newton brže konvergira, ali se može koristiti samo za konveksnu funkciju pogreške, dok GD nema tog ograničenja ali može zaglaviti u lokalnom optimumu |
| D | GD je računalno jednostavniji od Newtona, ali za razliku od Newtona kod L2-regularizirane regresije ne konvergira ako primjeri nisu linearno odvojivi |

> **Objašnjenje:** Prednost GD: omogućava **online učenje** (SGD ažurira po jednom primjeru). Nedostatak: može krivudati (cik-cak) i sporije konvergirati. Newton koristi zakrivljenost → manje iteracija, ali zahtijeva batch pristup. A je netočno (Newton također može imati problema bez linijskog pretraživanja). C je netočno (GD jednako može zaglaviti u lokalnom optimumu). D je netočno (GD konvergira neovisno o odvojivosti).

---

#### Pitanje 2: Koji je nužan i dovoljan uvjet za izvedivost i numeričku stabilnost Newtonovog postupka kod logističke regresije?

| Odgovor | Opis |
|---------|------|
| A | Značajke moraju biti linearno zavisne |
| B | Funkcija pogreške mora biti konveksna |
| **✅ C** | **U podatcima ne smije biti multikolinearnosti** |
| D | Broj primjera mora biti veći od broja značajki plus jedan |

> **Objašnjenje:** Hesseova matrica $H_E = \Phi^T S \Phi$ za LR je uvijek pozitivno definitna (ima inverz). Ali ako postoji **multikolinearnost**, matrica je loše kondicionirana → inverz je **numerički nestabilan**. B je uvijek istinito za LR (konveksnost je garantirana), ali ne jamči numeričku stabilnost. A je upravo suprotno od poželjnog. D je uvjet za OLS, ne za Newton na LR.

---

#### Pitanje 3: Koja je vremenska računalna složenost algoritma LMS primijenjenog na linearnu regresiju?

| Odgovor | Opis |
|---------|------|
| **✅ A** | **O(ENm)** |
| B | O(E(N + m)) |
| C | O(EN²m) |
| D | O(ENm²) |

> **Objašnjenje:** LMS za jedan primjer: izračunaj $w^T\phi(x)$ = O(m) operacija, ažuriraj w = O(m). Po primjeru: O(m). Po epohi (N primjera): O(Nm). Za E epoha: **O(ENm)**. Za usporedbu, pseudoinverz zahtijeva O(Nm² + m³), što je za jednu "epohu" skuplje, ali se radi samo jednom.

---

#### Pitanje 4: Koja je prednost MLR nad BLR-OVO i BLR-OVR?

| Odgovor | Opis |
|---------|------|
| A | MLR ima više parametara od BLR-OVR, ali nije osjetljiva na neuravnoteženost broja primjera po klasama |
| **✅ B** | **MLR i BLR-OVR imaju manje parametara od BLR-OVO, no jedino za MLR vrijedi Σ_k P(y=k|x) = 1** |
| C | Za razliku od BLR-OVR i BLR-OVO, kod MLR ne postoje područja u ulaznom prostoru za koje klasifikacijska odluka nije određena |
| D | Za razliku od BLR-OVO i BLR-OVR, MLR koristi softmax, pa minimizacija L1-regularizirane pogreške ima rješenje u zatvorenoj formi |

> **Objašnjenje:** MLR ima K vektora težina (kao OVR), dok OVO ima C(K,2) → MLR i OVR imaju manje parametara. Ključna prednost MLR: **softmax garantira da se vjerojatnosti zbrajaju u 1**. Kod OVO i OVR svaki klasifikator daje nezavisnu vjerojatnost → nema garancije da se zbrajaju u 1. D je netočno (softmax ne daje zatvorenu formu za L1). C je netočno (i MLR može imati rubne slučajeve).

---

#### Pitanje 5: Zašto optimizaciju kod logističke regresije ne provodimo izračunom pseudoinverza matrice dizajna?

| Odgovor | Opis |
|---------|------|
| A | Optimizaciju parametara linearne regresije također možemo napraviti GD-om, ali to ne radimo jer je pseudoinverz jeftiniji |
| B | Zbog nelinearnosti logističke funkcije, kod logističke regresije izračun pseudoinverza matrice dizajna nije moguće napraviti u zatvorenoj formi |
| **✅ C** | **Maksimizacija log-izglednosti oznaka logističke regresije kao rješenje za parametre ne daje izraz u zatvorenoj formi koji sadržava pseudoinverz matrice dizajna** |
| D | Optimizaciju možemo provesti izračunom pseudoinverza matrice dizajna, međutim, za razliku od gradijentnog spusta, taj postupak ne funkcionira kada je matrica dizajna singularna |

> **Objašnjenje:** Problem je u **nelinearnoj ovisnosti** izlaza modela o težinama (zbog sigmoide). Kad postavimo ∇E = 0, dobivamo nelinearnu jednadžbu u w → **nema zatvorene forme**. Pseudoinverz matrice Φ se uvijek može izračunati (B je krivo formuliran), ali rješenje LR optimizacije jednostavno nema oblik w* = Φ⁺y. D je netočno — pseudoinverz ne daje rješenje za LR uopće.

---

#### Pitanje 6: Koji je probabilistički princip ugrađen u optimizacijski postupak poopćenih linearnih modela?

| Odgovor | Opis |
|---------|------|
| A | Minimizirati Σ ln h(x^(i); w), gdje je h(x;w) = f(w^T x) |
| B | Minimizirati -Σ ln y^(i) h(x^(i); w), gdje je h(x;w) = w^T x |
| **✅ C** | **Maksimizirati Σ ln p(y^(i)|x^(i)), gdje je E[p(y^(i)|x^(i))] = f(w^T x)** |
| D | Maksimizirati Π_i ln p(y^(i)|x^(i)), gdje je E[p(y^(i)|x^(i))] = w^T x |

> **Objašnjenje:** Princip je **MLE (Maximum Likelihood Estimation)**: maksimiziramo log-vjerodostojnost = Σ ln p(y^(i)|x^(i)). Očekivana vrijednost distribucije dana je **funkcijom sredine** f(w^T x). A minimizira nešto drugo (ne MLE). B ima pogrešan izraz. D koristi Π umjesto Σ za logaritme (log produkta = suma logova, ne produkt logova) i nema aktivacijske funkcije.

---

#### Pitanje 7: Koja je točna poveznica između logističke regresije (LR) i neuronske mreže sa sigmoidnim prijenosnim funkcijama (NN)?

| Odgovor | Opis |
|---------|------|
| A | NN i LR imaju istu funkciju pogreške, ali samo LR može optimirati Newtonovim postupkom jer funkcija gubitka NN nije konveksna |
| B | Jezgreni stroj s Gaussovom jezgrenom funkcijom istovjetan je NN sa L2-regulariziranom funkcijom pogreške |
| C | Model LR istovjetan je modelu dvoslojne NN sa sigmoidnim prijenosnim funkcijama i pogreškom unakrsne entropije |
| **✅ D** | **Model dvoslojne NN istovjetan je modelu LR s poopćenim linearnim modelima sa sigmoidnim funkcijama kao baznim funkcijama** |

> **Objašnjenje:** Iz predavanja: neuronska mreža je proširenje GLM-a gdje su **bazne funkcije prilagodive** — svaka bazna funkcija je mali GLM sa sigmoidom. Dakle, dvoslojna NN = LR čije bazne funkcije su same logističke regresije. C je obrnuto (LR ≠ dvoslojna NN; LR je jednoslojni model). A i B miješaju koncepte.

---

#### Pitanje 8: Što možemo reći o razlici između novih i starih težina kod LMS pravila?

| Odgovor | Opis |
|---------|------|
| A | Razlika je to veća što je stopa učenja η bliža jedinici |
| **✅ B** | **Razlika je to manja što je vektor φ(x) bliži ishodištu** |
| C | Razlika je to veća što je izlaz modela h(x) bliži nuli |
| D | Razlika je to manja što je oznaka y bliže jedinici |

> **Objašnjenje:** LMS ažuriranje: Δw = -η(h(x) - y)φ(x). Norma: ||Δw|| = η·|h(x) - y|·||φ(x)||. Ako je φ(x) bliži ishodištu → ||φ(x)|| je manji → ||Δw|| je manji. A je djelomično točno ali η = 1 ne mora biti "blizu jedinice" za velike promjene. C i D ovise o razlici h(x)-y, ne o pojedinačnim vrijednostima.

---

#### Pitanje 9: Koja je veza između logističke regresije i modela neuronske mreže?

| Odgovor | Opis |
|---------|------|
| A | Multinomijalna LR sa softmax aktivacijom istovjetna je dvoslojnoj NN s više neurona u izlaznom sloju |
| **✅ B** | **LR koja kao adaptivne bazne funkcije koristi logističku regresiju istovjetna je NN sa sigmoidnom aktivacijskom funkcijom** |
| C | NN optimirana algoritmom propagacije pogreške unazad istovjetna je LR optimiranoj stohastičkim gradijentnim spustom |
| D | LR s linearnim jezgrenim funkcijama istovjetna je NN s linearnom aktivacijskom funkcijom i kvadratnom funkcijom pogreške |

> **Objašnjenje:** Ključna ideja predavanja: ako bazne funkcije φ_j definiramo kao **male logističke regresije** (GLM-ove sa sigmoidom), onda ukupni model postaje **neuronska mreža**. B to točno opisuje. A miješa multinomijalnu LR s dvoslojnom NN (MNR je jednoslojna). C je netočno (backprop ≠ SGD za jednoslojni model). D miješa kernele i NN.

---

### 🧮 Napomene za problemske zadatke (Cjelina 7)

#### Zadatak tip 1: Izračun gubitka višeklasne unakrsne entropije za jedan primjer

- Gubitak: L = -Σ_k y_k ln h_k(x; W)
- Koraci:
  1. Izračunaj w_k^T x za svaku klasu k (skalarni produkt k-tog stupca matrice W i vektora x)
  2. Primijeni softmax: h_k = exp(w_k^T x) / Σ_j exp(w_j^T x)
  3. Gubitak: samo klasa s y_k = 1 doprinosi (ostali imaju y_k = 0)
  4. L = -ln h_k za onu klasu k za koju je y_k = 1
- Pazi: stupci matrice W odgovaraju pojedinim klasama
- Softmax: ne zaboravi normalizaciju (dijeli sa sumom svih exp-ova)

#### Zadatak tip 2: Brojanje parametara modela s adaptivnim baznim funkcijama

- Model: h_k(x) = softmax_k(Σ_j w_{j,k} · φ_j(x))
- Razdijeli parametre u dva dijela:
  1. **Parametri baznih funkcija** (prvi sloj): svaka φ_j ima svoj vektor težina za preslikavanje iz ulaznog prostora — dimenzija ovisi o ulaznom prostoru (n+1 ako uključuje dummy)
  2. **Parametri izlaznog sloja** (drugi sloj): svaka klasa k ima težine w_{j,k} za svaku baznu funkciju j
- Bazne funkcije su **zajedničke** za sve klase → prebroji ih samo jednom
- Težine izlaznog sloja su **zasebne** po klasama → K × (broj baznih + 1)
- Ukupno = (parametri svih baznih funkcija) + (parametri izlaznog sloja)
- Pazi: "3 bazne funkcije" znači j = 0, 1, 2, 3 (uključujući dummy φ₀ = 1) ILI j = 1, 2, 3 (bez dummy) — čitaj pažljivo zadatak

---

## Cjelina 8: Stroj potpornih vektora

### 1. Ideja maksimalne margine

**Model SVM-a** — najjednostavniji linearni model (bez aktivacijske funkcije):

$$h(x; w, w_0) = w^T x + w_0$$

**Predikcija:** $y = \text{sgn}(h(x))$, oznake $y \in \{-1, +1\}$

**Margina** = udaljenost hiperravnine do najbližeg primjera sa svake strane.

**Cilj SVM-a:** pronaći hiperravninu koja **maksimizira marginu** → najbolja generalizacija (induktivna pristranost preferencijom).

- Ako su primjeri linearno odvojivi, postoji beskonačno mnogo razdvajajućih hiperravnina
- SVM bira onu koja je **maksimalno udaljena** od obiju klasa
- Geometrijski: hiperravnina je **simetrala spojnice** dviju konveksnih ljusaka klasa

**Teorem o odvajanju hiperravninom:** za dva disjunktna konveksna podskupa u $\mathbb{R}^n$ postoji razdvajajuća hiperravnina.

---

### 2. Formulacija optimizacijskog problema

**Nepredznakovana udaljenost** primjera od hiperravnine:

$$\frac{y^{(i)}(w^T x^{(i)} + w_0)}{\|w\|}$$

**Trik skaliranja:** pretpostavimo da za primjere najbliže hiperravnini vrijedi $y^{(i)}(w^T x^{(i)} + w_0) = 1$. To je moguće jer možemo proizvoljno skalirati $(w_0, w)$ bez promjene hiperravnine.

**Problem maksimalne margine** (konačna formulacija):

$$\arg\min_{w, w_0} \frac{1}{2} \|w\|^2$$

uz ograničenja:

$$y^{(i)}(w^T x^{(i)} + w_0) \geq 1, \quad i = 1, \ldots, N$$

- Ciljna funkcija je **kvadratna** (konveksna)
- Ograničenja su **linearna** (afina)
- Ovo je **kvadratni program** (QP) — poseban slučaj konveksne optimizacije s ograničenjima

---

### 3. Optimizacija uz ograničenja — osnove

**Standardni oblik:**

$$\min f(x) \quad \text{uz} \quad g_i(x) \leq 0, \quad h_i(x) = 0$$

- $f(x)$ — ciljna funkcija
- $g_i(x)$ — ograničenja nejednakosti
- $h_i(x)$ — ograničenja jednakosti
- **Ostvarivo područje** (feasible region) = skup točaka koje zadovoljavaju sva ograničenja

**Kvadratni program (QP):** ciljna funkcija je kvadratna, ograničenja su afina → konveksan problem.

---

### 4. Lagrangeova funkcija

Kombiniramo ciljnu funkciju i ograničenja u jednu funkciju:

$$L(x, \alpha, \beta) = f(x) + \sum_{i=1}^{m} \alpha_i g_i(x) + \sum_{i=1}^{p} \beta_i h_i(x)$$

- $\alpha_i \geq 0$ — Lagrangeovi multiplikatori za ograničenja nejednakosti
- $\beta_i$ — Lagrangeovi multiplikatori za ograničenja jednakosti
- Rješenje = **stacionarna točka** (sedlo): minimum po x, maksimum po α, β

**Ograničenja jednakosti:** u optimumu gradijenti ∇f i ∇h su kolinearni → $\nabla f + \beta \nabla h = 0$

**Ograničenja nejednakosti:**
- Ograničenje **neaktivno** (minimum unutar ostvarivog područja): $\alpha = 0$
- Ograničenje **aktivno** (minimum na granici): $g(x) = 0$, $\alpha > 0$

---

### 5. KKT uvjeti (Karush-Kuhn-Tucker)

U točki rješenja vrijede:

1. $g_i(x) \leq 0$ (ograničenja nejednakosti zadovoljena)
2. $h_i(x) = 0$ (ograničenja jednakosti zadovoljena)
3. $\alpha_i \geq 0$ (nenegativnost multiplikatora)
4. $\alpha_i g_i(x) = 0$ — **komplementarna labavost**: ili je $\alpha_i = 0$ (neaktivno) ili je $g_i(x) = 0$ (aktivno)

---

### 6. Lagrangeova dualnost

**Načelo dualnosti:**
- **Primarni problem:** minimizacija f(x)
- **Dualni problem:** nalaženje donje ograde primarnog problema

**Dualna Lagrangeova funkcija:**

$$\tilde{L}(\alpha, \beta) = \min_x L(x, \alpha, \beta)$$

- Za konveksne probleme vrijedi **jaka dualnost**: procjep dualnosti = 0
- Rješenje primarnog = rješenje dualnog problema
- Rješenje je u **točki sedla**: min po x, max po α, β

**Dualni problem:**

$$\max_{\alpha, \beta} \tilde{L}(\alpha, \beta) \quad \text{uz} \quad \alpha_i \geq 0$$

---

### 7. Dualni problem SVM-a

**Lagrangeova funkcija za SVM:**

$$L(w, w_0, \alpha) = \frac{1}{2}\|w\|^2 - \sum_{i=1}^{N} \alpha_i \left[ y^{(i)}(w^T x^{(i)} + w_0) - 1 \right]$$

**Deriviranje po primarnim varijablama:**

$$\frac{\partial L}{\partial w} = 0 \Rightarrow w = \sum_{i=1}^{N} \alpha_i y^{(i)} x^{(i)}$$

$$\frac{\partial L}{\partial w_0} = 0 \Rightarrow \sum_{i=1}^{N} \alpha_i y^{(i)} = 0$$

> **Ključna jednadžba:** $w = \sum \alpha_i y^{(i)} x^{(i)}$ — težine su linearna kombinacija primjera!

**Dualni optimizacijski problem:**

$$\max_\alpha \sum_{i=1}^{N} \alpha_i - \frac{1}{2} \sum_{i=1}^{N} \sum_{j=1}^{N} \alpha_i \alpha_j y^{(i)} y^{(j)} (x^{(i)})^T x^{(j)}$$

uz ograničenja:

$$\alpha_i \geq 0, \quad \sum_{i=1}^{N} \alpha_i y^{(i)} = 0$$

**KKT uvjeti za SVM:**

$$\alpha_i \left[ y^{(i)} h(x^{(i)}) - 1 \right] = 0$$

---

### 8. Dualni model i potporni vektori

**Dualni model:**

$$h(x) = \sum_{i=1}^{N} \alpha_i y^{(i)} x^T x^{(i)} + w_0$$

- Predikcija se temelji na **skalarnim produktima** ulaznog primjera sa svim primjerima iz D
- Skalarni produkt = mjera **sličnosti** između vektora

**Potporni vektori** — iz komplementarne labavosti:

$$\alpha_i (y^{(i)} h(x^{(i)}) - 1) = 0 \Rightarrow \alpha_i = 0 \text{ ili } y^{(i)} h(x^{(i)}) = 1$$

- Ako $\alpha_i = 0$ → primjer **ne utječe** na model (nije potporni vektor)
- Ako $\alpha_i > 0$ → primjer leži **točno na margini** → to je **potporni vektor**

> **Ključno:** hiperravnina je definirana samo potpornim vektorima. Svi ostali primjeri su irelevantni za model → **rijetki model** (efikasna predikcija).

**Usporedba primarnog i dualnog:**

| Svojstvo | Primalni | Dualni |
|----------|---------|--------|
| Varijable | $w, w_0$ (n+1 varijabli) | $\alpha$ (N varijabli) |
| Pohranjujemo | Vektor težina w | Potporne vektore + α |
| Isplativo kad | N >> n | N << n |
| Složenost QP | O(n³) | O(N²) s SMO algoritmom |

---

### 9. Ključni pojmovi

| Pojam | Opis |
|-------|------|
| **Margina** | Udaljenost hiperravnine do najbližeg primjera |
| **Maksimalna margina** | Induktivna pristranost SVM-a: hiperravnina s najvećom marginom |
| **Konveksna ljuska** | Najmanji konveksni skup koji sadrži sve primjere klase |
| **Kvadratni program (QP)** | Optimizacijski problem s kvadratnom ciljnom funkcijom i afinim ograničenjima |
| **Lagrangeova funkcija** | $L = f(x) + \sum \alpha_i g_i(x)$ — ciljna funkcija + ograničenja |
| **Lagrangeovi multiplikatori** | $\alpha_i$ — dualne varijable, po jedna za svako ograničenje |
| **KKT uvjeti** | Nužni uvjeti u točki rješenja (uključujući komplementarnu labavost) |
| **Komplementarna labavost** | $\alpha_i g_i(x) = 0$ — ili je ograničenje neaktivno ili je na granici |
| **Jaka dualnost** | Primarni i dualni problem imaju isto rješenje (nema procjepa) |
| **Potporni vektori** | Primjeri s $\alpha_i > 0$, leže na margini, jedini definiraju hiperravninu |
| **SMO** | Sequential Minimal Optimization — efikasan algoritam za dualni QP |
| **Dualni model** | $h(x) = \sum \alpha_i y^{(i)} x^T x^{(i)} + w_0$ — predikcija temeljem sličnosti s primjerima |

---

### 📝 Teorijska ispitna pitanja

#### Pitanje 1
**Kod SVM-a, problem maksimalne margine sveo se na problem minimizacije izraza ½||w||² uz određena ograničenja. Zašto minimizacija ovog izraza daje maksimalnu marginu?**

- A) ✅ Što je vektor w kraći, to je manja vrijednost h(x), pa primjeri moraju biti što dalje da bi vrijedilo h(x) = ±1, a to znači da je margina šira
- B) Što je vektor w kraći, to je manja udaljenost d primjera od hiperravnine, a to efektivno znači da je margina šira jer je margina fiksna a udaljenosti d se smanjuju
- C) Što je vektor w kraći, to je manja vrijednost h(x), ali je težina w₀ konstantna, pa se udaljenosti između hiperravnine i primjera povećavaju, što znači da se margina širi
- D) Što je vektor w kraći, to je veća udaljenost d primjera od hiperravnine, što znači da se potporni vektori udaljavaju od hiperravnine, a to znači da margina postaje šira

> **Objašnjenje:** Margina = 2/||w||. Minimizacija ||w||² znači kraći w, a time je h(x) = wᵀx + w₀ manji. Da bi i dalje vrijedilo y⁽ⁱ⁾h(x⁽ⁱ⁾) ≥ 1 za najbliže primjere, oni moraju biti dalje od hiperravnine → margina je šira.

---

#### Pitanje 2
**Kod optimizacije SVM-a iskoristili smo Lagrangeovu dualnost. Kako u konačnici glasi optimizacijski problem tvrde margine u dualnoj formulaciji (ako zanemarimo ograničenja)?**

- A) argmin_α max_{w,w₀} L(w, w₀, α)
- B) argmax_{w,w₀} min_α L(w, w₀, α)
- C) argmin_{w,w₀} max_α L(w, w₀, α)
- D) ✅ argmax_α min_{w,w₀} L(w, w₀, α)

> **Objašnjenje:** Dualna funkcija L̃(α) = min_{w,w₀} L(w, w₀, α). Dualni problem traži max po α te dualne funkcije, dakle argmax_α min_{w,w₀} L. Rješenje je u točki sedla — min po primarnim, max po dualnim varijablama.

---

#### Pitanje 3
**Po čemu se induktivna pristranost algoritma SVM (tvrda margina) razlikuje od induktivne pristranosti algoritma perceptrona?**

- A) SVM ima pristranost preferencijom kojom maksimizira marginu, dok perceptron nema induktivnu pristranost preferencijom već samo pristranost jezika
- B) Imaju istu pristranost preferencijom, a to je da primjeri moraju biti linearno odvojivi, no SVM ima dodatnu pristranost ograničenjem u vidu optimizacijskih ograničenja
- C) ✅ Razlikuju se po pristranosti preferencijom, jer perceptron ne maksimizira marginu, premda se može dogoditi da pronađe rješenje koje maksimizira marginu
- D) Imaju istu pristranost jezika, a pristranost preferencijom također će biti ista ako se oba optimiraju gradijentnim spustom s istim početnim težinama i istom stopom učenja

> **Objašnjenje:** Oba modela imaju istu pristranost jezika (linearni modeli). Razlika je u pristranosti preferencijom: SVM eksplicitno maksimizira marginu, dok perceptron samo traži bilo koju razdvajajuću hiperravninu (može slučajno naći onu s max marginom, ali to nije garantirano).

---

#### Pitanje 4
**Pretpostavili smo uvjet linearne odvojivosti: ∀(x⁽ⁱ⁾, y⁽ⁱ⁾) ∈ D, y⁽ⁱ⁾h(x⁽ⁱ⁾) ≥ 0. Koliko hipoteza zadovoljava ovaj uvjet, i kako algoritam SVM odabire jednu od njih?**

- A) Beskonačno mnogo hipoteza, međutim samo za jednu vrijedi yh(x) = 1 za najbliže, i to je hipoteza koju SVM odabire
- B) Konačan broj hipoteza koje su linearno odvojive, a SVM između njih odabire onu jednu koja minimizira kvadrat vektora težina
- C) ✅ Beskonačno mnogo hipoteza, a SVM odabire onu jednu koja minimizira kvadrat vektora težina te koja ispravno klasificira sve primjere, uz uvjet da h(x) nije u intervalu (−1, +1)
- D) Konačan broj hipoteza koje se razlikuju samo po faktoru koji množi težine (w, w₀), pa SVM odabire onu jednu za koju vrijedi yh(x) ≥ 1 za sve primjere

> **Objašnjenje:** Postoji beskonačno mnogo razdvajajućih hiperravnina. SVM bira onu s minimalnim ||w||² (max margina), što znači da najbliži primjeri zadovoljavaju yh(x) = 1, a nijedan primjer nema h(x) ∈ (−1, +1).

---

#### Pitanje 5
**Konceptualno, kada će primjer x u dualnoj formulaciji SVM-a biti klasificiran u pozitivnu klasu?**

- A) Ako je linearna kombinacija značajki iz x s pozitivnim težinama veća ili jednaka linearnoj kombinaciji značajki iz x s negativnim težinama
- B) ✅ Ako je vektor x po skalarnom umnošku sličniji potpornim vektorima s pozitivnom oznakom nego potpornim vektorima s negativnom oznakom
- C) Ako je skalarni umnožak vektora x i vektora oznaka y veća od praga definiranog parametrom w₀
- D) Ako većina od ukupno α primjera iz skupa za učenje koji su po euklidskoj udaljenosti najbliži primjeru x ima pozitivnu oznaku

> **Objašnjenje:** Dualni model: h(x) = Σ αᵢ yⁱ xᵀx⁽ⁱ⁾ + w₀. Predikcija ovisi o skalarnim produktima (sličnosti) s potpornim vektorima. Ako je x sličniji pozitivnim potpornim vektorima, suma je pozitivna → pozitivna klasa.

---

#### Pitanje 6
**Što je nužan i dovoljan uvjet da klasifikacijski problem bude rješiv SVM-om s tvrdom marginom?**

- A) Primjeri iz obje klase trebaju činiti konveksne skupove u ulaznom prostoru
- B) Najbliži primjeri iz suprotnih klasa moraju biti u vrhovima konveksnih ljusaka
- C) Barem jedna spojnica između primjera jedne klase treba biti unutar konveksne ljuske druge klase
- D) ✅ Konveksne ljuske dviju klasa ne smiju se preklapati (trebaju biti disjunktne)

> **Objašnjenje:** Tvrda margina zahtijeva linearnu odvojivost. Geometrijski, to znači da konveksne ljuske dviju klasa moraju biti disjunktne — tek tada postoji razdvajajuća hiperravnina (teorem o odvajanju hiperravninom).

---

### 🧮 Napomene za problemske zadatke

#### Zadatak tip 1: Usporedba margine nakon ispravke oznake primjera
- Trenirati SVM na originalnom i ispravljenom skupu → naći marginu = 2/||w|| za oba slučaja
- Potporni vektori su oni najbliži granici; uklanjanje/ispravka jednog primjera može drastično promijeniti marginu
- Omjer novih i starih margina daje koliko je puta šira

#### Zadatak tip 2: Izvođenje dualnih parametara α iz primalnog rješenja w
- Iz primalnog: $w = \sum \alpha_i y^{(i)} x^{(i)}$ — sustav jednadžbi za α
- Matrica dizajna X sadrži primjere u redcima; stupci su značajke (s jedinicom za w₀)
- KKT: $\alpha_i [y^{(i)}(w^T x^{(i)} + w_0) - 1] = 0$ — ako primjer nije na margini, α = 0
- Prvo izračunati h(x⁽ⁱ⁾) = wᵀx⁽ⁱ⁾ za svaki primjer i provjeriti koji leže na margini (yh = 1)
- Samo potporni vektori (α > 0) doprinose; riješiti sustav za te α

#### Zadatak tip 3: Predikcija SVM-a sa skaliranim značajkama
- Standardizacija: $x_j' = (x_j - \mu_j) / \sigma_j$
- Model je naučen na skaliranim podacima → izlaz modela se **ne mijenja** skaliranjem (jer je to ista transformacija)
- Ali kod predikcije treba skalirati novi primjer istim parametrima (μ, σ) prije umetanja u model
- Izlaz modela: $h(x') = \sum \alpha_i y^{(i)} (x')^T x'^{(i)} + w_0$

#### Zadatak tip 4: Usporedba udaljenosti od granice za SVM, LR i LINR
- SVM maksimizira marginu → potporni vektori na margini, ostali dalje
- LR daje probabilistički izlaz → granica gdje σ(wᵀx) = 0.5
- LINR (linearna regresija za klasifikaciju) — granica gdje wᵀx = 0 (prag 0.5 za oznake 0/1) ili wᵀx = 0 za oznake ±1
- Za konkretan primjer: izračunati udaljenost od granice svakog modela i usporediti
- SVM margina je "tvrda" — primjeri koji nisu potporni vektori mogu biti daleko od granice

---

## Cjelina 9: Stroj potpornih vektora II

### 1. Meka margina — motivacija

**Problem tvrde margine:**
- Zahtijeva linearnu odvojivost primjera → ako primjeri nisu linearno odvojivi, **nema rješenja** (ostvarivo područje je prazan skup)
- Čak i ako su linearno odvojivi, šum može uzrokovati usku marginu → loša generalizacija

**Zašto preslikavanje u viši prostor nije dovoljno:**
1. Nema garancije da ćemo naći φ koja daje linearno odvojiv problem
2. Ako forsiramo odvojivost u visokoj dimenziji → **prenaučenost** (nelinearna granica previše prilagođena šumu)

**Ideja meke margine (soft margin):** dopustiti da neki primjeri uđu u marginu ili budu pogrešno klasificirani, ali kazniti takve situacije.

---

### 2. Rezervne varijable (slack variables)

Modificirana ograničenja:

$$y^{(i)}(w^T x^{(i)} + w_0) \geq 1 - \xi_i, \quad \xi_i \geq 0$$

**Interpretacija ξᵢ:**

| Vrijednost ξᵢ | Situacija | Opis |
|---------------|-----------|------|
| $\xi_i = 0$ | Ispravno klasificiran, izvan margine | $y^{(i)}h(x^{(i)}) \geq 1$ |
| $0 < \xi_i < 1$ | Unutar margine, ispravna strana | $0 < y^{(i)}h(x^{(i)}) < 1$ |
| $\xi_i = 1$ | Točno na granici | $y^{(i)}h(x^{(i)}) = 0$ |
| $\xi_i > 1$ | Pogrešna strana granice | $y^{(i)}h(x^{(i)}) < 0$ |
| $\xi_i > 2$ | Pogrešna strana + izvan margine s krive strane | Još dalje od granice |

> **Ključno:** $\xi_i = |y^{(i)} - h(x^{(i)})|$ za pogrešno klasificirane primjere; $\xi_i = 0$ za ispravne.

---

### 3. Optimizacijski problem meke margine

$$\arg\min_{w, w_0, \xi} \left\{ \frac{1}{2} \|w\|^2 + C \sum_{i=1}^{N} \xi_i \right\}$$

uz ograničenja:

$$y^{(i)}(w^T x^{(i)} + w_0) \geq 1 - \xi_i, \quad \xi_i \geq 0, \quad i = 1, \ldots, N$$

**Hiperparametar C > 0** — kompromis između širine margine i tvrdoće margine:

| Veći C | Manji C |
|--------|---------|
| Više kažnjava pogreške | Manje kažnjava pogreške |
| Tvrđa (uža) margina | Mekša (šira) margina |
| Složeniji model | Jednostavniji model |
| Sklonost prenaučenosti | Sklonost podnaučenosti |

> **Napomena:** Varijable ξᵢ su optimizacijske varijable, ali **nisu parametri modela** (za razliku od α u dualnoj formulaciji).

---

### 4. Dualni problem meke margine

**Lagrangeova funkcija:**

$$L(w, w_0, \xi, \alpha, \beta) = \frac{1}{2}\|w\|^2 + C\sum_{i=1}^{N}\xi_i - \sum_{i=1}^{N}\alpha_i\left[y^{(i)}(w^Tx^{(i)}+w_0) - 1 + \xi_i\right] - \sum_{i=1}^{N}\beta_i\xi_i$$

**KKT uvjeti (6 uvjeta):**
1. $y^{(i)}(w^Tx^{(i)}+w_0) \geq 1 - \xi_i$
2. $\xi_i \geq 0$
3. $\alpha_i \geq 0$
4. $\beta_i \geq 0$
5. $\alpha_i(y^{(i)}(w^Tx^{(i)}+w_0) - 1 + \xi_i) = 0$ — komplementarna labavost
6. $\beta_i \xi_i = 0$

**Deriviranje po primarnim varijablama:**

$$\frac{\partial L}{\partial w} = 0 \Rightarrow w = \sum \alpha_i y^{(i)} x^{(i)}$$

$$\frac{\partial L}{\partial w_0} = 0 \Rightarrow \sum \alpha_i y^{(i)} = 0$$

$$\frac{\partial L}{\partial \xi_i} = 0 \Rightarrow \alpha_i = C - \beta_i \Rightarrow \alpha_i \leq C$$

**Dualna Lagrangeova funkcija** — ista kao kod tvrde margine!

$$\tilde{L}(\alpha) = \sum_{i=1}^{N}\alpha_i - \frac{1}{2}\sum_{i=1}^{N}\sum_{j=1}^{N}\alpha_i\alpha_j y^{(i)}y^{(j)}(x^{(i)})^Tx^{(j)}$$

**Dualni problem:**

$$\max_\alpha \tilde{L}(\alpha) \quad \text{uz} \quad 0 \leq \alpha_i \leq C, \quad \sum \alpha_i y^{(i)} = 0$$

> **Jedina razlika od tvrde margine:** dodana gornja ograda $\alpha_i \leq C$ (kutijasta ograničenja, box constraints).

---

### 5. Potporni vektori kod meke margine

**Predikcija** (ista kao tvrda margina):

$$h(x) = \sum_{i=1}^{N} \alpha_i y^{(i)} x^T x^{(i)} + w_0$$

**Klasifikacija potpornih vektora:**

| Uvjet | Tip | Opis |
|-------|-----|------|
| $\alpha_i = 0$ | Nije potporni vektor | Primjer ne utječe na model |
| $0 < \alpha_i < C$ | Potporni vektor **na margini** | $y^{(i)}h(x^{(i)}) = 1$ |
| $\alpha_i = C$ | Potporni vektor **unutar/preko margine** | $y^{(i)}h(x^{(i)}) \leq 1$ |

> **Napomena:** Iz KKT: ako $\alpha_i < C$ → $\beta_i > 0$ → $\xi_i = 0$ → primjer na margini. Ako $\alpha_i = C$ → $\beta_i = 0$ → $\xi_i \geq 0$ → primjer može biti unutar margine ili pogrešno klasificiran.

---

### 6. Gubitak zglobnice (hinge loss)

**Veza s regulariziranom pogreškom** — ciljna funkcija meke margine:

$$\frac{1}{2}\|w\|^2 + C\sum \xi_i$$

Ovo je ekvivalentno L2-regulariziranoj empirijskoj pogrešci:

$$E_R(w|\mathcal{D}) = \sum_{i=1}^{N} L(y^{(i)}, h(x^{(i)})) + \frac{\lambda}{2}\|w\|^2$$

uz $\lambda = 1/C$.

| Izraz u SVM-u | Odgovarajući koncept |
|---------------|---------------------|
| $\frac{1}{2}\|w\|^2$ | L2-regularizacija (šira margina = manja složenost) |
| $C\sum \xi_i$ | Empirijska pogreška (kazneni izraz) |

**Funkcija gubitka zglobnice:**

$$L(y, h(x)) = \max(0, 1 - y \cdot h(x))$$

- Ako $yh(x) \geq 1$ → gubitak = 0 (ispravno klasificiran, izvan margine)
- Ako $yh(x) < 1$ → gubitak = $1 - yh(x)$ (linearno raste)

**Ukupna pogreška SVM-a:**

$$E(w|\mathcal{D}) = \sum_{i=1}^{N} \max(0, 1 - y^{(i)}w^Tx) + \frac{\lambda}{2}\|w\|^2$$

---

### 7. Usporedba funkcija gubitka

| Funkcija gubitka | Izraz | Konveksna? | Surogatna za 0-1? |
|------------------|-------|------------|-------------------|
| **0-1 gubitak** | $\mathbb{1}[yh(x) < 0]$ | Ne | — |
| **Kvadratni** | $(y - h(x))^2$ | Da | Da (ali kažnjava i dobro klasificirane) |
| **Perceptron** | $\max(0, -yh(x))$ | Da | Da |
| **Logistički** | $\ln(1 + e^{-yh(x)})$ | Da | Da |
| **Zglobnica** | $\max(0, 1 - yh(x))$ | Da | Da |

**Zglobnica vs perceptron:** isti oblik, ali zglobnica pomaknuta udesno za 1 → kažnjava i primjere unutar margine ($0 < yh(x) < 1$)

**Zglobnica vs logistički gubitak:** zglobnica **ne kažnjava** ispravno klasificirane primjere izvan margine → rijeđa rješenja (više α = 0)

> **Zaključak:** Pogreška SVM-a = L2-regularizirano očekivanje gubitka zglobnice. Optimizacija se može provesti i SGD-om (uz podgradijent).

---

### 8. Alternativni algoritmi SVM-a

| Algoritam | Jezgre? | Optimizacija | Složenost |
|-----------|---------|-------------|-----------|
| **Platt SMO** | Da | Dualni QP (batch) | O(N²) |
| **LibLinear** | Ne (linearna granica) | Primalni | O(Nn) |
| **Pegasos** | Da | Primalni SGD | O(1/λε) |
| **Koordinatni spust** | Razl. | Primalni ili dualni | Razl. |

---

### 9. Praktične napomene za SVM

**Hiperparametar C:**
- SVM je **vrlo osjetljiv** na C
- Ne optimirati C na skupu za učenje (veći C → manja empirijska pogreška → prenaučenost)
- Koristiti **unakrsnu provjeru** za odabir C

**Skaliranje značajki:**
- Skalarni produkt u dualnom modelu → značajke veće skale dominiraju
- **Obavezno** skalirati značajke (max-min normalizacija ili standardizacija)

**Višeklasna klasifikacija:**
- SVM koristi shemu **OVO** (one-vs-one)
- OVR se **ne preporuča** zbog neuravnoteženosti klasa

**Probabilistički izlaz — Plattovo skaliranje:**

$$P(y=1|x) = \sigma(a \cdot h(x) + b)$$

- Parametri a, b optimiraju se na izdvojenom skupu
- Nema teorijsku podlogu (SVM nije probabilistički model)
- Za pouzdane vjerojatnosti → koristiti logističku regresiju

**Nelinearnost:**
- Preslikavanje φ u viši prostor značajki: $h(x) = \sum \alpha_i y^{(i)} \phi(x)^T\phi(x^{(i)}) + w_0$
- Jezgrene funkcije (kernel trick) — tema sljedećeg predavanja

---

### 10. Ključni pojmovi

| Pojam | Opis |
|-------|------|
| **Tvrda margina** | Inzistira na linearnoj odvojivosti — nema rješenja ako primjeri nisu odvojivi |
| **Meka margina** | Dopušta ulazak u marginu i pogrešnu klasifikaciju uz kaznu |
| **Rezervna varijabla (ξᵢ)** | Mjeri koliko primjer krši ograničenje tvrde margine |
| **Hiperparametar C** | Kompromis: veći C → tvrđa margina, složeniji model |
| **Kutijasta ograničenja** | $0 \leq \alpha_i \leq C$ — jedina razlika dualnog problema meke vs tvrde margine |
| **Gubitak zglobnice** | $\max(0, 1 - yh(x))$ — funkcija gubitka SVM-a |
| **Surogatna funkcija gubitka** | Konveksna gornja međa gubitka 0-1 (zglobnica, logistički, kvadratni) |
| **Plattovo skaliranje** | $P(y=1|x) = \sigma(ah(x)+b)$ — probabilistički izlaz za SVM |
| **LibLinear** | Efikasan SVM algoritam za linearnu granicu, O(Nn) |
| **SMO** | Sequential Minimal Optimization — dualni QP algoritam, O(N²) |

---

### 📝 Teorijska ispitna pitanja

#### Pitanje 1
**Koliko primarni optimizacijski problem meke margine ima ukupno ograničenja, a koliko varijabli po kojima optimiramo? (n = broj značajki, N = broj primjera)**

- A) 2N ograničenja i 2n varijabli
- B) N ograničenja i 2N + 1 varijabli
- C) N ograničenja i n + 1 varijabli
- D) ✅ 2N ograničenja i N + n + 1 varijabli

> **Objašnjenje:** Ograničenja: N marginalnih ($y^{(i)}(w^Tx^{(i)}+w_0) \geq 1-\xi_i$) + N nenegativnosti ($\xi_i \geq 0$) = 2N. Varijable: w (n) + w₀ (1) + ξ (N) = N + n + 1.

---

#### Pitanje 2
**Uvjet komplementarne labavosti meke margine: $\alpha_i(y^{(i)}(w^Tx^{(i)}+w_0) - 1 + \xi_i) = 0$. Što možemo zaključiti?**

- A) Da se primjeri koji nisu potporni vektori sigurno nalaze izvan margine
- B) Da se potporni vektori nalaze na margini ili izvan nje, a na pravoj strani granice
- C) Da se primjeri koji nisu potporni vektori nalaze na margini ili unutar margine
- D) ✅ Da se potporni vektori ne nalaze izvan margine na pravoj strani granice

> **Objašnjenje:** Ako $\alpha_i > 0$ (potporni vektor), tada $y^{(i)}h(x^{(i)}) = 1 - \xi_i \leq 1$. Dakle, potporni vektori su na margini ($\xi_i = 0$) ili unutar nje ($\xi_i > 0$) — nikad izvan margine na ispravnoj strani.

---

#### Pitanje 3
**Kako se opreka regularizacije i pogreške manifestira kod optimizacijskog problema meke margine SVM-a?**

- A) ✅ Što je veća vrijednost ||w||², to je margina uža i tim manje primjera ulazi u marginu, pa je tim manji zbroj od ξᵢ
- B) Što je veća vrijednost ||w||⁴ to je model složeniji, no tim je veća nelinearnost granice i to je veći hiperparametar C
- C) Što je manji zbroj od ξᵢ, to više primjera može ući u marginu i tim je veća vrijednost ||w||² te je model manje složenosti
- D) Što je veći zbroj od ξᵢ, to više primjera ulazi u marginu i tim je manja vrijednost ||w||² te je model veće složenosti

> **Objašnjenje:** Veći ||w||² → uža margina → manje primjera unutar margine → manji Σξᵢ. Obrnuto: manji ||w||² → šira margina → više primjera ulazi → veći Σξᵢ. D je netočan jer manji ||w||² znači jednostavniji (ne složeniji) model.

---

#### Pitanje 4
**Ako matrica dizajna ima više redaka nego stupaca (N > n), koja formulacija ima najmanje optimizacijskih varijabli?**

- A) Primarni problem meke margine
- B) ✅ Primarni problem tvrde margine
- C) Dualni problem meke margine
- D) Dualni problem tvrde margine

> **Objašnjenje:** Primarni tvrde: n+1 varijabli. Primarni meke: N+n+1. Dualni tvrde: N. Dualni meke: N. Kad N > n, najmanji broj varijabli ima primarni tvrde margine (n+1).

---

#### Pitanje 5
**Kada NIJE potrebno napraviti skaliranje značajki kod SVM-a?**

- A) ✅ Kada se koristi RBF jezgra sa Mahalanobisovom udaljenošću, jer ta udaljenost uzima u obzir varijancu značajki
- B) Kada se koristi linearna jezgra i značajke su centrirane oko nule, jer se onda ne računa skalarni produkt između značajki
- C) Kada se koristi dualna formulacija SVM-a i algoritam SMO, jer se tada implicitno provodi L1-regularizacija
- D) Kada se koristi Gaussova jezgrena funkcija, jer ta jezgra implicitno inducira beskonačnodimenzijski prostor značajki

> **Objašnjenje:** Mahalanobisova udaljenost normalizira po varijancu značajki ($d_M = \sqrt{(x-\mu)^T\Sigma^{-1}(x-\mu)}$), pa su razlike u skalama već uračunate. Kod svih ostalih pristupa skaliranje je potrebno.

---

### 🧮 Napomene za problemske zadatke

#### Zadatak tip 1: Usporedba tvrde i meke margine — koliko je meka veća
- Tvrda margina: margina = 2/||w|| gdje w zadovoljava yh(x) ≥ 1 za sve primjere
- Meka margina (C = 1): iz dualnih koeficijenata α rekonstruirati w = Σ αᵢ yⁱ xⁱ
- Potporni vektori su oni s αᵢ > 0; kod meke margine αᵢ = C znači primjer unutar/preko margine
- Izračunati ||w|| za oba slučaja, margina = 2/||w||, i naći omjer
- Skicirati obje margine u ulaznom prostoru za vizualnu provjeru

#### Zadatak tip 2: Računanje empirijske pogreške SVM-a (gubitak zglobnice)
- Empirijska pogreška = $\sum \max(0, 1 - y^{(i)} w^T x^{(i)}) + \frac{\lambda}{2}\|w\|^2$ gdje λ = 1/C
- Iz dualnih koeficijenata: $w = \sum \alpha_i y^{(i)} x^{(i)}$ i zadan w₀
- Za svaki primjer izračunati $y^{(i)}(w^T x^{(i)} + w_0)$ i primijeniti hinge loss: max(0, 1 − yh)
- Zbrojiti sve gubitke + regularizacijski član λ/2 · ||w||²
- Paziti na razliku: h(x) = wᵀx + w₀ koristi se za gubitak, ali regularizacija je samo na w (ne w₀)

---

## Cjelina 10: Jezgrene metode

### 1. Jezgrene funkcije — pojam i motivacija

**Jezgrena funkcija** (kernel function):

$$\kappa : \mathcal{X} \times \mathcal{X} \to \mathbb{R}$$

- Mjeri **sličnost** između dva primjera
- Tipično: $\kappa(x, x') \geq 0$ (nenegativna) i $\kappa(x, x') = \kappa(x', x)$ (simetrična)
- Ako je $\kappa : \mathcal{X} \times \mathcal{X} \to [0, 1]$ i $\kappa(x, x) = 1$ → **mjera sličnosti**

**Motivacija:** Ponekad je lakše izračunati sličnost između primjera nego ih prikazati kao vektore značajki:
- Znakovni nizovi (riječi, DNK) → jezgre znakovnih nizova (string kernels)
- Stabla (sintaktički grafovi) → jezgre stabala (tree kernels)
- Grafovi (molekule) → jezgre grafova (graph kernels)

---

### 2. Standardne jezgrene funkcije

| Jezgra | Izraz | Napomena |
|--------|-------|----------|
| **Linearna** | $\kappa(x, x') = x^T x'$ | Skalarni produkt, linearan model |
| **Polinomijalna** | $\kappa(x, x') = (x^T x' + 1)^p$ | Uključuje interakcije do stupnja p |
| **Gaussova (RBF)** | $\kappa(x, x') = \exp(-\gamma\|x-x'\|^2)$ | $\gamma = 1/2\sigma^2$, beskonačnodimenzijski prostor |
| **Eksponencijalna** | $\kappa(x, x') = \exp(-\gamma\|x-x'\|)$ | Slična Gaussovoj, bez kvadriranja norme |
| **Inverzna kvadratna** | $\kappa(x, x') = \frac{1}{1+\|x-x'\|^2}$ | Radijalna bazna funkcija |

**Radijalna bazna funkcija (RBF)** — općenito:

$$\kappa(x, x') = f(\|x - x'\|)$$

- Sličnost ovisi samo o **udaljenosti** između primjera

**Gaussova jezgra — parametri:**
- $\sigma^2$ = širina pojasa (bandwidth): veći $\sigma^2$ → šira distribucija → udaljeniji primjeri su sličniji
- $\gamma = 1/2\sigma^2$ = preciznost: veći $\gamma$ → uža distribucija → striktniji kriterij sličnosti

**Mahalanobisova udaljenost** — poopćenje euklidske:

$$\kappa(x, x') = \exp\left(-\frac{1}{2}(x-x')^T \Sigma^{-1} (x-x')\right)$$

- $\Sigma$ = kovarijacijska matrica → modelira korelacije između značajki
- Ako $\Sigma = I$ → degenerira na euklidsku udaljenost
- **Ne zahtijeva skaliranje značajki** (varijance su uračunate)

---

### 3. Jezgreni strojevi (kernel machines)

**Ideja:** Bazne funkcije definirati kao jezgrene funkcije s referentnim primjerima:

$$\phi_j(x) = \kappa(x, \mu_j)$$

**Preslikavanje u prostor značajki:**

$$\phi(x) = (1, \kappa(x, \mu_1), \kappa(x, \mu_2), \ldots, \kappa(x, \mu_m))$$

- Jezgreni stroj = poopćeni linearni model s ovako definiranim φ
- Može se koristiti s logističkom regresijom, linearnom regresijom, SVM-om...

**Odabir referentnih primjera μⱼ:**
- Uniformno po prostoru — problematično za visoke dimenzije (eksponencijalno mnogo točaka)
- **Iz skupa za učenje:** $\mu_j = x^{(j)}$ → dimenzija prostora značajki = N (broj primjera)

**Smanjenje broja referentnih primjera:**
- **L1-regularizacija** → pritisne neke težine na 0 → izbaci nepotrebne jezgre → **rijetki jezgreni strojevi** (sparse kernel machines, L1VM)
- L2-regularizacija → ne daje rijetki model (L2VM)

---

### 4. Jezgreni trik (kernel trick)

**Opažanje:** U dualnom SVM-u, primjeri se pojavljuju **isključivo** u obliku skalarnog produkta:

- **Model:** $h(x) = \sum \alpha_i y^{(i)} x^T x^{(i)} + w_0$
- **Optimizacija:** $\sum \alpha_i - \frac{1}{2} \sum_i \sum_j \alpha_i \alpha_j y^{(i)} y^{(j)} (x^{(i)})^T x^{(j)}$

**Trik:** Zamijeniti skalarni produkt **jezgrenom funkcijom**:

$$x^T x^{(i)} \longrightarrow \kappa(x, x^{(i)})$$

gdje je $\kappa(x, x') = \phi(x)^T \phi(x')$ — jezgra odgovara skalarnom produktu u prostoru značajki.

**Kerneliziran SVM model:**

$$h(x) = \sum_{i=1}^{N} \alpha_i y^{(i)} \kappa(x, x^{(i)}) + w_0$$

**Tri prednosti inverznog oblikovanja:**

| Prednost | Objašnjenje |
|----------|-------------|
| **Smanjenje složenosti** | Izračun κ često jednostavniji nego φ(x)ᵀφ(x') |
| **Jednostavnost** | Lakše definirati sličnost nego preslikavanje, osobito za strukturirane podatke |
| **Veća ekspresivnost** | Prostor značajki može biti beskonačnodimenzijski |

> **Ključno:** Nema eksplicitnog preslikavanja — preslikavanje je **implicitno**!

---

### 5. Mercerove jezgre (valjane jezgre)

**Problem:** Ne može se svaka jezgrena funkcija koristiti u jezgrenom triku. Jezgra mora odgovarati skalarnom produktu u nekom prostoru značajki.

**Mercerova (valjana) jezgra** = pozitivno definitna jezgra — jezgra za koju postoji preslikavanje φ takvo da:

$$\kappa(x, x') = \phi(x)^T \phi(x')$$

**Jezgrena matrica K:**

$$K_{ij} = \kappa(x^{(i)}, x^{(j)}), \quad K \in \mathbb{R}^{N \times N}$$

**Uvjet:** Jezgra je Mercerova ⟺ matrica K je **pozitivno semidefinitna** ($x^TAx \geq 0$, ∀x)

- Tada je K = ΦΦᵀ — **Gramova matrica**
- Prostor značajki je **Hilbertov prostor** H (vektorski prostor s definiranim skalarnim produktom, moguće beskonačnodimenzijski)

**Koje su jezgre Mercerove?**
- Linearna: ✅ (trivijalno, φ(x) = x)
- Polinomijalna: ✅
- Gaussova RBF: ✅ (preslikava u beskonačnodimenzijski prostor)
- Euklidska norma $\kappa(x,x') = \|x - x'\|$: ❌ (nije Mercerova)

---

### 6. Gaussova jezgra — prostor značajki

**Gramova matrica** K za Gaussovu jezgru je **punog ranga** → vektori φ(x) su linearno nezavisni.

**Posljedice:**
- Prostor značajki je **beskonačnodimenzijski** (toliko dimenzija koliko primjera, a nema gornje granice)
- Za dovoljno velik γ: svi primjeri u prostoru značajki postaju **međusobno ortogonalni** ($\kappa \to 0$ za $x \neq x'$)

**Efekt parametra γ:**

| Mali γ | Veliki γ |
|--------|----------|
| Široka distribucija | Uska distribucija |
| κ → 1 za sve parove | κ → 0 za sve parove (osim x = x') |
| Primjeri grupirani zajedno | Primjeri međusobno ortogonalni |
| Sklonost **podnaučenosti** | Sklonost **prenaučenosti** |

> **Ključno:** Za dovoljno velik γ, svaki primjer je "poslan u svoj vrh" duž ortogonalne osi → uvijek možemo postići savršenu linearnu odvojivost → opasnost od prenaučenosti!

---

### 7. Izgradnja složenijih jezgara

Ako su κ₁ i κ₂ Mercerove, onda su Mercerove i:

| Operacija | Izraz |
|-----------|-------|
| Skaliranje | $\alpha \kappa_1(x,x'), \quad \alpha > 0$ |
| Modulacija funkcijom | $f(x) \kappa_1(x,x') f(x')$ |
| Polinom s poz. koef. | $q(\kappa_1(x,x'))$ |
| Eksponencijal | $\exp(\kappa_1(x,x'))$ |
| Kompozicija | $\kappa_1(\phi(x), \phi(x'))$ |
| **Zbroj** | $\kappa_1(x,x') + \kappa_2(x,x')$ |
| **Umnožak** | $\kappa_1(x,x') \cdot \kappa_2(x,x')$ |

- **Zbroj jezgri** ≈ konkatenacija vektora u prostoru značajki (najjednostavniji način kombiniranja)
- **Učenje s više jezgara** (Multiple Kernel Learning, MKL) — kombiniranje jezgri za složene podatke

---

### 8. Praktične napomene

**Hiperparametri kod SVM-a s jezgrom:**
- Treba optimirati **C** (složenost modela) **i** hiperparametar jezgre (γ za Gaussovu, p za polinomijalnu)
- Parametri su povezani: velik γ → složeniji model → treba manji C
- Optimizacija: **pretraživanje po rešetci** (grid search) s unakrsnom provjerom

**Linearna jezgra — kad koristiti?**
- Kada želimo **rijetki model** (nekoliko potpornih vektora umjesto hrpe težina)
- Prednost kod predikcije (ne kod učenja — ionako treba izračunati sve parove)
- Dualni SMO: O(N²) vs primalni QP: O(n³)

**Aproksimacija jezgrenih funkcija:**
- Problem: jezgrena matrica K je N×N → skupa za velike N
- Rješenje: aproksimativno preslikavanje u prostor značajki + SGD optimizacija

**Ujezgravanje (kernelizacija) algoritama:**
- Jezgreni trik nije samo za SVM — primjenjiv na **svaki algoritam** gdje se primjeri pojavljuju isključivo u obliku skalarnog produkta
- Mogu se ujezgriti: linearna regresija, logistička regresija, i drugi

---

### 9. Ključni pojmovi

| Pojam | Opis |
|-------|------|
| **Jezgrena funkcija** | $\kappa(x,x') \to \mathbb{R}$ — mjeri sličnost dva primjera |
| **Linearna jezgra** | $\kappa = x^Tx'$ — skalarni produkt, linearan model |
| **Polinomijalna jezgra** | $\kappa = (x^Tx'+1)^p$ — uključuje interakcije do stupnja p |
| **Gaussova (RBF) jezgra** | $\kappa = \exp(-\gamma\|x-x'\|^2)$ — beskonačnodimenzijski prostor |
| **Radijalna bazna funkcija** | Jezgra oblika $f(\|x-x'\|)$ — ovisi samo o udaljenosti |
| **Jezgreni stroj** | Poopćeni linearni model s φⱼ(x) = κ(x, μⱼ) |
| **Jezgreni trik** | Zamjena skalarnog produkta Mercerovom jezgrom — implicitno preslikavanje |
| **Mercerova jezgra** | Valjana jezgra: κ = φ(x)ᵀφ(x'), K je pozitivno semidefinitna |
| **Jezgrena matrica K** | $K_{ij} = \kappa(x^{(i)}, x^{(j)})$, N×N simetrična matrica |
| **Gramova matrica** | K = ΦΦᵀ — matrica skalarnih produkata u prostoru značajki |
| **Hilbertov prostor** | Vektorski prostor s definiranim skalarnim produktom, moguće beskonačnodimenzijski |
| **Inverzno oblikovanje** | Izabiremo κ umjesto φ — jednostavnije, efikasnije, ekspresivnije |
| **Grid search** | Pretraživanje po rešetci za optimizaciju hiperparametara (C, γ) |
| **MKL** | Multiple Kernel Learning — kombiniranje više jezgri |

---

### 📝 Teorijska ispitna pitanja

#### Pitanje 1
**Treniramo SVM s nekom jezgrenom funkcijom. Je li moguće izračunati udaljenost primjera od hiperravnine u prostoru značajki?**

- A) Ne, jer u dualnoj formulaciji nemamo vektor značajki
- B) Ne, jer granica između klasa ne mora biti hiperravnina
- C) ✅ Da, ako nismo koristili Gaussovu jezgru ili neku složeniju jezgru koja koristi Gaussovu jezgru kao gradivni blok
- D) Da, ako smo koristili linearnu jezgru, odnosno ako je ulazni prostor jednak prostoru značajki

> **Objašnjenje:** Za jezgre s konačnodimenzijskim prostorom značajki (linearna, polinomijalna) udaljenost se može izračunati. Gaussova jezgra preslikava u beskonačnodimenzijski prostor, pa udaljenost u tom prostoru nije izravno izračunljiva.

---

#### Pitanje 2
**Zašto je dobro da je jezgrena funkcija Mercerova jezgra?**

- A) ✅ Zato što takva jezgra odgovara skalarnom produktu u nekom prostoru značajki, a to je nužno da bismo mogli primijeniti jezgreni trik
- B) Zato što takva jezgra inducira Hilbertov prostor beskonačnodimenzijskih značajki, što daje potencijalno vrlo složene modele
- C) Zato što takva jezgra omogućava da klasifikaciju određujemo na temelju sličnosti između primjera i prototipnih primjera
- D) Zato što takva jezgra nužno daje nenegativne vrijednosti sličnosti između parova primjera

> **Objašnjenje:** Jezgreni trik zamjenjuje φ(x)ᵀφ(x') s κ(x,x'). Da bi to bilo valjano, jezgra mora odgovarati skalarnom produktu u nekom prostoru značajki — upravo to znači da je Mercerova. B je netočan jer Mercerova jezgra ne mora inducirati beskonačnodimenzijski prostor.

---

#### Pitanje 3
**Kakav je utjecaj parametra γ na vrijednost Gaussove jezgrene funkcije κ(x₁, x₂), gdje x₁ ≠ x₂, te na nelinearnost modela jezgrenog stroja?**

- A) Što je γ manja, to je manja κ(x₁,x₂), i to je model manje nelinearan
- B) Što je γ veća, to je veća κ(x₁,x₂), i to je model manje nelinearan
- C) Što je γ manja, to je manja κ(x₁,x₂), i to je model više nelinearan
- D) ✅ Što je γ veća, to je manja κ(x₁,x₂), i to je model više nelinearan

> **Objašnjenje:** κ = exp(−γ||x₁−x₂||²). Veći γ → argument eksponencijale je negativniji → κ manji (primjeri manje slični). Veći γ → uža distribucija → striktniji kriterij sličnosti → primjeri ortogonalniji u prostoru značajki → model više nelinearan (sklonost prenaučenosti).

---

#### Pitanje 4
**Može se dokazati da je Gaussova jezgra Mercerova. Što to znači u matematičkom smislu?**

- A) ∀x₁∀x₂: x₁ᵀx₂ = exp(−γ|φ(x₁) − φ(x₂)|²)
- B) ✅ ∀x₁∀x₂: φ(x₁)ᵀφ(x₂) = exp(−γΔ²) gdje Δ² = (x₁−x₂)ᵀ(x₁−x₂)
- C) ∀x₁∀x₂: φ(x₁ᵀx₂) = exp(−γΔ²), gdje Δ² = (x₁−x₂)ᵀ(x₁−x₂)
- D) ∀x₁∀x₂: (x₁ ≠ x₂) ⟹ exp(−γ|φ(x₁)−φ(x₂)|²) = x₁ᵀx₂

> **Objašnjenje:** Mercerova jezgra znači κ(x₁,x₂) = φ(x₁)ᵀφ(x₂) za neko preslikavanje φ. Za Gaussovu jezgru: φ(x₁)ᵀφ(x₂) = exp(−γ||x₁−x₂||²).

---

#### Pitanje 5
**Koja je prednost primjene jezgrenog trika kad prostor ulaznih primjera nije euklidski vektorski prostor?**

- A) Jezgrenim trikom implicitno se ostvaruje nelinearnost prostora značajki, što povećava kapacitet modela
- B) Umjesto vektorizacije primjera, dovoljno je definirati nelinearnu funkciju preslikavanja iz ulaznog prostora u prostor značajki
- C) Jezgrena funkcija mjeri sličnost između primjera, čime se primjeri efektivno preslikavaju u beskonačnodimenzijski prostor značajki
- D) ✅ Jezgrena funkcija može biti mjera sličnosti između nevektoriziranih primjera, što implicitno inducira vektorski prostor značajki

> **Objašnjenje:** Kad primjeri nisu vektori (stringovi, grafovi...), ne možemo ih izravno vektorizirati. Jezgrena funkcija mjeri sličnost izravno nad strukturiranim primjerima i time implicitno inducira prostor značajki (Hilbertov prostor), bez eksplicitne vektorizacije.

---

#### Pitanje 6
**Po čemu je SVM specifičan u odnosu na općeniti algoritam rijetkoga jezgrenog stroja?**

- A) Zbog L1-regularizacije, mnoge težine modela bit će pritegnute na nulu
- B) Dimenzija prostora značajki ne može biti veća od broja primjera
- C) Broj parametara modela jednak je dimenziji prostora značajki
- D) ✅ Prototipni primjeri odabiru se u okviru optimizacijskog postupka

> **Objašnjenje:** Kod općenitih rijetkih jezgrenih strojeva, referentni primjeri se biraju unaprijed ili L1-regularizacijom. Kod SVM-a, potporni vektori (prototipni primjeri) odabiru se **automatski** tijekom optimizacije (KKT uvjeti, komplementarna labavost) — to je ključna razlika.

---

#### Pitanje 7
**Kažemo da Mercerove jezgrene funkcije implicitno definiraju prostor značajki. Što to znači?**

- A) Klasifikacija primjera je na temelju umnoška jezgrene funkcije za taj primjer i sve druge primjere u skupu za učenje
- B) Jezgrena funkcija između primjera u prostoru značajki jednaka je skalarnom produktu tih primjera u ulaznom prostoru
- C) Broj dimenzija prostora značajki implicitno ovisi o broju klasa u ulaznom prostoru
- D) ✅ Vrijednost jezgrene funkcije nad parom vektora jednaka je skalarnom produktu tih vektora nakon preslikavanja u prostor značajki

> **Objašnjenje:** "Implicitno definirati prostor značajki" znači: κ(x,x') = φ(x)ᵀφ(x') — jezgra daje skalarni produkt u prostoru značajki bez potrebe za eksplicitnim preslikavanjem pomoću φ.

---

### 🧮 Napomene za problemske zadatke

#### Zadatak tip 1: Broj hiperparametara, parametara optimizacije i naučenog modela (jezgreni stroj)
- Hiperparametri: σ² (ili γ) Gaussove jezgre — obično 1 hiperparametar (isti za sve jezgre)
- Parametri za optimizaciju: težine w (m+1, uključujući w₀) — dimenzija prostora značajki + 1
- Naučeni model: potporni vektori (prototipni primjeri) + pripadni α → broj potpornih vektora + w₀
- Paziti na razliku: rijetki jezgreni stroj izbacuje jezgre L1-regularizacijom

#### Zadatak tip 2: Točnost inicijaliziranog jezgrenog stroja s logističkom regresijom
- φ(x) = (1, κ(x, μ₁), κ(x, μ₂), ..., κ(x, μₘ)) — vektor značajki za svaki primjer
- Model: h(x) = σ(wᵀφ(x)) — logistička regresija na preslikane značajke
- Izračunati φ(x) za svaki primjer, zatim wᵀφ(x), pa σ(...), pa zaokružiti na 0/1
- Usporediti s pravom oznakom → postotak točnosti

#### Zadatak tip 3: Gubitak modela jezgrenog stroja (string kernel)
- Jezgreni stroj za znakovne nizove: κ mjeri sličnost (npr. Jaccard, Levenshtein, zajednički podnizovi)
- φ(x) = (1, κ(x, x⁽¹⁾), ..., κ(x, x⁽ᴺ⁾)) — značajke su sličnosti s primjerima iz D
- Gubitak ovisi o modelu: za logističku regresiju cross-entropy, za SVM hinge loss
- Izračunati h(x) = wᵀφ(x), pa primijeniti odgovarajuću funkciju gubitka

#### Zadatak tip 4: Euklidska udaljenost između φ_κ(x) i φ_p(x)
- Polinomijalna jezgra κ(x,z) = (xᵀz)² daje implicitno preslikavanje φ_κ
- Za n=2: φ_κ(x) = (x₁², √2·x₁x₂, x₂²) — izvesti raspisivanjem (xᵀz)²
- Eksplicitni polinom φ_p(x) = (x₁², x₁x₂, x₂²) — bez √2 faktora
- Udaljenost: ||φ_κ(x) − φ_p(x)|| — razlika je u koeficijentima mješovitih članova

#### Zadatak tip 5: Predikcija SVM-a s polinomijalnom jezgrom (jezgreni trik)
- h(x) = Σ αᵢ yⁱ κ(x, x⁽ⁱ⁾) + w₀
- κ(x, z) = (xᵀz + c)ᵖ — izračunati za svaki potporni vektor
- w₀ izračunati iz potpornog vektora s 0 < α < C: y⁽ⁱ⁾h(x⁽ⁱ⁾) = 1

#### Zadatak tip 6: Gubitak zglobnice SVM-a s Gaussovom jezgrom (matrica udaljenosti)
- Iz matrice euklidskih udaljenosti D izračunati κ(x⁽ⁱ⁾, x⁽ʲ⁾) = exp(−γ · D²ᵢⱼ)
- h(x⁽ⁱ⁾) = Σⱼ αⱼ yⱼ κ(x⁽ⁱ⁾, x⁽ʲ⁾) + w₀
- w₀ izračunati iz potpornog vektora na margini (0 < α < C)
- Hinge loss: L = max(0, 1 − y⁽ⁱ⁾h(x⁽ⁱ⁾))

#### Zadatak tip 7: Gubitak zglobnice SVM-a s jezgrenom matricom (grafovi)
- Jezgrena matrica K zadana izravno (κ vrijednosti između svih parova)
- h(x⁽ⁱ⁾) = Σⱼ αⱼ yⱼ Kᵢⱼ + w₀
- w₀ iz potpornog vektora na margini
- Hinge loss: L = max(0, 1 − y⁽ⁱ⁾h(x⁽ⁱ⁾))

#### Zadatak tip 8: Pretraživanje po rešetci — koliko modela ispitati za prenaučenost
- Grid search: sve kombinacije C × γ
- Ako model (C₀, γ₀) je prenaučen, svi modeli s C ≥ C₀ i γ ≥ γ₀ su **sigurno** prenaučeni
- Veći C → složeniji model, veći γ → složeniji model
- Prebrojiti kombinacije (C, γ) gdje C ≥ C₀ i γ ≥ γ₀

#### Zadatak tip 9: Omjer veličina Gramove matrice za OVO vs OVR shemu
- OVO: K klasa → K(K−1)/2 binarnih klasifikatora, svaki s primjerima dviju klasa
- OVR: K klasifikatora, svaki koristi sve primjere (N)
- Gramova matrica je simetrična → dovoljno pohraniti polovicu (bez dijagonale)
- Veličina matrice: n(n−1)/2 za n primjera u jednom klasifikatoru
- Ukupno za shemu: zbrojiti preko svih klasifikatora

---

## Cjelina 11: Neparametarske metode

### 1. Parametarske vs. neparametarske metode

| Svojstvo | Parametarske | Neparametarske |
|----------|-------------|----------------|
| **Hipoteza** | Definirana do na parametre θ | Nije eksplicitno definirana |
| **Broj parametara** | Fiksan (ne ovisi o N) | Ovisi o broju primjera N |
| **Pretpostavka** | Podatci slijede neki model/distribuciju | Ne pretpostavljaju model podataka |
| **Utjecaj primjera** | **Globalan** — svi primjeri utječu na cijelu hipotezu | **Lokalan** — aproksimacija u okolici pohranjenih primjera |
| **Predikcija** | Unaprijed (model naučen) | Na zahtjev → **lijene metode** (lazy methods) |

> **Napomena:** Neparametarski modeli **imaju** parametre, ali nemaju parametre distribucije!

**Induktivna pristranost neparametarskih metoda:** slični primjeri imaju slične oznake.

**Preporuke:**
- Malo podataka i/ili poznat model → **parametarski** postupci
- Mnogo podataka i nepoznat model → **neparametarski** postupci

---

### 2. SVM kao neparametarski model

**Primalna formulacija** → parametarski (parametri: w, w₀ — fiksan broj n+1)

**Dualna formulacija** → neparametarski:

$$h(x) = \sum_{i=1}^{N} \alpha_i y^{(i)} x^T x^{(i)} + w_0$$

- Broj parametara proporcionalan broju **potpornih vektora**, koji ovisi o N
- Prikladno kada N ≪ n (algoritam SMO ima složenost O(N²))

---

### 3. Algoritam k-NN (k najbližih susjeda)

**Neparametarski klasifikacijski algoritam** — predikcija na temelju većinske oznake k najbližih susjeda:

$$h(x) = \arg\max_{j \in \{0,...,K-1\}} \sum_{(x^{(i)}, y^{(i)}) \in NN_k(x)} \mathbb{1}[y^{(i)} = j]$$

**Hiperparametar k:**
- **Manji k** → složeniji model (osjetljiviji na šum, prenaučenost)
- **Veći k** → jednostavniji model (glađa granica, podnaučenost)
- k = 1 → ulazni prostor particioniran u **Voronoijev dijagram**

**Težinski k-NN** — utjecaj primjera ovisi o udaljenosti/sličnosti (kernel):

$$h(x) = \arg\max_{j \in \{0,...,K-1\}} \sum_{i=1}^{N} \kappa(x^{(i)}, x) \cdot \mathbb{1}[y^{(i)} = j]$$

**Mjera udaljenosti:** ne mora biti euklidska (npr. Mahalanobisova udaljenost)

---

### 4. Računalni aspekti k-NN-a

**Problem:** Nalaženje najbližeg susjeda (nearest neighbor search) — skupo za velike N.

**Alternative iscrpnom pretraživanju:**

| Pristup | Metoda | Opis |
|---------|--------|------|
| **Egzaktne** | Ball tree, KD-tree | Indeksiranje prostora primjera |
| **Aproksimativne** | Locally Sensitive Hashing (LSH) | Brže, ali približno |

---

### 5. Prokletstvo dimenzionalnosti (curse of dimensionality)

- S porastom dimenzije n, **sve točke postaju međusobno vrlo udaljene**
- Udaljenosti postaju **nediskriminativne** (svi susjedi podjednako daleko)
- Općenit problem **svih** algoritama u visokodimenzijskim prostorima
- Udio podataka u jediničnoj hiperkocki opada s dimenzijom
- Udaljenost između susjeda raste s dimenzijom

---

### 6. Neparametarska regresija — modeli zaglađivanja

**k-NN smoother** — prosjek vrijednosti k najbližih susjeda:

$$h(x) = \frac{1}{k} \sum_{(x^{(i)}, y^{(i)}) \in NN_k(x)} y^{(i)}$$

**Jezgreno zaglađivanje** (kernel smoothing) — težinski prosjek svih primjera:

$$h(x) = \frac{\sum_{i=1}^{N} \kappa(x^{(i)}, x) \cdot y^{(i)}}{\sum_{i=1}^{N} \kappa(x^{(i)}, x)}$$

- Svaki primjer doprinosi proporcionalno svojoj sličnosti s x
- Bliži primjeri imaju veći utjecaj

---

### 7. Stabla odluke

- **Neparametarski model** — broj parametara (≈ broj razina) raste s brojem primjera
- Ulazni prostor **rekurzivno dijeli** na lokalna područja (dva potprostora)

---

### 8. Ključni pojmovi

| Pojam | Opis |
|-------|------|
| **Parametarski model** | Fiksan broj parametara, ne ovisi o N, globalan utjecaj primjera |
| **Neparametarski model** | Broj parametara ovisi o N, lokalna aproksimacija |
| **Lijene metode** | Predikcija na zahtjev (lazy), bez eksplicitnog učenja modela |
| **k-NN** | Klasifikacija većinskim glasanjem k najbližih susjeda |
| **Voronoijev dijagram** | Particija prostora za k=1 — svaki primjer definira svoju regiju |
| **Težinski k-NN** | Utjecaj susjeda proporcionalan sličnosti (jezgrena funkcija) |
| **Prokletstvo dimenzionalnosti** | U visokim dimenzijama sve udaljenosti postaju slične |
| **k-NN smoother** | Neparametarska regresija: prosjek k najbližih susjeda |
| **Jezgreno zaglađivanje** | Težinski prosjek svih primjera po sličnosti |
| **Ball tree / LSH** | Metode za efikasno nalaženje najbližih susjeda |

---

### 📝 Teorijska ispitna pitanja

#### Pitanje 1
**Algoritam SVM može biti parametarski i neparametarski. Kako rijetkost modela ovisi o hiperparametru C?**

- A) Što je C manji, to je neparametarski model rjeđi, ali to nema utjecaja na rijetkost parametarskog modela jer on nema potporne vektore
- B) Što je C veći, to je neparametarski model manje rijedak, dok je parametarski to rjeđi jer λ pada
- C) ✅ Što je C manji, to je neparametarski model rjeđi, a također je to rjeđi i parametarski model jer λ raste
- D) Što je C veći, to je neparametarski model manje rijedak, dok parametarski model nije rijedak jer ima L2-regularizaciju a ne L1-regularizaciju

> **Objašnjenje:** Manji C → veći λ = 1/C → jača regularizacija → šira margina → manje potpornih vektora (rjeđi dualni/neparametarski model). Istovremeno, veći λ → jača regularizacija u primalnom modelu → više težina blizu nule → rjeđi parametarski model.

---

#### Pitanje 2
**Kako se problem prokletstva dimenzionalnosti u visokodimenzijskim prostorima manifestira kod algoritma k-NN?**

- A) Udaljenosti između primjera se smanjuju i model k-NN postaje sve složeniji
- B) Povećava se broj susjeda u okolini svakog primjera i model k-NN postaje sve jednostavniji
- C) ✅ Svi primjeri su međusobno vrlo udaljeni i gube se razlike u udaljenosti
- D) Broj susjeda k nekog primjera se smanjuje i gube se granice između klasa

> **Objašnjenje:** U visokim dimenzijama sve udaljenosti postaju slične (nediskriminativne) — razlika između najbližeg i najdaljeg susjeda postaje zanemariva. k-NN se oslanja na udaljenosti za pronalaženje susjeda, pa kad su sve udaljenosti podjednake, algoritam gubi sposobnost razlikovanja.

---

#### Pitanje 3
**Što je karakteristika neparametarskih algoritama strojnog učenja?**

- A) Pretpostavljaju vjerojatnosnu distribuciju podataka
- B) ✅ Broj parametara ovisi o broju primjera
- C) Eksplicitno modeliraju granicu između primjera
- D) Svaki primjer ima globalan utjecaj na izgled hipoteze

> **Objašnjenje:** Ključna karakteristika neparametarskih metoda: broj parametara raste s brojem primjera N. A i D opisuju parametarske metode (pretpostavljaju distribuciju, globalan utjecaj).

---

#### Pitanje 4
**Na koji način funkcionira algoritam stabla lopti (ball tree) za ubrzanje k-NN pretraživanja?**

- A) Koristi preslikavanje osjetljivo na lokalne promjene u vektoru kojim se bliske točke pohranjuju u iste pretince
- B) Koristi pretraživanje duž pravca u vektorskome prostoru u smjeru suprotnom od gradijenta funkcije pogreške
- C) ✅ Koristi brzo pretraživu binarnu indeksnu strukturu za particioniranje prostora primjera u preklapajuće regije
- D) Koristi jezgreni trik za izračun euklidske udaljenosti između točke upita i svih drugih točaka u skupu primjera

> **Objašnjenje:** Ball tree koristi binarnu strukturu stabla koja particionira prostor u hipersphere (lopte) koje se mogu preklapati. Time se brzo eliminiraju velike regije prostora bez potrebe za izračunom udaljenosti do svakog primjera.

---

### 🧮 Napomene za problemske zadatke

#### Zadatak tip 1: k-NN klasifikacija s Levenshteinovom udaljenosti (stringovi)
- Levenshteinova udaljenost L(a,b) = min broj umetanja, brisanja i zamjena jednog znaka da se a pretvori u b
- Jezgrena funkcija: κ(x,x') = 1/(1 + L(x,x')) — veća sličnost za manju udaljenost
- k-NN: naći k najbližih susjeda (najmanja L), većinsko glasanje po oznakama
- Težinski k-NN: zbrojiti κ za svaku klasu, klasa s većim zbrojem pobjeđuje
- Pravila za izjednačenje: prednost klasa s manjom numeričkom oznakom; kod jednake sličnosti prednost primjer naveden ranije u D

#### Zadatak tip 2: Višeklasni k-NN s jezgrenom funkcijom nad znakovnim nizovima
- κ(x₁,x₂) = |x₁ ∩ x₂| / |x₁ ∪ x₂| — Jaccardova sličnost nad skupovima slova
- 3-NN: naći 3 najbliža susjeda po κ, većinsko glasanje
- Težinski k-NN (k=N): zbrojiti κ(x⁽ⁱ⁾, x) za svaku klasu, klasa s max zbrojem pobjeđuje
- Za svaki primjer izračunati skupove slova, pa uniju i presjek
- Pravila za izjednačenje: prednost klasa s manjom oznakom; kod jednake sličnosti prednost prvi u D

---
