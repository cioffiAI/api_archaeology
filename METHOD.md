# Archeologia delle API: un metodo

La maggior parte dei siti web moderni ricchi di dati non sono pagine HTML monolitiche. Sono frontend che renderizzano l'interfaccia chiamando il backend del sito stesso via HTTP e ricevendo dati strutturati in risposta. Quel comportamento è pubblico per necessità: il frontend gira nel browser, quindi ciò che fa è osservabile.

Questo documento descrive un metodo sistematico per identificare queste chiamate backend, caratterizzarle abbastanza da poter essere riutilizzate responsabilmente, e decidere quando lo sforzo è giustificato.

## Terminologia
Due cose vengono chiamate "API" e la distinzione conta:
- Un'API documentata è un prodotto. Ha documentazione, un contratto, chiavi API, promesse di stabilità e di solito un piano a pagamento.
- Un'API interna non documentata è l'impianto idraulico che un sito pubblico usa per servire se stesso. Strutturalmente sono ancora richieste HTTP più risposte strutturate, ma senza un contratto pubblicato o supporto.

Questo progetto riguarda la seconda categoria. Non riguarda il bypass dell'autenticazione, il superamento di sistemi anti-bot, o l'accesso a dati intenzionalmente privati.

## Le quattro fasi
### Fase 1: Osservazione
Apri il sito target con DevTools nella scheda Network e filtra per `XHR` o `Fetch`. Interagisci con l'interfaccia normalmente: cambia date, filtri, pagine o visualizzazioni. L'obiettivo non è la comprensione immediata. L'obiettivo è un inventario delle richieste che appaiono quando l'interfaccia renderizza nuovi dati.

### Fase 2: Separazione
Separa le richieste che portano dati dal rumore.

Le richieste data-bearing di solito hanno:
- risposte strutturate come JSON o XML
- parametri semantici come date, ID, range o nomi
- payload che corrispondono chiaramente a ciò che l'interfaccia sta mostrando

Ignora asset, analytics, font, chiamate di tracciamento e rumore simile.

### Fase 3: Caratterizzazione
Per ogni endpoint候选, rispondi a un insieme fisso di domande:
- Richiede autenticazione?
- Può essere chiamato da un contesto fresco e ancora restituire dati?
- Quali parametri sono semanticamente necessari?
- È coinvolta la paginazione?
- Quale comportamento di rate limit è visibile empiricamente?
- `robots.txt` o i ToS del sito creano una condizione di stop operativa?

L'output di questa fase è una specifica scritta breve che un'altra persona può riprodurre.

### Fase 4: Riutilizzo minimo
Una volta caratterizzato l'endpoint, lo script risultante deve essere piccolo e leggibile. Deve eseguire le chiamate HTTP minime, parsare il payload strutturato, e persistere il risultato in un formato portatile come CSV, Parquet o SQLite.

Se lo script diventa complesso prima che l'endpoint sia compreso, il problema reale è probabilmente una caratterizzazione incompleta.

## Tre pattern ricorrenti
### Pattern A: Endpoint tabulari con filtro semantico
Tipici di aggregatori sportivi e interfacce simili. L'interfaccia mostra tabelle filtrabili e il backend espone endpoint i cui parametri mappano strettamente i controlli visibili.

### Pattern B: Serie temporali dietro controlli UI restrittivi
Tipici di portali meteo storici. Il frontend offre finestre temporali strette mentre il backend spesso accetta range più ampi di ciò che l'interfaccia suggerisce.

### Pattern C: Dati aperti già pubblicati, ma oscurati dall'interfaccia
Tipici di dataset governativi o di industrie regolamentate. I dati sono già pubblici, ma il sito mette in primo piano una mappa o un'interfaccia di ricerca piuttosto che il feed flat.

## Quando il metodo non si applica
Fermati quando una di queste condizioni è vera:
- i dati richiedono autenticazione reale
- il sito usa protezione anti-bot seria
- il payload è intenzionalmente offuscato o firmato
- i ToS del sito vietano chiaramente l'accesso automatizzato

In questi casi il percorso difendibile è fermarsi o usare l'API documentata ufficiale se esiste.

## Per cosa è utile il metodo
Usi appropriati:
- ispezione educativa di dati pubblici
- ricerca occasionale
- giornalismo su dataset pubblici
- analisi accademica su piccola scala
- progetti personali che non girano come servizio

Usi inappropriati:
- servizi commerciali costruiti su endpoint non documentati
- pipeline di download di massa
- redistribuzione di raw data su larga scala
- qualsiasi cosa che sia difficile da difendere verso l'operatore del sito in linguaggio normale

## Un'osservazione finale
Il risultato tecnico conta, ma il risultato più interessante è solitamente economico: una quota significativa del mercato dei dati è un mercato per accesso più facile, non per dati intrinsecamente scarsi. L'abilità dimostrata qui è riconoscere quando quel divario è piccolo.