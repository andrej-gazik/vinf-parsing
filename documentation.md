# Parsovanie title, alt, typ pre EN a index

# Krátky opis problému a motivácia

Téma projektu sa zaoberá tak ako je to uvedené v nadpise parsovaním title, alt a typu pre anglický jazyk z dát databázových dumpov Freebase. Nutnosť parsovania dát vzniká z faktu, že v databázových dumpoch Freebase sa nenachádzajú len informácie, ktoré sa snažíme získať ale aj mnoho iných informácií. Pre získanie správnych dát musíme zistiť v čom sa lýšia a aké atribúty určujú správnosť dát pre náš prípad. Následne sa pokúsime a parsovanie dát ktoré vyhovujú požiadavkám zadania a pokúsime sa o indexáciu získaných dát. Pre výber správnych dát je možné použiť regulárne výrazy, pre ktoré zostrojíme vyhľadávacie vzory vzhľadom k charakteristike vstupných dát tak aby nám vrátili zhody. Indexácia získaných dát je potrebná z dôvodu zjednodušenia vyhľadávania. Bez indexácie by bolo nutné prechádzať lineárne celú množinu získaných dát. Cieľom indexácie je optimalizácia rýchlosti a výkonnosti vyhľadávania pre zadaný dopyt. 

# Prehľad súčasných riešení

Súčasné riešenia zaoberajúce sa Freebase dátami sa venovali prácou s dátami nasledovnne. 

## Using linked open data for novel artist recommendations

Toto riešenie sa opisuje systém, ktorý za pomoci dát z Freebase opisuje hudobných tvorcov. Tvorci sú reprezentovaný profilmi metadát, ktoré charakterizujú rôzne aspekty ich tvorby ako žánre, hudobné nástroje a taktiež aj kolaborácia s inými tvorcami. Systém využíva indexáciu v Lucene pre odporúčanie tvorcov. 

