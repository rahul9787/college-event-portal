import json
import os
import uuid
from datetime import datetime, timezone

import boto3
from boto3.dynamodb.conditions import Key


dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ["TABLE_NAME"]
ADMIN_TOKEN = os.environ["ADMIN_TOKEN"]

table = dynamodb.Table(TABLE_NAME)


EVENTS = [
    {
        "event_id": "TECH-001",
        "name": "Tech Fest",
        "date": "2026-08-20",
        "description": "Annual technical festival"
    },
    {
        "event_id": "HACK-001",
        "name": "Hackathon",
        "date": "2026-08-25",
        "description": "24-hour college hackathon"
    },
    {
        "event_id": "CULT-001",
        "name": "Cultural Fest",
        "date": "2026-08-30",
        "description": "College cultural celebration"
    }
]


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,X-Admin-Token",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
        },
        "body": json.dumps(body)
    }


def lambda_handler(event, context):

    method = event.get("requestContext", {}).get(
        "http", {}
    ).get("method", "")

    path = event.get("rawPath", "/")

    if method == "OPTIONS":
        return response(200, {"message": "OK"})

    # GET /events
    if method == "GET" and path == "/events":
        result = []

        for item in EVENTS:

            count = table.query(
                IndexName="EventIndex",
                KeyConditionExpression=Key("event_id").eq(
                    item["event_id"]
                ),
                Select="COUNT"
            )

            event_data = item.copy()
            event_data["registrations"] = count["Count"]

            result.append(event_data)

        return response(200, {"events": result})

    # POST /register
    if method == "POST" and path == "/register":

        try:
            body = json.loads(event.get("body") or "{}")
        except json.JSONDecodeError:
            return response(400, {"error": "Invalid JSON"})

        name = body.get("name", "").strip()
        email = body.get("email", "").strip()
        event_id = body.get("event_id", "").strip()

        if not name or not email or not event_id:
            return response(
                400,
                {
                    "error": "Name, email and event are required"
                }
            )

        selected_event = next(
            (e for e in EVENTS if e["event_id"] == event_id),
            None
        )

        if not selected_event:
            return response(
                400,
                {"error": "Invalid event"}
            )

        registration_id = str(uuid.uuid4())

        item = {
            "registration_id": registration_id,
            "name": name,
            "email": email,
            "event_id": event_id,
            "event_name": selected_event["name"],
            "registered_at": datetime.now(
                timezone.utc
            ).isoformat()
        }

        table.put_item(Item=item)

        return response(
            201,
            {
                "message": "Registration successful",
                "registration_id": registration_id
            }
        )

    # GET /events/{event_id}/count
    if method == "GET" and path.startswith("/events/") and path.endswith("/count"):

        parts = path.strip("/").split("/")

        if len(parts) != 3:
            return response(400, {"error": "Invalid path"})

        event_id = parts[1]

        count = table.query(
            IndexName="EventIndex",
            KeyConditionExpression=Key("event_id").eq(event_id),
            Select="COUNT"
        )

        return response(
            200,
            {
                "event_id": event_id,
                "registrations": count["Count"]
            }
        )

    # GET /admin/registrations
    if method == "GET" and path == "/admin/registrations":

        headers = event.get("headers") or {}

        supplied_token = (
            headers.get("x-admin-token")
            or headers.get("X-Admin-Token")
        )

        if supplied_token != ADMIN_TOKEN:
            return response(
                401,
                {"error": "Unauthorized"}
            )

        result = table.scan()

        return response(
            200,
            {
                "registrations": result.get("Items", [])
            }
        )

    return response(
        404,
        {"error": "Route not found"}
    )