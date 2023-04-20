Nume: Volintiru Mihai Catalin \
Grupă: 336CA

# Tema <NR> TODO
#### Este recomandat să folosiți diacritice. Se poate opta și pentru realizarea în limba engleză. 

Organizare
-
1. Explicație pentru soluția aleasă:
> Pentru soluție am ales să fac un buffer separat pentru fiecare
> producător unde să publice produsele lui. Limita bufferului este cea impusă de marketplace,
> iar fiecare consumator o să caute secvențial, pe la toți producătorii, produsul de care are nevoie. \
> Având în vedere că bufferul de marketplace este o resursă partajată, am ales sa îl sincroniezez cu Lock-uri
> pentru toate operațiile de tip publish sau add_to_cart, pentru a mă asigura că totul este ok.

***Obligatoriu:*** 


* De făcut referință la abordarea generală menționată în paragraful de mai sus. Aici se pot băga bucăți de cod/funcții - etc.
> Mă asigur că fiecare producător are bufferul separat astfel:
> > self.marketplace.update({producer_id: []})

> Mă asigur că operațiile care folosesc bufferul marketplace sunt sincronizate astfel:
> > self.lock_producers.acquire()
* Consideri că tema este utilă?
> Da, consider că tema este utilă pentru că poate să mă ajute pe viitor cand vine vorba de programare
paralelă.
* Consideri implementarea naivă, eficientă, se putea mai bine?
> Sunt de părere că implementarea este într-adevăr naivă, deoarece mă folosesc numai de Lock-uri pentru
> a sincroniza anumite resurse partajate. Sunt convins că se putea face si cu un executor service, dar
> nu am simțit nevoia să mă complic.

***Opțional:***


* De menționat cazuri speciale, nespecificate în enunț și cum au fost tratate.
> Sunt 2 cazuri: bufferul de marketplace care nu e specificat dacă să fie la comun sau nu (am ales să 
> îl fac separat pentru fiecare producător) și cazul în care produsul pe care consumatorul îl dă jos
> din cart, deși coada producătorilor este plină (am ales să îl pun chiar dacă nu mai e loc în marketplace).

Implementare
-

* De specificat dacă întregul enunț al temei e implementat
> Da, enunțul a fost implementat.
* Dacă există funcționalități extra, pe lângă cele din enunț - descriere succintă + motivarea lor
> Nu, nu există.
* De specificat funcționalitățile lipsă din enunț (dacă există) și menționat dacă testele reflectă sau nu acest lucru
> Nu, nu există.
* Dificultăți întâmpinate
> Nu am întâmpinat dificultăți.
* Lucruri interesante descoperite pe parcurs
> Am descoperit că dacă nu fac buffer separat pentru fiecare producător în parte și las un buffer la comun
> o să îmi intre într-un deadlock pentru că: să zicem că am produsele id1, id2, id3, si producătorii prod1 și prod2;
> dacă prod1 poate face doar produse de tipul id1 și id2, iar prod2 poate face doar produse id2 și id3,
> având în vedere că ei fac produsele secvențial, este foarte probabil ca marketplace-ul să fie plin numai cu
> produse de tipul id1 și id2, dar nu id3. \
> Acest lucru devine o problemă când consumatorul are nevoie de un produs
> de tipul id3 (asta în cazul în care e singurul consumator sau dacă toți consumatorii vor produsul id3), pentru
> că producătorii nu o să mai publice nimic (pentru că e coada plină), iar consumatorii nu o să consume nimic
> (pentru că nu găsesc produsul pe care îl doresc).


Resurse utilizate
-

* Resurse utilizate - toate resursele publice de pe internet/cărți/code snippets, chiar dacă sunt laboratoare de ASC
> https://ocw.cs.pub.ro/courses/asc/laboratoare/02 \
> https://ocw.cs.pub.ro/courses/asc/laboratoare/03 \
> https://stackoverflow.com/questions/3029816/how-do-i-get-a-thread-safe-print-in-python-2-6 \
> https://docs.python.org/3/library/unittest.html \
> https://docs.python.org/3/library/logging.html \
> https://docs.python.org/3/library/logging.handlers.html#logging.handlers.RotatingFileHandler

Git
-
1. Link către repo-ul de git
> Repo-ul este privat la momentul de față, vă rog să îmi dați un mesaj ca să îl pun pe public (probabil
> îl voi pune și eu după deadline-ul hard) \
> https://github.com/Volintiru-Mihai-Catalin/Marketplace

Ce să **NU**
-
* Detalii de implementare despre fiecare funcție/fișier în parte
* Fraze lungi care să ocolească subiectul în cauză
* Răspunsuri și idei neargumentate
* Comentarii (din cod) și *TODO*-uri