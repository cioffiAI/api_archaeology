# api-archaeology

Trovare le API dietro i siti web che fingono di non averne una.

## La tesi
Per molte categorie di dati, il mercato a pagamento esiste in larga parte per asimmetria informativa. La fonte pubblica esiste già, gratis, se sai dove guardare, e dove guardare è un'abilità che può essere insegnata.

Questo repository documenta un metodo per identificare endpoint HTTP non documentati dietro siti web ricchi di dati, con tre case study in domini non correlati:
- dati sportivi
- dati meteo storici
- prezzi carburanti

Il metodo è in `METHOD.md`. I vincoli etici e operativi sono in `ETHICS.md`.

## Perché conta
La maggior parte dei siti web moderni ricchi di dati sono thin client sopra i loro stessi backend API. Il browser chiama quelle API per renderizzare l'interfaccia. Se i dati sono pubblici e il sito non difende attivamente l'endpoint, il lavoro interessante non è lo HTML scraping. Il lavoro interessante è riconoscere quali chiamate backend contano, caratterizzarle correttamente, e decidere quando il riutilizzo è legittimo.

Questo repo riguarda quel passo di riconoscimento. Non è un framework di scraping e non è un tool di bypass.

## Struttura del repository
- `METHOD.md`: metodologia domain-agnostic in quattro fasi
- `ETHICS.md`: ambito, rate limiting, robots.txt, ToS e politica di rimozione
- `cases/sports-aggregator/`: scaffold del primo case study
- `cases/weather-historical/`: secondo case study completo (ARPAE Emilia-Romagna)
- `cases/fuel-prices-mimit/`: terzo case study completo (MIMIT osservatorio carburanti)
- `paper/`: output del mini-paper pianificato per la Fase 3

## Case studies
### `cases/sports-aggregator/`
Pattern: endpoint tabulari con filtro semantico.

Questo è il caso entry-level perché è il pattern più comune e più didattico. Nel repo pubblico, il target è intenzionalmente formulato in modo generico e non espone il nome del sito originale o dettagli endpoint live.

### `cases/weather-historical/`
Pattern: archivio storico strutturato — directory listing + file mensili compressi NDJSON.

ARPAE Emilia-Romagna pubblica 20 anni di osservazioni meteorologiche (2006–2026) come archivi mensili `.json.gz`, ciascuno contenente letture di stazioni a cadenza 15 minuti. Il parsing richiede la decodifica di variabili BUFR e la conversione di coordinate Gauss-Boaga.

### `cases/fuel-prices-mimit/`
Pattern: dati aperti già pubblicati, ma oscurati dall'interfaccia principale.

Questo caso si concentra sui dati dell'osservatorio prezzi carburanti italiano pubblicati sotto l'ecosistema MIMIT.

## Quickstart
```bash
uv venv
uv sync
python cases/sports-aggregator/fetch.py
```

L'attuale `fetch.py` è intenzionalmente uno scaffold. Applica i default di policy e si ferma prima di targetizzare qualsiasi endpoint reale.

## Etica e ambito
Questo repository è educativo. Gli script devono usare rate limit conservativi, un User-Agent identificabile, e nessun bypass di autenticazione. I raw dataset non sono redistribuiti qui. Solo piccoli campioni dimostrativi appartengono al repo.

Se rappresenti uno dei target documentati e vuoi che un case study sia modificato o rimosso, la policy in `ETHICS.md` si applica.

## Stato attuale
La Fase 2 è completata:
- scaffold del repo creato
- documenti di metodo ed etica creati
- `cases/fuel-prices-mimit/`: completo
- `cases/weather-historical/`: completo

Il case study `cases/sports-aggregator/` rimane uno scaffold in attesa di
caratterizzazione pubblica riproducibile (vedi README interno).