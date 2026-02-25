# Music Practice SRS - Installation Guide

## Quick Start (Web App - Recommended)

### What You Need:
- Any modern web browser (Chrome, Firefox, Safari, Edge)
- No server, no installation, no dependencies!

### Files Required:
```
music-practice-app/
├── practice-app.html
├── practice-app.js
└── practice-app-styles.css
```

### Installation Steps:

1. **Create a folder** anywhere on your computer:
   ```
   mkdir ~/music-practice-app
   cd ~/music-practice-app
   ```

2. **Download these 3 files** into that folder:
   - `practice-app.html`
   - `practice-app.js`
   - `practice-app-styles.css`

3. **Open the app**:
   - Double-click `practice-app.html`
   - OR right-click → Open With → Your Browser
   - OR drag the file into your browser window

4. **That's it!** The app is now running.

### First Use:

1. Click "Add New Piece"
2. Enter:
   - Title: "Test Sonata"
   - Start: 1
   - End: 100
   - Tempo: 120
3. Click "Start Practice"
4. Run through the tempo search
5. Watch it auto-create hot spots and child segments!

### Your Data:

- Stored in **browser localStorage**
- Persists between sessions
- View in browser DevTools → Application → Local Storage
- To clear test data: Data Management → Clear All Data

---

## Advanced: Deploy to Website

### Upload to timowen.me:

```
timowen.me/saxophone/practice-app/
├── practice-app.html
├── practice-app.js
└── practice-app-styles.css
```

Then visit: `https://timowen.me/saxophone/practice-app/practice-app.html`

---

## Optional: Python CLI Version

If you want to test the command-line version:

### Files Required:
```
music-practice-python/
├── practice_data_model.py
├── practice_database.py
└── practice_session.py
```

### Installation:

1. **Create folder**:
   ```bash
   mkdir ~/music-practice-python
   cd ~/music-practice-python
   ```

2. **Download files** into that folder

3. **Run**:
   ```bash
   python3 practice_session.py
   ```

4. **Follow prompts** to add pieces and practice

### Your Data:

- Stored in `~/practice_data/`
  - `nodes.json` - All your pieces/segments/hot spots
  - `sessions.json` - Practice history

---

## Migrating from Anki

### Prerequisites:

1. Install **CrowdAnki** add-on in Anki (code: 1788670778)
2. Export your Repertoire deck as JSON

### Steps:

1. Open the web app
2. Go to "Data Management"
3. Click "Import from Anki"
4. Select your exported JSON file
5. Your entire practice tree imports with preserved SRS schedules!

See `ANKI_IMPORT_GUIDE.md` for detailed instructions.

---

## Troubleshooting

### "Nothing happens when I click Start Practice"

**Fix:** Add a piece first (click "Add New Piece")

### "My data disappeared"

**Check:**
- Are you using the same browser?
- Did you clear browser data/cookies?
- Try: Browser DevTools → Application → Local Storage

**Prevention:** 
- Use Data Management → Export Data regularly
- Save the JSON file as backup

### "Import from Anki isn't working"

**Check:**
- File is valid JSON (open in text editor)
- Exported with CrowdAnki (not regular Anki export)
- Contains "notes" array

---

## File Descriptions

### Web App (Recommended)
- **practice-app.html** - Main interface
- **practice-app.js** - All logic (tempo search, SRS, data management)
- **practice-app-styles.css** - Beautiful styling

### Python CLI (Optional)
- **practice_data_model.py** - Data structures
- **practice_database.py** - Storage layer
- **practice_session.py** - Practice flow

### Documentation
- **ANKI_IMPORT_GUIDE.md** - How to migrate from Anki
- **DATA_STRUCTURE_ANALYSIS.md** - Technical explanation
- **example_workflow.py** - Code examples

---

## Next Steps After Installation

1. **Test with dummy data**
   - Add 2-3 test pieces
   - Practice them to see how hot spots are created
   - Explore the queue and library

2. **Clear test data**
   - Data Management → Clear All Data
   - Confirm twice

3. **Import from Anki** (if migrating)
   - Follow ANKI_IMPORT_GUIDE.md
   - OR start fresh by adding real pieces

4. **Start practicing!**
   - App will auto-show next due node
   - Tree builds automatically
   - SRS handles scheduling

---

## Support

Questions? Check:
- `DATA_STRUCTURE_ANALYSIS.md` - How it works
- `ANKI_IMPORT_GUIDE.md` - Migration details
- Browser console (F12) - For any errors

---

## Tips

**Backup your data:**
- Data Management → Download All Data
- Save JSON file somewhere safe
- Do this before clearing browser data

**Best practices:**
- Practice due nodes daily
- Add notes to hot spots (helps memory)
- Let SRS algorithm guide your practice schedule

**Progressive Web App (future):**
- Add to home screen on mobile
- Works offline
- Syncs across devices (planned feature)
