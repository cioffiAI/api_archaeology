# PROJECT_BRIEF.md

## Scopo
Questo documento sintetizza, in forma operativa, il contenuto dei PDF presenti nel workspace.

Fonte esclusiva:
- `piano_api_archaeology.pdf`
- `method_ethics_api_archaeology.pdf`
- `documenti_api_archaeology.pdf`

## Stato del documento
- Stato: compilato dai PDF
- Fonte primaria: PDF nel workspace
- Livello di confidenza: medio-alto
- Limite: il brief deriva dai documenti strategici e testuali, non da codice gia' esistente

## 1. Obiettivo del progetto
- Obiettivo principale: costruire un progetto pubblico chiamato `api-archaeology` che documenti una metodologia sistematica per identificare e riusare endpoint HTTP non documentati dietro siti web data-heavy.
- Problema che risolve: mostrare che, per molte categorie di dati, il mercato "a pagamento" esiste per asimmetria informativa, mentre la sorgente pubblica esiste gia' ed e' raggiungibile se si sa dove guardare.
- Utente o destinatario: reviewer tecnici, senior engineer, pubblico tecnico su GitHub e LinkedIn, oltre a studenti, ricercatori, giornalisti e persone che fanno analisi one-off su dati pubblici.
- Risultato finale atteso: repository GitHub pubblico con metodologia, policy etica e tre case study; articolo LinkedIn; mini-paper di accompagnamento.

## 2. Output finali attesi
- Output 1: `README.md` in inglese, leggibile in circa 60 secondi, con tesi, overview dei case study, quickstart, scope ed ethics.
- Output 2: `METHOD.md` con metodologia astratta in quattro fasi, tassonomia di tre pattern tecnici e limiti dell'approccio.
- Output 3: `ETHICS.md` con policy d'uso, rate limiting, User-Agent, posizione su ToS, robots.txt e richieste di rimozione.
- Output 4: tre cartelle `cases/` per i case study.
- Output 5: articolo LinkedIn in italiano, narrativo, circa 1400 parole.
- Output 6: mini-paper "Il prezzo dell'asimmetria informativa".
- Formato degli output: Markdown per i documenti del repo, Python per gli script, CSV per i campioni dimostrativi, PDF per il mini-paper, articolo LinkedIn per la pubblicazione social.
- Criteri minimi di completezza: almeno Fase 1 completata e pubblicabile con `README.md`, `METHOD.md`, `ETHICS.md` e un case study completo.

## 3. Metodo di lavoro
- Sequenza operativa prevista:
  1. osservazione con DevTools
  2. separazione delle richieste data-bearing dal rumore
  3. caratterizzazione degli endpoint
  4. riuso minimo con script Python leggibili
- Fonti da analizzare: richieste HTTP osservate nel browser, risposte JSON/XML, robots.txt, Terms of Service, eventuali flat file o feed pubblici, prezzi pubblici dei servizi commerciali equivalenti.
- Modalita' di raccolta dati: uso del tab Network con filtro XHR/Fetch, interazione normale con la UI, analisi di URL, parametri, payload e pattern di paginazione; solo se necessario, uso di mitmproxy.
- Modalita' di verifica: controllo dell'assenza di autenticazione, test di riuso da contesto fresco, osservazione empirica del rate limit, documentazione riproducibile nel case study.
- Cosa non fare: bypass autenticazione, evadere anti-bot, lavorare su dati intenzionalmente privati, ignorare ToS proibitive, usare Playwright o Selenium all'inizio senza evidenza che siano necessari.

## 4. Vincoli etici e pratici
- Limiti etici: uso educativo, ricerca personale, studio accademico, giornalismo basato su dati pubblici, analisi one-off.
- Limiti legali o di utilizzo: se i ToS sono chiaramente proibitivi il case study non va incluso; se i ToS sono ambigui l'ambiguita' va dichiarata.
- Dati sensibili da evitare o trattare con cautela: dati che richiedono login, dati privati dell'utente autenticato, dati realmente proprietari.
- Azioni esplicitamente vietate: mass download per redistribuzione, costruzione di un servizio commerciale su endpoint non documentati, spoofing del browser User-Agent, bypass di autenticazione, aggiramento di protezioni anti-bot serie, reverse engineering di payload offuscati.
- Rischi principali: fragilita' degli endpoint non documentati, costo infrastrutturale scaricato sui siti target, esposizione legale o reputazionale, progetto percepito come tutorial aggressivo invece che come lavoro serio.

