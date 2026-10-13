# SecureWatch

SecureWatch is a web-based cybersecurity event monitoring system developed
using Flask and Apache CouchDB.

The application demonstrates the use of a document-oriented NoSQL database
for storing and managing different types of cybersecurity events.

## Features

- Create cybersecurity events
- View stored events
- Update severity, status, and analyst notes
- Delete events
- Filter events using CouchDB Mango queries
- Store different event types using flexible JSON documents
- Demonstrate CouchDB document revisions
- Demonstrate CouchDB indexing
- Demonstrate database replication
- Dashboard displaying live event statistics

## Technologies Used

- Python
- Flask
- Apache CouchDB
- Docker
- HTML
- CSS
- JavaScript
- CouchDB Fauxton
- Git and GitHub

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
├── app.py
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md