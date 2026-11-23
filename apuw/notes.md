# RESTful API Dizajn

## Resursi i URI dizajn
- **URI (Uniform Resource Identifier)** je case-sensitive osim sheme i hosta. Treba koristiti **mala slova** u URI putanjama radi dosljednosti.
- **Razmaci** nisu dozvoljeni u URI-jima, umjesto njih koristi se **crtica (-)** za bolju čitljivost.
- **Podvlake (_)** ne bi se trebale koristiti jer mogu biti skrivene podcrtavanjem u klijentskim aplikacijama.
- **Ekstenzije datoteka** ne bi trebale biti uključene u URI-je. Format poruke treba biti određen putem **Content-Type** headera.
- **Top-level domena i prvi subdomain** trebaju identificirati vlasnika servisa. Za API se koristi **api** kao subdomain.

## Modeliranje resursa
Postoje **četiri arhetipa resursa**:
- **Dokument** - pojedinačni resurs koji sadrži reprezentaciju i poveznice na druge resurse.
- **Kolekcija** - direktorij resursa kojim upravlja server.
- **Spremište** - repozitorij resursa kojim upravlja klijent.
- **Kontroler** - izvršne funkcije s parametrima i povratnim vrijednostima.

## URI putanja
- **Kosa crta (/)** označava hijerarhijski odnos.
- **Zarez (,)** koristi se kada je redoslijed važan.
- **Točka-zarez (;)** koristi se kada redoslijed nije bitan.
- **Završna kosa crta (/)** ne bi se trebala koristiti.
- **Jednina imenice** za dokumente, **množina imenice** za kolekcije i spremišta.
- **Glagoli** za kontrolere.
- **Query parametri** za filtriranje i paginaciju.

## Interakcijski dizajn
### HTTP metode
- **GET** - dohvaćanje resursa.
- **HEAD** - dohvaćanje metapodataka.
- **PUT** - dodavanje/ažuriranje resursa.
- **POST** - kreiranje resursa ili izvršavanje kontrolera.
- **DELETE** - uklanjanje resursa.
- **OPTIONS** - dohvaćanje dostupnih interakcija.

### Response status kodovi
- **200 OK** - općeniti uspjeh.
- **201 Created** - uspješno kreiranje resursa.
- **202 Accepted** - početak asinkrone akcije.
- **204 No Content** - nema tijela odgovora.
- **301 Moved Permanently** - resurs trajno premješten.
- **307 Temporary Redirect** - resurs privremeno premješten.
- **400 Bad Request** - greška klijenta.
- **401 Unauthorized** - problem s autorizacijom.
- **403 Forbidden** - nedovoljno privilegija.
- **404 Not Found** - resurs nije pronađen.
- **405 Method Not Allowed** - metoda nije podržana.
- **500 Internal Server Error** - greška servera.

200 OK - uspjeh opcenito
201 Created - uspjesno kreiranje resursa
202 accepted - pocetak asinkrone akcije (websocket)?
204 no content - no body
301 moved permanently
304 not modified??
307 temporary redirect
400 bad request -> glup si
401 unauthorized
403 forbidden -> slabe privilegije
404 not found
405 method not allowed (get a ne postoji)
500 internal server errror

## Metadata dizajn
- **Content-Type** - specificira tip podataka.
- **Content-Length** - veličina tijela u bajtovima.
- **Host header** - obavezan u HTTP 1.1 za virtual hosting.

## Web hosting
- **On-premise hosting** - vlastita infrastruktura.
- **Web hosting usluga** - infrastruktura davatelja usluge.
- **Dedicated hosting** - cijeli server za jedan servis.
- **Virtual hosting** - više domena na jednom serveru.
- **Implementacija virtualnog hostinga**:
  - URL putanja (loše rješenje)
  - Broj porta (komplicirano)
  - IP adresa (ograničeno)
  - Host header (preporučeno)

## Asinkroni web protokoli
- **HTTP** je sinkroni protokol (request-response model).
- **XHR (XMLHttpRequest)** omogućuje asinkroni prijenos podataka.
- **Real-time notifikacije**:
  - **Client-To-Server** - neefikasno.
  - **Server-To-Client** - polling i long polling.
- **Server-Sent Events (SSE)** - efikasan streaming tekstualnih podataka.
- **WebSocket** - bidirekcionalni prijenos podataka.

### XHR vs. SSE vs. WebSocket
| Protokol | Prednosti | Nedostaci |
|----------|------------|------------|
| **XHR** | Jednostavan | Nije za streaming |
| **SSE** | Efikasan za streaming | Unidirekcionalan, samo tekst |
| **WebSocket** | Najefikasniji | Zahtijeva dugotrajne veze |

## Remote Procedure Calls (RPC)
- Omogućuje pozivanje udaljenih procedura.
- Može biti **sinkron i asinkron**.
- Generacije RPC:
  1. Sun RPC, XDR (1980-e)
  2. CORBA, DCOM, Java RMI (1990-e)
  3. XML RPC, SOAP (2000-e)
  4. gRPC, Protocol Buffers (2010-)

### gRPC
- Open source RPC od Google-a.
- Koristi **HTTP/2** i **Protocol Buffers**.
- Podržava **streamanje, autentikaciju i cross-platform**.

## Mikroservisi
- **Mikroservisi** su skup **malih, neovisnih servisa**.
- **Monolitna aplikacija** - teško skalabilna.
- **SOA vs. Mikroservisi**:
  - **SOA** - XML baziran, centraliziran.
  - **Mikroservisi** - REST, event-based.
- **Modeliranje mikroservisa**:
  - **Labava povezanost**, **visoka kohezija**.
  - **Izbjegavati dijeljenje baze podataka**.
  - **REST, RPC, Event-based komunikacija**.

### Implementacija mikroservisa
- Kontejneri (**Docker**), orkestracija (**Kubernetes**).
- Više servisa po hostu vs. jedan servis po hostu.
- **Virtualizacija**: KVM, VMWare, Xen, VirtualBox.

### Testiranje i monitoring
- **Unit testovi** - brzi i izolirani.
- **Servisni testovi** - bypass UI-a.
- **End-to-end testovi** - cijeli sustav.
- **Monitoring**: Logstash, Nagios, Graphite, Kibana/Grafana.

### Zaključak
**Prednosti:** Skalabilnost, modularnost, izolacija grešaka.
**Nedostaci:** Složenost, mrežni pozivi, testiranje, logiranje.

