import os

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, redirect, url_for


load_dotenv()

app = Flask(__name__)


COUCHDB_URL = os.getenv("COUCHDB_URL")
DATABASE = os.getenv("COUCHDB_DATABASE")
COUCHDB_USER = os.getenv("COUCHDB_USER")
COUCHDB_PASSWORD = os.getenv("COUCHDB_PASSWORD")


@app.route("/")
def home():

    url = f"{COUCHDB_URL}/{DATABASE}/_find"

    query = {
        "selector": {
            "type": "security_event"
        }
    }

    response = requests.post(
        url,
        json=query,
        auth=(COUCHDB_USER, COUCHDB_PASSWORD)
    )

    if response.status_code != 200:
        return "Could not retrieve dashboard data from CouchDB", response.status_code

    events = response.json()["docs"]

    total_events = len(events)

    open_events = sum(
        1 for event in events
        if event.get("status") == "open"
    )

    investigating_events = sum(
        1 for event in events
        if event.get("status") == "investigating"
    )

    resolved_events = sum(
        1 for event in events
        if event.get("status") == "resolved"
    )

    critical_events = sum(
        1 for event in events
        if event.get("severity") == "critical"
    )

    return render_template(
        "dashboard.html",
        total_events=total_events,
        open_events=open_events,
        investigating_events=investigating_events,
        resolved_events=resolved_events,
        critical_events=critical_events
    )


@app.route("/test-db")
def test_database():
    url = f"{COUCHDB_URL}/{DATABASE}"

    response = requests.get(
        url,
        auth=(COUCHDB_USER, COUCHDB_PASSWORD)
    )

    if response.status_code == 200:
        return jsonify({
            "message": "Successfully connected to CouchDB",
            "database_info": response.json()
        })

    return jsonify({
        "message": "Could not connect to CouchDB",
        "status_code": response.status_code
    }), response.status_code


@app.route("/api/events")
def get_events():
    url = f"{COUCHDB_URL}/{DATABASE}/_find"

    query = {
        "selector": {
            "type": "security_event"
        }
    }

    response = requests.post(
        url,
        json=query,
        auth=(COUCHDB_USER, COUCHDB_PASSWORD)
    )

    if response.status_code == 200:
        return jsonify(response.json()["docs"])

    return jsonify({
        "message": "Could not retrieve security events",
        "status_code": response.status_code
    }), response.status_code


@app.route("/events")
def events_page():

    severity = request.args.get("severity", "")
    status = request.args.get("status", "")
    event_type = request.args.get("event_type", "")

    selector = {
        "type": "security_event"
    }

    if severity:
        selector["severity"] = severity

    if status:
        selector["status"] = status

    if event_type:
        selector["event_type"] = event_type

    query = {
        "selector": selector
    }

    url = f"{COUCHDB_URL}/{DATABASE}/_find"

    response = requests.post(
        url,
        json=query,
        auth=(COUCHDB_USER, COUCHDB_PASSWORD)
    )

    if response.status_code == 200:
        events = response.json()["docs"]

        return render_template(
            "events.html",
            events=events,
            selected_severity=severity,
            selected_status=status,
            selected_event_type=event_type
        )

    return "Could not retrieve events from CouchDB", response.status_code


@app.route("/create-event", methods=["GET", "POST"])
def create_event():

    if request.method == "POST":

        event_type = request.form["event_type"]

        event = {
            "type": "security_event",
            "event_type": event_type,
            "timestamp": request.form["timestamp"],
            "severity": request.form["severity"],
            "status": "open",
            "description": request.form["description"],
            "analyst_notes": ""
        }

        # Failed Login
        if event_type == "failed_login":
            event["username"] = request.form.get("username", "")
            event["source_ip"] = request.form.get("source_ip", "")
            event["hostname"] = request.form.get("hostname", "")

            failed_attempts = request.form.get("failed_attempts", "")

            if failed_attempts:
                event["failed_attempts"] = int(failed_attempts)

        # Malware Detection
        elif event_type == "malware_detection":
            event["hostname"] = request.form.get("hostname", "")
            event["source_ip"] = request.form.get("source_ip", "")
            event["malware_name"] = request.form.get("malware_name", "")
            event["file_path"] = request.form.get("file_path", "")

        # Phishing
        elif event_type == "phishing":
            event["sender_email"] = request.form.get("sender_email", "")
            event["recipient_email"] = request.form.get("recipient_email", "")
            event["subject"] = request.form.get("subject", "")

        # Network Anomaly
        elif event_type == "network_anomaly":
            event["source_ip"] = request.form.get("source_ip", "")
            event["destination_ip"] = request.form.get("destination_ip", "")
            event["protocol"] = request.form.get("protocol", "")

            source_port = request.form.get("source_port", "")
            destination_port = request.form.get("destination_port", "")

            if source_port:
                event["source_port"] = int(source_port)

            if destination_port:
                event["destination_port"] = int(destination_port)

        url = f"{COUCHDB_URL}/{DATABASE}"

        response = requests.post(
            url,
            json=event,
            auth=(COUCHDB_USER, COUCHDB_PASSWORD)
        )

        if response.status_code == 201:
            return redirect(url_for("events_page"))

        return "Could not create event", response.status_code

    return render_template("create_event.html")

@app.route("/event/<document_id>", methods=["GET", "POST"])
def event_details(document_id):

    url = f"{COUCHDB_URL}/{DATABASE}/{document_id}"

    response = requests.get(
        url,
        auth=(COUCHDB_USER, COUCHDB_PASSWORD)
    )

    if response.status_code != 200:
        return "Event not found", response.status_code

    event = response.json()

    if request.method == "POST":

        event["severity"] = request.form["severity"]
        event["status"] = request.form["status"]
        event["analyst_notes"] = request.form["analyst_notes"]

        update_response = requests.put(
            url,
            json=event,
            auth=(COUCHDB_USER, COUCHDB_PASSWORD)
        )

        if update_response.status_code == 201:
            return redirect(
                url_for(
                    "event_details",
                    document_id=document_id
                )
            )

        return "Could not update event", update_response.status_code

    return render_template(
        "event_details.html",
        event=event
    )


@app.route("/delete-event/<document_id>", methods=["POST"])
def delete_event(document_id):

    url = f"{COUCHDB_URL}/{DATABASE}/{document_id}"

    response = requests.get(
        url,
        auth=(COUCHDB_USER, COUCHDB_PASSWORD)
    )

    if response.status_code != 200:
        return "Event not found", response.status_code

    event = response.json()
    revision = event["_rev"]

    delete_response = requests.delete(
        url,
        params={"rev": revision},
        auth=(COUCHDB_USER, COUCHDB_PASSWORD)
    )

    if delete_response.status_code == 200:
        return redirect(url_for("events_page"))

    return "Could not delete event", delete_response.status_code


if __name__ == "__main__":
    app.run(debug=True, port=5001)