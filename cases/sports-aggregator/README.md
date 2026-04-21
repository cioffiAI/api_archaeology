# Case Study Aggregatore Sportivo

## Stato
Scaffold in corso.

Questo case study documenta il pattern dell'aggregatore sportivo senza esporre il target originale, URL live o stringhe endpoint esatte. L'implementazione in questo repository rimane uno scaffold policy-aware fino a quando le osservazioni non vengono riscritte in un writeup pubblico riproducibile.

## Framing pubblico
Questo case study resta generico come aggregatore di dati sportivi. Il repo pubblico non nomina il sito sorgente, non espone URL live, e non pubblica stringhe endpoint esatte.

## Pattern osservato
Dati sportivi tabulari con filtro semantico.

Caratteristiche osservate:
- dati tipo tabella consegnati a una pagina di tipo live-score
- visualizzazioni basate su lega e tempo
- feed di dati strutturati sufficienti a popolare l'interfaccia senza HTML scraping
- navigazione superficiale pubblica visibile senza login

## Review della sorgente verificata
Il target di lavoro attuale è stato ri-verificato dopo la correzione di un errore precedente di nome dominio nelle note del progetto.

Fatti verificati il 2026-04-21:
- il sito è raggiungibile pubblicamente
- la FAQ pubblica dice che i dati dei punteggi possono essere visualizzati senza registrazione
- il sito espone una pagina pubblica "Free Feed"
- `robots.txt` disallow esplicitamente diversi path dinamici, inclusi `/ajax/`, `/home/ajax/`, `/gf/`, `/soccer/flashLive/`, `/textlive/`, e `/scripts/`

Implicazione:
- questo case study può procedere solo se il percorso riproducibile usa superfici che non sono bloccate da `robots.txt`
- se il vecchio workflow dipendeva da uno dei path disallow, quel workflow non deve essere pubblicato o reimplementato qui

## Limitazioni attuali
Il repository evita ancora di pubblicare dettagli specifici del target. Ciò che manca è il layer di caratterizzazione esposto al pubblico:
- una descrizione riproducibile del pattern di richiesta osservato
- una spiegazione sanificata dei parametri rilevanti
- un piccolo flusso dimostrativo che resti dentro la policy del repository

## Cosa succede dopo
1. Ricostruire la caratterizzazione della richiesta sanificata dalle osservazioni originali.
2. Confermare che il percorso minimo riproducibile resti fuori dai path `robots.txt` attualmente disallow.
3. Mantenere il framing pubblico generico ed evitare di esporre dettagli endpoint specifici del target.
4. Sostituire questo scaffold con un case study riproducibile e policy-compliant.

## Ruolo dei file
- `fetch.py`: entrypoint policy-aware del case
- `parse.py`: scaffold di normalizzazione per l'eventuale payload strutturato
- `sample.csv`: solo campione dimostrativo, non dati bulk

## Nota di pubblicazione
Uno scaffold generico è meglio di affermazioni specifiche del target non verificabili.