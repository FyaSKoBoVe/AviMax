# Simulatione di Utilizzo - CutFlow

## Scenario: Quick Cut per YouTube

### Persona: Marco (Content Creator)

**Obiettivo:** Tagliare un video di 5 minuti per rimuovere l'introduzione e l'outro, poi esportarlo per YouTube 1080p.

---

## Passo 1: Avvio dell'Applicazione

Marco apre CutFlow dal terminale:

```bash
python -m cutflow.app.main
```

L'applicazione si avvia mostrando:
- Finestra principale con tema scuro
- Pannello sinistro vuoto (Metadata, Filters, Export)
- Pannello destro con player video e timeline vuoti
- Barra dei menu in alto
- Toolbar con pulsanti (Import, Export, Undo, Redo, Settings)
- Status bar: "Ready"

---

## Passo 2: Importazione del Video

Marco clicca su **File → Import Video...** o usa il pulsante **Import** nella toolbar.

Si apre la dialog di selezione file:
```
/home/marco/Videos/raw_footage_2024.mp4
```

Dopo la selezione:
- Il video viene caricato nel player
- FFprobe estrae i metadati
- Il pannello **Metadata** si popola con:
  - File: raw_footage_2024.mp4
  - Duration: 05:23
  - Resolution: 1920x1080
  - Codec: H.264
  - FPS: 60
  - Bitrate: 8 Mbps
- Il video inizia a riprodursi automaticamente nel player

---

## Passo 3: Navigazione nel Video

Marco usa i controlli del player:
- **Play/Pause**: Spazio o pulsante Play
- **Stop**: Pulsante Stop
- **Seek**: Trascina lo slider o usa le frecce (←/→ per +/- 5 secondi)

Naviga fino al minuto 0:45 dove inizia il contenuto principale.

---

## Passo 4: Impostazione del Marker IN

Marco posiziona il cursore a 0:45 e:
- Premi il tasto **I** sulla tastiera
- Oppure clicca sul pulsante **Set In (I)** nella timeline

Il marker IN appare sulla timeline come un triangolo verde:
```
Timeline: [I_______________________]
          0:45
```

Il pannello Metadata mostra:
- In Point: 00:45.00

---

## Passo 5: Navigazione alla Fine del Contenuto

Marco continua a navigare fino al minuto 4:50 dove l'outro inizia.

---

## Passo 6: Impostazione del Marker OUT

Marco posiziona il cursore a 4:50 e:
- Premi il tasto **O** sulla tastiera
- Oppure clicca sul pulsante **Set Out (O)** nella timeline

Il marker OUT appare sulla timeline come un triangolo rosso:
```
Timeline: [I_______________________O]
          0:45                   4:50
```

Il pannello Metadata mostra:
- In Point: 00:45.00
- Out Point: 04:50.00
- Selected Duration: 04:05.00

---

## Passo 7: Configurazione dell'Export

Marco va al pannello **Export Settings**:

**Preset:** Seleziona "YouTube 1080p" dal dropdown
- Questo configura automaticamente:
  - Video Codec: libx264
  - Audio Codec: aac
  - Resolution: 1920x1080
  - Bitrate: 8M
  - CRF: 23
  - Preset: medium

**Mode:** Seleziona "Stream Copy" per un export veloce
- Poiché il codec originale è già H.264, può usare stream copy
- Questo evita la ricodifica e mantiene la qualità originale

---

## Passo 8: Anteprima del Segmento

Marco clicca **Play** nel player per verificare che il segmento selezionato sia corretto.
Il player riproduce solo la parte tra IN e OUT.

Soddisfatto della selezione, procede con l'export.

---

## Passo 9: Export

Marco clicca sul pulsante **Export** nel pannello Export.

Si apre la dialog di salvataggio:
```
/home/marco/Videos/exports/youtube_video_final.mp4
```

Clicca **Save**.

---

## Passo 10: Monitoraggio dell'Export

La **Export Queue** si apre automaticamente:

```
┌─────────────────────────────────────┐
│ Export Queue                 [X]    │
├─────────────────────────────────────┤
│ Job 1: raw_footage_2024.mp4 →      │
│        youtube_video_final.mp4     │
│ Status: Exporting...               │
│ Progress: ████████░░░░ 60%         │
│ Time remaining: 00:15              │
│ [Cancel]                            │
└─────────────────────────────────────┘
```

Marco può continuare a lavorare mentre l'export procede in background.

---

## Passo 11: Completamento dell'Export

Dopo circa 30 secondi (stream copy è veloce):

```
┌─────────────────────────────────────┐
│ Export Queue                 [X]    │
├─────────────────────────────────────┤
│ Job 1: raw_footage_2024.mp4 →      │
│        youtube_video_final.mp4     │
│ Status: Completed ✓                │
│ Duration: 04:05                    │
│ [Open] [Remove]                     │
└─────────────────────────────────────┘
```

Marco clicca **Open** per aprire il file nel file manager e verificarlo.

---

## Passo 12: Upload su YouTube

Marco apre YouTube Studio, trascina il file esportato, e lo carica.