## 5. Input e fonti operative
- Documenti di input: i tre PDF del workspace e, nel progetto finale, README, METHOD, ETHICS e documentazione dei case study.
- Eventuali URL o sorgenti esterne: siti target dei case study, rispettivi robots.txt, rispettivi ToS, eventuali feed open data, pagine pubbliche di pricing dei servizi equivalenti.
- Formato dei dati in ingresso: richieste HTTP, JSON, XML, CSV, HTML e dati osservati via DevTools.
- Qualita' attesa dei dati: dati pubblicamente accessibili, semanticamente riconoscibili e sufficienti a dimostrare il metodo.
- Dipendenze esterne: browser con DevTools, Python 3.11+, `uv`, `httpx`, `selectolax` quando serve, `pydantic`, `pandas` o `polars`, opzionalmente `mitmproxy`.

## 6. Struttura iniziale del progetto
- Cartelle principali:
  - `cases/`
  - `cases/sports-aggregator/`
  - `cases/weather-historical/`
  - `cases/fuel-prices-mimit/`
  - `paper/`
  - `tool/` come componente opzionale in Fase 3
- File iniziali:
  - `README.md`
  - `METHOD.md`
  - `ETHICS.md`
  - `paper/asymmetry.pdf`
- Moduli o componenti previsti per ogni case study:
  - `README.md`
  - `fetch.py`
  - `parse.py`
  - `sample.csv`
- Linguaggi o strumenti previsti: Python, Markdown, DevTools del browser, GitHub, LinkedIn.
- Convenzioni di naming: cartelle dei case study in kebab-case; stessa struttura per tutti i casi per dare coerenza e auditabilita'.

## 7. Case study previsti
- Case study A: aggregatore sportivo.
  - Pattern: endpoint tabulari filtrati da parametri semantici come competizione, stagione e data.
  - Framing pubblico: "sports data aggregator".
  - Vincolo: non citare nome, URL completo o endpoint reali nel progetto pubblico; usare placeholder `example.com`.
- Case study B: dati meteo storici.
  - Pattern: serie temporali dietro paginazione o UI con range temporali artificialmente limitati.
  - Candidati: `ilMeteo.it`, `3BMeteo`, oppure preferibilmente un portale ARPA regionale come ARPA Lazio.
  - Scelta raccomandata dai PDF: ARPA, perche' ente pubblico e dato intrinsecamente pubblico.
- Case study C: prezzi carburanti MIMIT.
  - Pattern: open data gia' pubblicati come CSV/JSON o feed poco visibili, ma oscurati dall'interfaccia principale.
  - Sorgente: Osservatorio prezzi carburanti del MIMIT.

## 8. Fasi e milestone
- Fase 1: metodologia + primo case study.
  - Output: repo con `METHOD.md`, `ETHICS.md`, `README.md` e un solo case study completo.
  - Pubblicabile: si.
  - Tempo stimato: 5-7 giorni.
- Fase 2: aggiunta degli altri due case study.
  - Output: repo arricchito e tabella comparativa dei pattern tecnici nel README.
  - Pubblicabile: si, come aggiornamento.
  - Tempo aggiuntivo: 4-6 giorni.
- Fase 3: mini-paper, CLI helper opzionale e thread X lungo.
  - Pubblicabile: si.
  - Tempo aggiuntivo: 3-5 giorni.

Milestone piu' granulari citate nel piano:
- 1.1 Setup repo, `ETHICS.md`, `METHOD.md` draft v1: 2 giorni.
- 1.2 Case study A ripulito e ricondotto al framing generale: 3 giorni.
- 1.3 `README.md` v1, push pubblico, post LinkedIn di lancio: 2 giorni.