Zdroj: [https://www.semanticscholar.org/paper/USING-LINKED-OPEN-DATA-FOR-NOVEL-ARTIST-Baumann-Schirru/9b73079aea69c4b75d579bd863af1b84083aba0f](https://www.semanticscholar.org/paper/USING-LINKED-OPEN-DATA-FOR-NOVEL-ARTIST-Baumann-Schirru/9b73079aea69c4b75d579bd863af1b84083aba0f)

## **FreeQ: an interactive query interface for freebase**

V tomto riešení sa autor venoval zjednodušeniu vyhľadávania informácií nad dátami vo Freebase, kedže vyhľadávanie podľa kľúčových slov je nejednoznačné kvôli veľkosti dát a ich komplexite. Riešením je klient-server Java aplikácia ktorej môže používateľ zadať dopyt a na základe tohoto dopytu rozhranie vráti výsledky. Indexácia je implementovaná cez Lucene.

Zdroj: h[ttps://www.researchgate.net/publication/254008881_FreeQ_An_interactive_query_interface_for_Freebase](https://www.researchgate.net/publication/254008881_FreeQ_An_interactive_query_interface_for_Freebase)

# Popis riešenia

Problém parsovania title, alt, typ pre EN a index z freebase sme riešili postupne po krokoch. 

V prvom kroku sme sa venovali zoznamovaniu s dátami a vytváraniu regulárnych výrazov, ktoré nám získajú potrebnú podmnožinu dát z celej množiny. Dáta RDF sú serializované v N-Trojiciach a enkódované v UTF-8. 

Formát dát je napríklad: `<subject>  <predicate>  <object> .`

Kde subject je id objektu, predicate charakterizuje následný object obsahuje referenciu na iný objekt alebo hodnoty ako sú reťazce numerické hodnoty alebo boolovské hodnoty. 

Pre získanie title alt a typ sme vymedzili hodnoty predicate na `type.object.type` , `type.object.name`, a `common.topic.alias`. Filtrovanie záznamov je vykonávané pomocou regulárnych výrazov ktoré získajú z riadku id záznamu type name alebo alias a obsah objektu. 

Následným prechádzaním gzip súboru datadumpu sme pomocou regulárných výrazov získavali dáta.

V dalšom kroku sme sa venovali paralelizácii parsovania dát a indexácii. Pre paralelizáciu riešenia sme použili PySpark, ktorý umožní načítanie dát do dátového rámcu z textu z dekomprimovaného súboru konverziu na RDD a vykonávaniu parsovacích a filtrovacích operácií nad dátami no paralelizovane. 

Pre parsovanie sme vytvorili lambda funkciu ktorú sme pomocou metódy `.map` aplikovali na dáta. Hodnoty ktoré boli namapované na None sme odfiltrovali a to dôvodu, že nevyhovujú požiadavkám zadania a tak sme ich nepotrebovali. Ako poslednú operáciu sme odstránili duplikátne hodnoty za pomoci metódy `.distinct`. Výsledný RDD sme uložili ako parquet súbory do výstupnej zložky a pokračovali sme indexáciou. Indexácia je vykonávaná za pomoci python knižnice whoosh. 

Nad vytvoreným indexom sme vytvorili jednoduché vyhľadávacie rozhranie, ktoré vyhľadáva nad vytvoreným indexom zadané frázy od používateľa a vráti zhodu. Pre jednoslovné vyhľadávanie stačí zadať slovo a pre vyhľadávanie výrazu je nutné dať výraz do úvodzoviek. Vrátené sú riadky vyhovujúce zadaným výrazom a všetky ostatné informácie spojené s vyhľadaným ID. 

## Použitý softvér

************Python -************ skriptovacia časť bola implementovaná v jazyku python

**************PySpark -************** Načítanie vstupného súboru parsovanie a výstup v .parquet súboroch

************Whoosh -************ Whoosh je knižnica tried a funkcií na indexovanie textu a následné vyhľadávanie v indexe.

# Dáta

Dáta sú získané z voľne dostupného dumpu z [https://developers.google.com/freebase](https://developers.google.com/freebase). Komprimovaný súbor má veľkosť **22GB** a po dekomprimácii je jeho veľkosť **250 GB**, čo je pre naše účely priveľké. Počas práce na projekte som pracoval s čiastkovým súborom, ktorý je podmnožinou celkového súboru. Tento súbor som získal dekomprimáciou pomocou nasledovného príkazu.

```bash
gzip -cd freebase_triples.gz | dd ibs=1024 skip=0 count=1000000 > 1GB_file.txt
```

Príkaz dekomprimuje iba časť súboru tak aby výsledný súbor mal zadanú veľkosť. 

# Vyhodnotenie

V projekte sa mi podarilo vyparsovat potrebné dáta spraviť nad nimi indexáciu a umožniť tak vyhľadávanie. Overenie riešenia bolo vykonané len manuálne. Pre výsledky vyhľadávania sa zisťovalo skóre ktoré je vypísané pri každom výsledku, túto metriku je možné použiť na overenie. 

Ako príklad uvediem výsledok pre vyhľadanie slova metallica:

```bash
Input phrase to search:
input query: metallica
Results for: metallica
1 {"id": "01gbwls", "predicate": "alias", "object": "Metal Militia - A Tribute to Metallica"}   Score: 11.99
                type : base.type_ontology.abstract
                type : music.album
                alias : Metal Militia - A Tribute to Metallica
                type : base.type_ontology.non_agent
                name : Metal Militia: A Tribute to Metallica
                type : base.type_ontology.inanimate
                type : common.topic
                alias : Metal Militia – A Tribute to Metallica
2 {"id": "01gbwls", "predicate": "name", "object": "Metal Militia: A Tribute to Metallica"}     Score: 11.99
                type : base.type_ontology.abstract
                type : music.album
                alias : Metal Militia - A Tribute to Metallica
                type : base.type_ontology.non_agent
                name : Metal Militia: A Tribute to Metallica
                type : base.type_ontology.inanimate
                type : common.topic
                alias : Metal Militia – A Tribute to Metallica
3 {"id": "012479sx", "predicate": "name", "object": "One (8-Bit Metallica Speed remix)"}        Score: 11.99
                type : base.type_ontology.non_agent
                type : music.single
                type : music.recording
                name : One (8-Bit Metallica Speed remix)
                type : base.type_ontology.abstract
                type : common.topic
4 {"id": "01gbwls", "predicate": "alias", "object": "Metal Militia – A Tribute to Metallica"}   Score: 11.99
                type : base.type_ontology.abstract
                type : music.album
                alias : Metal Militia - A Tribute to Metallica
                type : base.type_ontology.non_agent
                name : Metal Militia: A Tribute to Metallica
                type : base.type_ontology.inanimate
                type : common.topic
                alias : Metal Militia – A Tribute to Metallica
---------------------------------
```

# Inštalácia a spustenie

Pre inštaláciu je nutné prvorade splniť nasledovné podmienky: 

- JAVA 8
- Pyhton 3
- PySpark (V našom prípade spark-3.3.1-bin-hadoop2)
- pip install -r requirements.txt

Pred spustením parsovania je nutné sa uistiť, že v súbore [conf.py](http://conf.py) je správne nastavený názov súboru datasetu, výstupu a ostatných parametrov. Následne je možné pokračovať nasledovným postupom. 

Pre spustenie parsovania

```bash
spark-submit parsing.py
```

Pre vytvorenie indexácie a vyhľadávanie

```bash
pyhton index.py
python search.py
```

Pre testovanie jednotlivých častí je možné spúštať testovací skript nasledovne. 

```bash
#usage: test.py [-h] [-t TEST] [-a ALL]
#
#options:
#  -h, --help            show this help message and exit
#  -t TEST, --test TEST  Test to run (regex | parsing | index | search | all)
#  -a ALL, --all ALL     Run all tests

# Testing of regex
python test.py -t regex

# Testing of parsing output
python test.py -t parsing

# Testing of index creation
python test.py -t index

# Testing of searching
python test.py -t search

# Run all tests at once 
python test.py --all 
```
