# 🏭 AluMatrix-Tracker 2.0 (aluminum extrusion system)

Choose your language / Scegli la tua lingua:
* [🇬🇧 English Version](#-english-version)
* [🇮🇹 Versione Italiana](#-versione-italiana)

---

### 🇬🇧 English Version

AluMatrix-Tracker 2.0 is an enterprise-grade industrial desktop application and REST API backend, built with Python, CustomTkinter, and FastAPI. Designed specifically for the aluminum extrusion sector, it serves as a distributed operator terminal to manage extrusion matrices (molds), technical drawings, and shift logs across the factory floor.

#### 🚀 Core Features

* **Client-Server Architecture:** Centralized data and file management allowing multiple operator terminals to sync seamlessly via a unified API.
* **Matrix Data Management:** Input a matrix code to immediately fetch related data from the SQL database, validated dynamically based on engineering rules.
* **Network File Transfer:** Seamless uploading (POST) and downloading (GET) of PDF Technical Drawings and JPG "Incestatura" photos via the centralized FastAPI server.
* **Database-Backed Dynamic Technical Sheets (Scheda Tecnica):** An object-oriented, dynamically rendered form that records extrusion parameters. Features an expandable card UI, with complex data payloads safely stored as JSON within SQLite via SQLAlchemy.
* **Electronic Shift Logs (Rapportino):**
    * Divided into standard industrial shifts (Turno D, E, F).
    * Real-time CRUD operations synchronized with the relational database.
    * Displayed in stylized, high-performance tables (CTkTable).
    * Right-click context menus for editing and deleting historical records.
* **Asynchronous Processing:** Uses background threading and the `requests` library for all API calls to ensure the UI never freezes during data I/O.

#### 🛠️ Tech Stack

* **Language:** Python 3.11+
* **Frontend Framework:** CustomTkinter (Modern UI) + PIL (Image Processing) + CTkTable
* **Backend Framework:** FastAPI + Uvicorn + SQLAlchemy
* **Data Persistence:** SQLite Relational Database (Replaced local JSON files)
* **Architecture:** Client-Server (REST API), OOP (Object-Oriented Programming), Multithreading

#### ⚙️ How to Run

**1. Clone the repository:**
```bash
git clone [https://github.com/your-username/AluMatrix-Tracker.git](https://github.com/your-username/AluMatrix-Tracker.git)
```

**2. Create a virtual environment and activate it:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**3. Install requirements:**
```bash
pip install customtkinter pillow CTkTable fastapi uvicorn sqlalchemy requests pydantic
```

**4. Run the API Server (Backend):**
```powershell
uvicorn server.api_server:app --reload
```

**5. Run the Application (Frontend Client):**
*Open a new terminal window, activate the venv, and run:*
```powershell
python main.py
```

---

### 🇮🇹 Versione Italiana

AluMatrix-Tracker 2.0 è un'applicazione desktop industriale di livello aziendale e un backend API REST, sviluppata in Python, CustomTkinter e FastAPI. Progettata specificamente per il settore dell'estrusione dell'alluminio, funge da terminale distribuito per gli operatori per gestire le matrici di estrusione, i disegni tecnici e i registri dei turni in tutta la fabbrica.

#### 🚀 Funzionalità Principali

* **Architettura Client-Server:** Gestione centralizzata di dati e file che consente a più terminali operatore di sincronizzarsi perfettamente tramite un'API unificata.
* **Gestione Dati Matrici:** Inserimento del codice matrice per recuperare immediatamente i dati dal database SQL, con validazione dinamica basata su regole di ingegneria.
* **Trasferimento File in Rete:** Caricamento (POST) e download (GET) fluido di Disegni Tecnici (PDF) e foto di Incestatura (JPG) tramite il server centralizzato FastAPI.
* **Scheda Tecnica Dinamica su Database:** Un modulo generato dinamicamente (Object-Oriented) che registra i parametri di estrusione. Interfaccia a schede espandibili, con payload di dati complessi archiviati in modo sicuro come JSON all'interno di SQLite tramite SQLAlchemy.
* **Rapportino Elettronico dei Turni:**
    * Suddiviso per turni industriali (Turno D, E, F).
    * Operazioni CRUD in tempo reale sincronizzate con il database relazionale.
    * Visualizzate in tabelle stilizzate e ad alte prestazioni (CTkTable).
    * Menu contestuali con clic destro per la modifica e l'eliminazione dei record storici.
* **Elaborazione Asincrona:** Utilizza il threading in background e la libreria `requests` per tutte le chiamate API, garantendo che l'interfaccia utente non si blocchi mai durante l'I/O dei dati.

#### 🛠️ Tecnologie Utilizzate

* **Linguaggio:** Python 3.11+
* **Framework Frontend:** CustomTkinter (Interfaccia Moderna) + PIL (Elaborazione Immagini) + CTkTable
* **Framework Backend:** FastAPI + Uvicorn + SQLAlchemy
* **Persistenza Dati:** Database Relazionale SQLite (Sostituisce i file JSON locali)
* **Architettura:** Client-Server (API REST), OOP (Programmazione Orientata agli Oggetti), Multithreading

#### ⚙️ Come Eseguire

**1. Clona il repository:**
```bash
git clone [https://github.com/your-username/AluMatrix-Tracker.git](https://github.com/your-username/AluMatrix-Tracker.git)
```

**2. Crea un ambiente virtuale e attivalo:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**3. Installa le dipendenze:**
```bash
pip install customtkinter pillow CTkTable fastapi uvicorn sqlalchemy requests pydantic
```

**4. Avvia il Server API (Backend):**
```powershell
uvicorn server.api_server:app --reload
```

**5. Esegui l'Applicazione (Client Frontend):**
*Apri una nuova finestra del terminale, attiva il venv ed esegui:*
```powershell
python main.py
```