## 9. Regole operative da implementare nel codice
- Rate limiting: minimo 2 secondi tra richieste allo stesso host.
- Rate limiting per siti piccoli o istituzionali: default 5 secondi.
- Configurazione: il rate limit puo' essere configurabile ma gli script non devono accettare valori sotto 1 secondo.
- User-Agent: `ApiArchaeology/1.0 (educational; +github.com/<cioffiAI>/api-archaeology)` con email di contatto configurabile via variabile d'ambiente.
- Robots.txt: va letto a startup; i path esplicitamente disallow per crawler generali vanno saltati.
- Redistribuzione: il repository non deve contenere raw dataset completi, solo piccoli sample dimostrativi.
- Autenticazione: nessun case study deve usare endpoint che richiedono login.
- Rimozione: se un sito introduce autenticazione, il case study va aggiornato e il codice rimosso o marcato come non funzionante.

## 10. Strategia di pubblicazione
- Ordine consigliato:
  1. repo GitHub live e funzionante
  2. articolo LinkedIn che linka al repo
- Commit history raccomandata:
  1. commit iniziale con `README`, `METHOD`, `ETHICS` placeholder
  2. commit separati per ciascun documento
  3. un commit per ogni case study
- Motivo: una history leggibile mostra progressione reale; un singolo commit con tutto dentro segnala generazione automatica e va evitato.

## 11. Assunzioni esplicite
- Assunzione 1: i tre case study finali saranno effettivamente implementati in Python, come indicato nei documenti.
- Assunzione 2: il primo rilascio pubblico puo' avvenire con il solo primo case study completo.
- Assunzione 3: il repo pubblico deve mantenere un framing non-betting e non centrato sui nomi specifici dei siti.

## 12. Questioni aperte
- Questione aperta 1: quale portale meteo storico verra' scelto in modo definitivo tra i candidati indicati.
- Questione aperta 2: se il componente `tool/` opzionale di Fase 3 verra' realizzato davvero o lasciato fuori.
- Questione aperta 3: quali numeri di pricing reali e quali screenshot verranno inseriti dopo l'esecuzione concreta dei case study.

## 13. Criteri di accettazione
- Il progetto e' correttamente avviato se esistono `README.md`, `METHOD.md`, `ETHICS.md` e la struttura `cases/`.
- La prima milestone e' completata quando il repo contiene il primo case study completo con writeup, script di fetch, parsing e sample dimostrativo.
- Il risultato e' verificabile tramite:
  - riproduzione delle richieste osservate via DevTools
  - controllo del rispetto delle policy etiche nel codice
  - leggibilita' end-to-end degli script
  - compatibilita' con il framing pubblico definito dai documenti

## 14. Tracciabilita'
- Decisione: il progetto deve essere presentato come metodologia generale e non come progetto di scraping.
  - Basata su: `piano_api_archaeology.pdf`, sezione "La tesi del progetto"; `documenti_api_archaeology.pdf`, README.
  - Tipo: fatto
  - Da verificare: no
- Decisione: il primo rilascio pubblico puo' includere un solo case study.
  - Basata su: `piano_api_archaeology.pdf`, fasi operative e note di pubblicazione.
  - Tipo: fatto
  - Da verificare: no
- Decisione: ogni case study deve avere `README.md`, `fetch.py`, `parse.py`, `sample.csv`.
  - Basata su: `method_ethics_api_archaeology.pdf`, note finali.
  - Tipo: fatto
  - Da verificare: no
- Decisione: gli script devono implementare rate limiting, User-Agent identificabile e rispetto di robots.txt.
  - Basata su: `method_ethics_api_archaeology.pdf`, `ETHICS.md`.
  - Tipo: fatto
  - Da verificare: no
- Decisione: il case study sportivo va reso generico e senza nomi/URL reali nel repo pubblico.
  - Basata su: `piano_api_archaeology.pdf`, sezione case study A.
  - Tipo: fatto
  - Da verificare: no

## Nota operativa
Questo brief e' stato compilato usando esclusivamente il contenuto dei PDF del workspace.
Le uniche parti lasciate aperte sono quelle che i PDF non fissano in modo definitivo.
