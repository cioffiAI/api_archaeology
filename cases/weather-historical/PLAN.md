# Piano — Case Study Meteo Storico (ARPAE)

## Fonte dati

- **Ente**: ARPAE Emilia-Romagna (arpae.it / dati.arpae.it)
- **Endpoint**: `https://dati-simc.arpae.it/opendata/osservati/meteo/storico/`
- **Pattern URL**: `YYYY-MM.json.gz` (es. `2006-01.json.gz` → `2026-04.json.gz`)
- **Formato**: NDJSON (una stazione per riga), compresso gzip
- **Periodo**: 20 anni (2006-01 → 2026-04), **244 file mensili**
- **Licenza**: IODL 2.0

## Pattern — Time-Series Archive

A differenza del MIMIT (API attiva), qui la sfida è un **archivio storico strutturato** con:
1. Listing HTML che elenca tutti i file `YYYY-MM.json.gz`
2. Download di file mensili compressi in NDJSON
3. Parsing del JSON interno (ogni riga = una stazione + timestep)

Non serve scraping HTML complesso: si naviga la directory listing e si scaricano i `.json.gz` mensili.

## Schema JSON (verificato con 2024-01.json.gz)

Ogni riga è un oggetto JSON contenente **una singola stazione per un singolo timestep**:

```json
{
  "version": "0.1",
  "network": "agrmet",
  "ident": null,
  "lon": 958959,      // coordinate Gauss-Boaga est (cm)
  "lat": 4504139,     // coordinate Gauss-Boaga nord (cm)
  "date": "2024-01-01T00:00:00Z",  // ISO 8601 UTC
  "data": [
    {
      "timerange": [tipo, tempo, durata],
      "level": [livello, ...],
      "vars": { "B13011": {"v": 0.0}, ... }
    }
  ]
}
```

**Variabili chiave rilevate** (formato `BXXXXX` = codice BUFR):

| Codice | Descrizione | Unità |
|--------|-------------|-------|
| B12101 | Temperatura | K (Kelvin) |
| B13003 | Umidità relativa | % |
| B13011 | Precipitazione | mm |
| B07030/B07031 | Radiazione solare | W/m² |

**Coordinate**: Gauss-Boaga in cm (es. lon=958959 → ~9.59°E, lat=4504139 → ~45.04°N).

**Timerange**: array `[tipo, tempo_agg, durata]`
- tipo 0=istantaneo, 1=media, 2=min, 3=max, 254=processato
- durata: 0=nessuna, 900=15min, 3600=1h, 86400=1gg

**Livello**: `[tipo_livello, valore, ...]` — 103/2000 = altezza in m slm.

## Struttura progetto

```
cases/weather-historical/
├── fetch.py          # robots.txt check, listing parsing, download .json.gz, decompress
├── parse.py          # modello Pydantic, parsing NDJSON, estrazione variabili chiave
├── sample.csv        # output sample (prima stazione di un mese, ~20 record)
└── README.md         # documentazione caso
```

## Implementazione

### fetch.py
1. Check `robots.txt` di `dati-simc.arpae.it` (404 = permesso)
2. Fetch `https://dati-simc.arpae.it/opendata/osservati/meteo/storico/`
3. Parsare link `YYYY-MM.json.gz` → collezione di URL
4. Scaricare UN mese (es. `2024-01.json.gz`) come sample
5. Decompress in-memory (gzip) → passare a parse.py
6. Institutional delay: 2.0s tra richieste

### parse.py

```python
class StationObs(BaseModel):
    station_name: str      # B01019
    network: str           # agrmet
    lon: float             # Gradi decimali
    lat: float             # Gradi decimali
    timestamp: datetime    # UTC
    temperature_k: float | None   # B12101
    humidity_pct: float | None     # B13003
    precipitation_mm: float | None # B13011
    solar_rad_wm2: float | None    # B07030
```

Il parsing è complesso: ogni riga contiene MULTIPLI blocchi `data[]` con `timerange` diversi.
Per il sample si estrae il timestep istantaneo (tipo=0, durata=0) se disponibile.

### README.md
- Overview del pattern
- Dati source con link
- Schema con codici BUFR
- Reproduction steps

## Verifiche completate

- [x] `robots.txt` → 404 (nessun divieto esplicito)
- [x] Index HTML elenca 244 file `YYYY-MM.json.gz`
- [x] Schema JSON verificato con download diretto di 2024-01.json.gz

## Rischi noti

- **Volume**: 10-24 MB per file mensile × 244 mesi = ~3.5 GB totali compressi
- **Complessità parsing**: struttura nested con `data[]`, `timerange`, `level` — servono filtri per variabile/durata
- **Codici BUFR**: necessaria tabella di decodifica per interpretare B12101 etc.

## TODO

- [x] Scrivere fetch.py
- [x] Scrivere parse.py
- [x] Generare sample.csv
- [x] Scrivere README.md