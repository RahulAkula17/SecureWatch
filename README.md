## Project Structure

```text
SecureWatch/
├── static/
│   └── css/
│       └── style.css
├── templates/
│   ├── base.html
│   ├── create_event.html
│   ├── dashboard.html
│   ├── event_details.html
│   └── events.html
├── docs/
│   ├── SecureWatch_Final_Presentation.pptx
│   └── SecureWatch_Final_Report.pdf
├── app.py
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Prerequisites

Before running SecureWatch, install:

- Python 3
- Docker Desktop
- Git
- A modern web browser

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/RahulAkula17/SecureWatch.git
cd SecureWatch
```

### 2. Create a Python Virtual Environment

On Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file from `.env.example`.

On Windows:

```powershell
Copy-Item .env.example .env
```

On macOS/Linux:

```bash
cp .env.example .env
```

The `.env` file should contain:

```text
COUCHDB_URL=http://127.0.0.1:5984
COUCHDB_DATABASE=securewatch
COUCHDB_USER=admin
COUCHDB_PASSWORD=your_password_here
```

Replace `your_password_here` with the CouchDB administrator password you want to use.

The `.env` file is intentionally excluded from GitHub using `.gitignore`.

### 5. Start CouchDB Using Docker

Make sure Docker Desktop is running.

Then execute:

```bash
docker compose up -d
```

Verify that the CouchDB container is running:

```bash
docker ps
```

The container should appear as:

```text
securewatch-couchdb
```

CouchDB is available locally on port `5984`.

### 6. Open CouchDB Fauxton

Open the CouchDB administration interface:

```text
http://localhost:5984/_utils/
```

Log in using the administrator username and password configured in the `.env` file.

Create a database named:

```text
securewatch
```

Fauxton can also be used to inspect JSON documents, execute Mango queries, manage indexes, and perform database replication.

### 7. Run the Flask Application

From the SecureWatch project directory, run:

```bash
python app.py
```

The application will start at:

```text
http://127.0.0.1:5001
```

Open this address in a web browser to access the SecureWatch dashboard.

## Using SecureWatch

The application allows users to:

- Create new cybersecurity events
- View stored security events
- Filter events by event type, severity, and status
- View individual event details
- Update event severity, status, and analyst notes
- Delete events
- View live dashboard statistics

Supported event types include:

- Failed Login
- Malware Detection
- Phishing
- Network Anomaly

Each event is stored as a JSON document in CouchDB. Event types can contain different fields depending on the information associated with that event.

## CouchDB Features Demonstrated

SecureWatch demonstrates several NoSQL database features provided by Apache CouchDB:

- Flexible JSON document storage
- Create, read, update, and delete operations
- Mango queries
- JSON indexes
- Document revision tracking using `_rev`
- HTTP/REST-based database access
- Database replication

The Flask backend communicates with CouchDB using HTTP requests through the Python `requests` library.

## Database Replication

The project also demonstrates one-time CouchDB replication.

The primary database:

```text
securewatch
```

can be replicated to:

```text
securewatch_backup
```

using CouchDB Fauxton.

This demonstrates CouchDB's built-in database replication capability.

## Project Deliverables

The final project deliverables are available in the `docs` directory:

```text
docs/
├── SecureWatch_Final_Presentation.pptx
└── SecureWatch_Final_Report.pdf
```

## GitHub Repository

The complete source code, configuration files, documentation, presentation, and final report are available at:

```text
https://github.com/RahulAkula17/SecureWatch
```
