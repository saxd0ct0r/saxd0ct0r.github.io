# Music Practice SRS

**Incremental Processing with Spaced Repetition**  
*by Timothy J. Owen, D.M.A.*

A systematic approach to music practice that automatically manages complex hierarchical structures of pieces, segments, and "hot spots" using spaced repetition scheduling.

---

## Quick Start

### Web App (Recommended)

1. Download these 3 files:
   - `practice-app.html`
   - `practice-app.js`
   - `practice-app-styles.css`

2. Put them in a folder together

3. Double-click `practice-app.html`

4. Add a piece and start practicing!

**See `INSTALLATION_GUIDE.md` for detailed instructions.**

---

## What This Does

### The Problem

Traditional practice approaches:
- Manually track what needs work
- Forget to revisit difficult passages
- No systematic method for breaking down complex pieces
- Guesswork about tempo progression

### The Solution

This app:
- **Automatically finds** the hardest measure in any passage
- **Splits pieces** into manageable segments
- **Schedules practice** using proven spaced repetition
- **Tracks tempo progress** with binary search algorithm
- **Manages the tree structure** without manual overhead

### How It Works

1. **Add a piece** (e.g., "Adelaide Sonata, mm.1-120, 144 BPM")
2. **Practice it** - Run the tempo search
3. **Find hot spot** - App identifies hardest measure (e.g., m.47 at step -7)
4. **Auto-creates 3 nodes:**
   - Hot spot card (m.47)
   - Before segment (mm.1-48)
   - After segment (mm.47-120)
5. **SRS scheduling** - Each node gets independent schedule
6. **Repeat** - Tree grows automatically as you practice

---

## Features

### ✅ Incremental Processing
- Binary tree decomposition of musical pieces
- Automatic hot spot detection
- Child segment generation
- Unlimited tree depth

### ✅ Tempo Training
- Step-based system (16 steps per doubling)
- Binary search algorithm
- Calculated vs Quantized tempo display
- Percentage tracking

### ✅ Spaced Repetition
- Anki SM-2 algorithm
- Auto-rating based on improvement
- Due date scheduling
- Practice queue management

### ✅ Data Management
- Export/import (JSON)
- Anki migration support
- Clear test data
- Session history

---

## Files Included

### Web Application
- **practice-app.html** - Main interface
- **practice-app.js** - Application logic
- **practice-app-styles.css** - Styling

### Python CLI (Optional)
- **practice_data_model.py** - Data structures
- **practice_database.py** - Storage layer  
- **practice_session.py** - Interactive practice

### Documentation
- **INSTALLATION_GUIDE.md** - Setup instructions ⭐ **START HERE**
- **ANKI_IMPORT_GUIDE.md** - Migrate from Anki
- **DATA_STRUCTURE_ANALYSIS.md** - Technical deep-dive

### Examples
- **example_workflow.py** - Code walkthrough
- **tempo_trainer.py** - Standalone tempo trainer

---

## Technology

**Web App:**
- Pure HTML/CSS/JavaScript
- No dependencies, no server needed
- localStorage for data persistence
- Works offline

**Python:**
- Python 3.8+
- No external dependencies
- JSON file storage

---

## Migrating from Anki

Already using the Anki "Repertoire" note type?

1. Export deck with CrowdAnki add-on
2. Import JSON into app
3. Entire tree structure preserved
4. SRS schedules maintained

See `ANKI_IMPORT_GUIDE.md` for details.

---

## How to Use

### First Time:
1. Add a piece
2. Practice until you find a hot spot
3. Watch the app create child nodes
4. Practice the hot spot independently
5. Eventually practice parent again (reassembly)

### Daily Practice:
1. Click "Start Practice"
2. App shows most overdue node
3. Run tempo search
4. Rate automatically
5. Continue to next due node

---

## Architecture

### Data Model
```javascript
PracticeNode {
  id, title, measures, targetTempo,
  currentStep,           // Progress tracking
  parentId, childrenIds, // Tree structure
  srs: {                 // Scheduling
    interval, dueDate, easeFactor
  }
}

PracticeSession {
  nodeId, achievedStep, rating,
  hotSpotDiscovered, timestamp
}
```

### Algorithms
- **Tempo Search:** Binary search O(log n)
- **Tree Structure:** Explicit pointers
- **SRS:** Anki SM-2 algorithm
- **Data:** Normalized (1NF)

See `DATA_STRUCTURE_ANALYSIS.md` for CS best practices.

---

## Future Features

- [ ] Integrated metronome
- [ ] Tempo maps (for rubato/meter changes)
- [ ] Progress charts/analytics
- [ ] Cloud sync
- [ ] Mobile app (PWA)
- [ ] Sheet music integration

---

## License

Personal use by Timothy J. Owen.

---

## Credits

**Concept & Design:** Timothy J. Owen, D.M.A.  
**Implementation:** Built with Claude (Anthropic)  
**Algorithms:**
- Binary search tempo training
- Anki SM-2 spaced repetition
- Step-based tempo scaling (2^(n/16))

---

## Support

For questions or issues, refer to:
- `INSTALLATION_GUIDE.md` - Setup help
- `DATA_STRUCTURE_ANALYSIS.md` - How it works
- Browser console (F12) - Error messages

---

**Built February 2026**
