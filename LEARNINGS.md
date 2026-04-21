# LEARNINGS.md

Questo file raccoglie errori, limiti e lezioni emerse durante la creazione del progetto e dei suoi file di istruzioni.

## Errori e limiti osservati

1. I PDF sono presenti nel workspace, ma il primo tentativo di lettura diretta non e' stato affidabile.
   - I file risultano essere PDF generati con ReportLab e compressi.
   - L'estrazione testuale semplice non ha prodotto contenuto leggibile in modo affidabile.

2. Nell'ambiente non era disponibile Python.
   - Il tentativo di usare `python` ha fallito perche' il comando non esisteva.
   - Anche `py -3` non era disponibile.
   - Questo ha impedito di usare uno script rapido per estrarre il testo dai PDF.

3. Gli strumenti PDF locali non erano disponibili.
   - Non erano presenti comandi come `pdftotext`, `mutool`, `gswin64c` o `qpdf`.
   - Per questo e' stato necessario limitarsi a ispezioni alternative e conservative.

4. I PDF inizialmente referenziati risultavano in un percorso sandbox diverso da quello del workspace visibile.
   - I file esistevano nella root del workspace, ma erano stati rilevati anche in un path interno alla sandbox.
   - Questo ha richiesto verifica del percorso reale prima di procedere con la scrittura dei file.

5. L'output di PowerShell ha mostrato problemi di codifica per i caratteri accentati.
   - Il contenuto scritto nel file puo' essere corretto anche quando la console mostra caratteri sostituiti.
   - La visualizzazione in console non va usata come unica prova della qualita' del file.

6. Il file di istruzioni doveva chiamarsi `AGENTS.md`, non `Agents.md`.
   - Il nome esatto e' importante perche' il modello e gli strumenti lo riconoscano in modo consistente.

7. Il primo target sportivo valutato non e' stato tracciato in modo abbastanza preciso nel workspace.
   - Il dominio ricordato informalmente e il dominio effettivo osservato possono divergere.
   - Senza una traccia verificabile del target reale, il rischio e' costruire conclusioni su un riferimento sbagliato.

8. Nel caso sportivo c'era un errore concreto di naming: `Gaoloo.com` invece di `Goaloo.com`.
   - L'errore non era innocuo, perche' `gaoloo.com` oggi non coincide con il sito sportivo osservato.
   - Una variazione minima nel dominio puo' falsare review su `robots.txt`, ToS e stato del target.

## Lezioni apprese

- Prima di assumere il contenuto di un PDF, verificare se il testo e' davvero estraibile.
- Se l'ambiente non ha Python o tool PDF dedicati, conviene ridurre le assunzioni e documentare chiaramente i limiti.
- Il percorso effettivo dei file va sempre verificato prima di scrivere nuovi documenti.
- La console puo' falsare la percezione del contenuto per via della codifica; serve controllare il file salvato, non solo l'output a schermo.
- I file di istruzioni del workspace devono essere espliciti, conservativi e facili da aggiornare.
- Nei case study con target non pubblicato, la tracciabilita' del dominio e del contesto osservato va conservata meglio, altrimenti il writeup diventa ambiguo.
- Prima di concludere che un target sia cambiato o non esista piu', conviene verificare anche errori banali di naming del dominio.

## Cosa ricordare per i prossimi passi

- Se arrivano nuovi PDF o documenti, leggerli prima di modificare le istruzioni.
- Se servono estrazioni piu' precise, usare un ambiente con strumenti PDF adeguati.
- Evitare di trasformare un limite tecnico in una conclusione non verificata.
- Quando un target viene tenuto fuori dal repo pubblico, conviene conservare almeno una nota privata verificabile sul dominio reale e sul contesto del test.
- Nel caso sportivo, ogni review futura va fatta sul dominio corretto `Goaloo.com` e non su varianti simili.
