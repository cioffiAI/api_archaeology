# LEARNINGS.md

Questo file raccoglie errori, limiti e lezioni emerse durante la creazione del progetto e dei suoi file di istruzioni.

## Errori e limiti osservati

1. I PDF sono presenti nel workspace, ma il primo tentativo di lettura diretta non è stato affidabile.
   - I file risultano essere PDF generati con ReportLab e compressi.
   - L'estrazione testuale semplice non ha prodotto contenuto leggibile in modo affidabile.

2. Nell'ambiente non era disponibile Python.
   - Il tentativo di usare `python` ha fallito perché il comando non esisteva.
   - Anche `py -3` non era disponibile.
   - Questo ha impedito di usare uno script rapido per estrarre il testo dai PDF.

3. Gli strumenti PDF locali non erano disponibili.
   - Non erano presenti comandi come `pdftotext`, `mutool`, `gswin64c` o `qpdf`.
   - Per questo è stato necessario limitarsi a ispezioni alternative e conservative.

4. I PDF inizialmente referenziati risultavano in un percorso sandbox diverso da quello del workspace visibile.
   - I file esistevano nella root del workspace, ma erano stati rilevati anche in un path interno alla sandbox.
   - Questo ha richiesto verifica del percorso reale prima di procedere con la scrittura dei file.

5. L'output di PowerShell ha mostrato problemi di codifica per i caratteri accentati.
   - Il contenuto scritto nel file è corretto.
   - La visualizzazione in console ha mostrato caratteri sostituiti, quindi non va usata come prova della qualità del file.

6. Il file di istruzioni doveva chiamarsi `AGENTS.md`, non `Agents.md`.
   - Il nome esatto è importante perché il modello e gli strumenti lo riconoscano in modo consistente.

## Lezioni apprese

- Prima di assumere il contenuto di un PDF, verificare se il testo è davvero estraibile.
- Se l'ambiente non ha Python o tool PDF dedicati, conviene ridurre le assunzioni e documentare chiaramente i limiti.
- Il percorso effettivo dei file va sempre verificato prima di scrivere nuovi documenti.
- La console può falsare la percezione del contenuto per via della codifica; serve controllare il file salvato, non solo l'output a schermo.
- I file di istruzioni del workspace devono essere espliciti, conservativi e facili da aggiornare.

## Cosa ricordare per i prossimi passi

- Se arrivano nuovi PDF o documenti, leggerli prima di modificare le istruzioni.
- Se servono estrazioni più precise, usare un ambiente con strumenti PDF adeguati.
- Evitare di trasformare un limite tecnico in una conclusione non verificata.
