Paghi per dati che sono già gratis. Falsi.

Negli ultimi mesi ho costruito un repository che si chiama api-archaeology. Non è un tool di scraping. Non è un tutorial per aggirare protezioni. È un'esplorazione di un fatto economico che pochi nel nostro settore sembrano disposti a guardare in faccia.

Per molte categorie di dati — prezzi carburanti, osservazioni meteo storiche, anagrafiche di impianti — esiste un intero mercato commerciale. E quel mercato esiste in larga parte per asimmetria informativa. La fonte pubblica esiste già, gratis, se sai dove guardare. E dove guardare è un'abilità che può essere insegnata.

---

Il problema non è tecnico. È cognitivo.

Ogni giorno, somewhere in un ufficio, un data engineer sta per acquistare un accesso a un data broker per ottenere prezzi storici dei carburanti in Italia. Non perché il dato non esista altrove. Perché non sa che il MIMIT pubblica quegli stessi dati in CSV tutti i giorni, su un URL diretto, con licenza IODL 2.0. Il sito principale mostra una mappa. La mappa oscura il file.

Ogni settimana, qualcuno in una redazione pagherebbe per accedere a un archivio meteo storico. ARPAE Emilia-Romagna pubblica 20 anni di osservazioni meteorologiche, 15 minuti di granularità, dal 2006 a oggi, come archivi mensili compressi. Il sito ufficiale mostra una finestra temporale stretta. Il backend accetta qualunque range.

Il pattern è sempre lo stesso. I dati sono pubblici. L'interfaccia li nasconde. Il costo di quella opacità è il vostro budget per i dati.

---

Ho sviluppato un metodo in quattro fasi per riconoscere questi casi. Lo chiamo Archeologia delle API, ma non nel senso tecnico del termine. Non si tratta di trovare API nascoste per violarle. Si tratta di osservare come un sito web si serve da se stesso — perché il frontend gira nel vostro browser, quindi ciò che fa è osservabile — e di distinguere tra il rumore e i dati che contano.

**Fase 1: Osservazione.** Aprite DevTools, scheda Network, filtrare per XHR o Fetch. Interagite con l'interfaccia normalmente. Cambiate date, filtri, pagine. L'obiettivo non è la comprensione immediata. L'obiettivo è un inventario delle richieste che appaiono quando l'interfaccia renderizza nuovi dati.

**Fase 2: Separazione.** Separate le richieste che portano dati dal rumore. Le richieste data-bearing di solito hanno risposte strutturate come JSON, parametri semantici come date o ID, payload che corrispondono chiaramente a ciò che l'interfaccia sta mostrando. Ignorate asset, analytics, font, tracciamento.

**Fase 3: Caratterizzazione.** Per ogni endpoint candidato, rispondete a un insieme fisso di domande: richiede autenticazione? Posso chiamarlo da un contesto fresco e ottenere dati? Quali parametri sono semanticamente necessari? Qual è il comportamento di rate limit visibile empiricamente? robots.txt o i ToS del sito creano una condizione di stop?

**Fase 4: Riutilizzo minimo.** Lo script deve essere piccolo e leggibile. Deve eseguire le chiamate HTTP minime, parsare il payload strutturato, persistere in CSV o Parquet. Se lo script diventa complesso prima che l'endpoint sia compreso, il problema è probabilmente una caratterizzazione incompleta.

Il risultato di ogni ciclo è una specifica scritta breve che un'altra persona può riprodurre. Non è un framework. È un modo di guardare.

---

Due esempi concreti, entrambi pubblicati nel repository.

**MIMIT — Prezzi carburanti.** Il Ministero delle Imprese e del Made in Italy pubblica ogni giorno un CSV con i prezzi praticati da tutti gli impianti italiani e un secondo CSV con l'anagrafica degli impianti attivi. Entrambi raggiungibili via URL diretto. La licenza è IODL 2.0, che significa libero riuso con attribuzione. Il sito principale mostra una mappa interattiva con un'interfaccia di ricerca. Il CSV esiste da anni, ma la mappa lo oscura completamente.

Il CSV usa un delimitatore pipe e una riga di metadati da skippare. C'è un passaggio di parsing minimo per normalizzare i separatori decimali. Niente di complesso. Lo script che ho scritto ha circa 60 righe. Controlla robots.txt, scarica il CSV, scrive 20 record campione. Il resto è accesso diretto.

**ARPAE — Meteo storico.** ARPAE Emilia-Romagna pubblica 20 anni di osservazioni meteorologiche come archivi mensili .json.gz, uno per mese, dal 2006 a oggi. Ogni file è NDJSON — un oggetto JSON per riga, ciascuno rappresentante una stazione a un singolo timestep. I dati includono temperatura, umidità relativa, precipitazioni, radiazione solare. Le coordinate sono in Gauss-Boaga Roma40, quindi serve una conversione banale per averle in gradi decimali WGS84.

Il sito ufficiale offre una finestra temporale stretta per le query. Il backend accetta qualunque range. Il pattern è esattamente quello che METHOD.md descrive come Pattern B: serie temporali dietro controlli UI restrittivi. Il frontend dice "no, max 30 giorni". Il backend dice "no, io accetto qualunque cosa".

---

Devo essere esplicito su una cosa, perché capita che qualcuno salti alla conclusione sbagliata.

Questo non è uno strumento di scraping. Non è un tutorial per aggirare protezioni. Non è un invito all'abuso di endpoint altrui. Se un sito richiede autenticazione reale, o ha protezione anti-bot seria, o il payload è intenzionalmente offuscato, o i ToS vietano chiaramente l'accesso automatizzato — il percorso difendibile è fermarsi. Punto.

Quello che questo progetto documenta è l'uso legittimo di dati pubblici che esistono già. Dati aperti da fonti istituzionali, con licenze open, pubblicati sotto URL diretto che chiunque può raggiungere con un browser. Il lavoro interessante non è lo scraping. Il lavoro interessante è riconoscere che quel mercato da mille euro al mese per "dati carburanti storici" è un mercato per accesso più facile, non per dati intrinsecamente scarsi.

I vincoli operativi che seguo: rate limit conservativi, User-Agent identificabile, nessun bypass di autenticazione, nessuna redistribuzione di raw dataset su larga scala. Gli script di esempio producono al massimo 20 record. Il resto è left as an exercise.

---

Se questo ti suona interessante, il repository è su GitHub: github.com/cioffiAI/api-archaeology. Il metodo è in METHOD.md, i casi completi sono nei rispettivi README nelle sottocartelle cases/. Ogni caso include i passaggi di riproduzione, lo schema dei dati, e le note sulle decisioni che ho preso.

Se hai familiarità con un dominio dove sai che esistono dati aperti pubblicati ma oscurati da un'interfaccia — o se hai provato ad applicare il metodo e hai trovato qualcosa di interessante — segnalalo. Il repository è pensato per crescere come catalogo di casi, non come tool monolitico.

Il risultato tecnico conta, ma il risultato più interessante è solitamente economico: una quota significativa del mercato dei dati è un mercato per accesso più facile. L'abilità dimostrata qui è riconoscere quando quel divario è piccolo.
