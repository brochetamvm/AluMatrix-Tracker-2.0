🏭 Rapportino Elettronico (aluminum extrusion system)

Choose your language / Scegli la tua lingua:

🇬🇧 English Version

🇮🇹 Versione Italiana

🇬🇧 English Version

Rapportino Elettronico is an industrial desktop application built with Python and CustomTkinter, designed specifically for the aluminum extrusion sector. It serves as an operator terminal to manage extrusion matrices (molds), technical drawings, and shift logs.

🚀 Core Features

Matrix Data Management: Input a matrix code to immediately fetch related data and validate it dynamically based on engineering rules.

Network/Local Fallback Fetching: Automatically searches for PDF Technical Drawings and JPG "Incestatura" photos on company network drives, with a built-in fallback to local directories if the network is down.

Dynamic Technical Sheets (Scheda Tecnica): An object-oriented, dynamically rendered form that records extrusion parameters (Alloy, Press, Furnace zones, Cooling mechanisms, Puller/Saw settings). Features an expandable card UI.

Electronic Shift Logs (Rapportino): * Divided into standard industrial shifts (Turno D, E, F).

Real-time CRUD operations displayed in stylized tables (CTkTable).

Right-click context menus for editing and deleting historical records.

High Performance: Uses background threading for all JSON file reading/writing operations to ensure the UI never freezes during data I/O.

🛠️ Tech Stack

Language: Python 3.12+

GUI Framework: CustomTkinter (Modern UI) + PIL (Image Processing) + CTkTable

Data Persistence: Local JSON storage with structured data serialization.

Architecture: OOP (Object-Oriented Programming) + Multithreading.

⚙️ How to Run

Clone the repository:

git clone [https://github.com/your-username/Rapportino-Alexia.git](https://github.com/your-username/Rapportino-Alexia.git)



Create a virtual environment and activate it:

python -m venv .venv
.\.venv\Scripts\Activate.ps1



Install requirements:

pip install customtkinter pillow CTkTable



Run the application:

python main.py



🇮🇹 Versione Italiana

Rapportino Elettronico è un'applicazione desktop industriale sviluppata in Python con CustomTkinter, progettata specificamente per il settore dell'estrusione dell'alluminio. Funge da terminale per gli operatori per gestire le matrici di estrusione, i disegni tecnici e i registri dei turni.

🚀 Funzionalità Principali

Gestione Dati Matrici: Inserimento del codice matrice per recuperare immediatamente i dati correlati, con validazione dinamica basata su regole di ingegneria.

Ricerca File in Rete/Locale: Cerca automaticamente i Disegni Tecnici (PDF) e le foto di Incestatura (JPG) nelle unità di rete aziendali, con un sistema di fallback integrato su directory locali in caso di assenza di rete.

Scheda Tecnica Dinamica: Un modulo generato dinamicamente (Object-Oriented) che registra i parametri di estrusione (Lega, Pressa, Zone del Forno, Meccanismi di Raffreddamento ad aria/acqua, Puller e Taglio). Interfaccia a schede espandibili.

Rapportino Elettronico dei Turni: * Suddiviso per turni industriali (Turno D, E, F).

Operazioni CRUD in tempo reale visualizzate in tabelle stilizzate (CTkTable).

Menu contestuali con clic destro per la modifica e l'eliminazione dei record storici.

Alte Prestazioni: Utilizza il threading in background per tutte le operazioni di lettura/scrittura dei file JSON, garantendo che l'interfaccia utente non si blocchi mai durante l'I/O dei dati.

🛠️ Tecnologie Utilizzate

Linguaggio: Python 3.12+

Framework GUI: CustomTkinter (Interfaccia Moderna) + PIL (Elaborazione Immagini) + CTkTable

Persistenza Dati: Archiviazione locale tramite file JSON.

Architettura: OOP (Programmazione Orientata agli Oggetti) + Multithreading.

⚙️ Come Eseguire

Clona il repository:

git clone [https://github.com/your-username/Rapportino-Alexia.git](https://github.com/your-username/Rapportino-Alexia.git)



Crea un ambiente virtuale e attivalo:

python -m venv .venv
.\.venv\Scripts\Activate.ps1



Installa le dipendenze:

pip install customtkinter pillow CTkTable



Esegui l'applicazione:

python main.py