Il video è perfettamente tagliato, mantiene la qualità originale, e ha le dimensioni ottimali per YouTube.

---

## Scenario Alternativo: Merge di Clip

### Persona: Giulia (Teacher)

**Obiettivo:** Unire tre clip di lezione in un unico video.

---

## Passo 1: Importazione delle Clip

Giulia importa tre file:
1. `lezione_parte1.mp4` (10:00)
2. `lezione_parte2.mp4` (12:30)
3. `lezione_parte3.mp4` (08:45)

---

## Passo 2: Selezione delle Clip

Nel pannello Metadata, Giulia vede tutte e tre le clip caricate nel progetto.

---

## Passo 3: Configurazione del Merge

Giulia usa il menu **Edit → Merge Clips...** (funzionalità pianificata).

Seleziona le tre clip nell'ordine desiderato:
1. lezione_parte1.mp4
2. lezione_parte2.mp4
3. lezione_parte3.mp4

---

## Passo 4: Configurazione dell'Export

**Preset:** Seleziona "YouTube 720p" per dimensioni più ridotte
**Mode:** "Reencode" per garantire codec uniformi

---

## Passo 5: Export

L'export queue mostra il job di merge:
```
Job 1: Merging 3 clips → lezione_completa.mp4
Status: Exporting...
Progress: ████████░░░░ 45%
```

---

## Passo 6: Completamento

Dopo circa 5 minuti (ricodifica di 30+ minuti di video):
```
Job 1: Merging 3 clips → lezione_completa.mp4
Status: Completed ✓
Duration: 31:15
```

Giulia ora ha un unico video di 31:15 pronto per la classe.

---

## Scenario con Filtri

### Persona: Alessandro (Video Editor)

**Obiettivo:** Applicare correzioni colore a un video.

---

## Passo 1: Importazione e Selezione

Alessandro importa `footage_scura.mp4`.

---

## Passo 2: Applicazione dei Filtri

Nel pannello **Filters**, Alessandro regola:
- **Brightness:** +0.15 (da 0.0 a 0.15)
- **Contrast:** +0.10 (da 0.0 a 0.10)
- **Saturation:** +0.05 (da 0.0 a 0.05)

Clicca **Add Filter** per aggiungere la catena di filtri.

---

## Passo 3: Anteprima

Il player mostra il video con i filtri applicati in tempo reale.

---

## Passo 4: Export con Filtri

**Mode:** "Reencode" (necessario per applicare i filtri)
**Preset:** Custom
- CRF: 20 (qualità più alta)
- Preset: slow (migliore compressione)

L'export applica i filtri durante la ricodifica.

---

## Scenario di Errore e Recovery

### Persona: Sofia (Social Media Manager)

**Obiettivo:** Export per Instagram, ma FFmpeg non è configurato.

---

## Passo 1: Tentativo di Export

Sofia importa un video e prova a esportare per Instagram.

Riceve un errore:
```
Error: FFmpeg not found
Please configure FFmpeg path in Settings
```

---

## Passo 2: Configurazione

Sofia apre **Edit → Preferences...**

Nella sezione **FFmpeg**:
- Clicca **Auto-detect**
- Il sistema trova FFmpeg in `/usr/bin/ffmpeg`
- Clicca **Apply**

---

## Passo 3: Riprova

Sofia riprova l'export e questa volta funziona correttamente.

---

## Statistiche della Sessione

### Marco (Quick Cut)
- **Tempo totale:** ~5 minuti
- **Tempo di export:** 30 secondi (stream copy)
- **Dimensione output:** 450 MB (da 600 MB originale)
- **Qualità:** Identica all'originale

### Giulia (Merge)
- **Tempo totale:** ~10 minuti
- **Tempo di export:** 5 minuti (ricodifica)
- **Dimensione output:** 1.2 GB
- **Durata totale:** 31:15

### Alessandro (Filtri)
- **Tempo totale:** ~15 minuti
- **Tempo di export:** 8 minuti (ricodifica lenta)
- **Dimensione output:** 380 MB
- **Qualità:** Alta (CRF 20)

---

## Note sull'Esperienza Utente

### Punti di Forza
- **Velocità:** Stream copy permette export quasi istantanei
- **Intuitivo:** Marcatori IN/OUT con scorciatoie da tastiera
- **Flessibilità:** Preset per diverse piattaforme
- **Non-blocking:** Export in background permette di continuare a lavorare

### Aree di Miglioramento
- **Merge Clips:** Funzionalità ancora da implementare completamente
- **Undo/Redo:** Potrebbe essere più visibile nella UI
- **Drag & Drop:** Importazione file potrebbe supportare drag & drop
- **Preview Filtri:** Anteprima in tempo reale potrebbe essere più fluida

---

## Conclusione

La simulazione mostra che CutFlow è efficace per:
- Tagli rapidi con stream copy
- Export multi-piattaforma con preset
- Applicazione di filtri base
- Gestione di export in coda

L'architettura MVVM e la separazione dei servizi permettono un'esperienza utente fluida e responsiva.
