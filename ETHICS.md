# Etica e Politica di Ambito

Questo repository documenta una tecnica per accedere ai dati attraverso le API interne dei siti web. Tale tecnica è legittima per un insieme ristretto di usi e inappropriata per altri. Questo documento definisce il confine e le regole operative che si applicano a ogni case study in questo repository.

## Uso previsto
Questo repository è educativo. Gli usi appropriati includono:
- ricerca personale
- studio accademico
- giornalismo basato su dati pubblici
- analisi occasionali
- apprendimento di come le applicazioni web moderne espongono i loro dati

Usi inappropriati includono:
- costruire un servizio commerciale su endpoint non documentati
- scaricare in massa contenuti per redistribuzione
- eludere tier a pagamento che forniscono valore genuino
- targetizzare siti che proibiscono esplicitamente l'accesso automatizzato

## Regole operative
Ogni script in questo repository deve applicare i seguenti default:

### Rate limiting
- ritardo minimo di 2 secondi tra richieste allo stesso host
- default di 5 secondi per host più piccoli o istituzionali
- gli script devono rifiutare valori sotto 1 secondo

### User-Agent
Le richieste devono identificarsi onestamente, con un formato equivalente a:

`ApiArchaeology/1.0 (educational; +github.com/<user>/api-archaeology)`

Un'email di contatto deve essere configurabile tramite variabile d'ambiente.

### robots.txt
Gli script devono leggere `robots.txt` prima di eseguire e saltare i path esplicitamente disallow per crawler generali.

### Gestione dei dati
- nessuna redistribuzione di raw dataset nel repository
- solo piccoli campioni dimostrativi appartengono al version control
- nessun bypass di autenticazione

Se un target introduce successivamente autenticazione, il case study rilevante deve essere aggiornato e il codice rimosso o chiaramente marcato come non funzionante.

## Termini di servizio
Ogni case study deve citare i ToS del sito come osservati al momento dello studio e spiegare perché l'uso specifico educativo, rate-limited e non-redistributivo è o non è compatibile.

Dove i ToS sono ambigui, l'ambiguità deve essere dichiarata. Dove sono chiaramente prohibitivi, il case study non deve essere incluso.

## Richieste di rimozione
Se un operatore del sito chiede che un case study sia modificato o rimosso, la risposta default è compliance entro una settimana. L'argomento tecnico è solitamente cheap; il costo di reputazione non lo è.

## Responsabilità
Gli utenti sono responsabili di assicurare che qualsiasi uso reale rispetti la legge applicabile e i termini di servizio del sito target. Questo repository non endorsea usi derivati che eccedano l'ambito educativo qui descritto.

## Una regola sola
Se ti sentiresti a disagio a spiegare il workflow esatto all'operatore del sito, fermati. L'obiettivo è un metodo che rimane tecnicamente chiaro ed eticamente difendibile.