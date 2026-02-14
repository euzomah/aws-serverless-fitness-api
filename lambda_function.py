import json
import os
import uuid
from datetime import datetime, timezone
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def to_decimal(x):
    # DynamoDB does NOT allow Python float types.
    # Always convert numbers to Decimal using str() to avoid float issues.
    return Decimal(str(x))


def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body, default=str),
    }


def get_method_and_path(event):
    # HTTP API (v2) usually uses rawPath + requestContext.http.method
    method = (
        event.get("requestContext", {})
        .get("http", {})
        .get("method", "")
    )
    path = event.get("rawPath", "") or event.get("path", "")

    # IMPORTANT: strip stage prefix like "/prod"
    stage = event.get("requestContext", {}).get("stage")
    if stage:
        stage_prefix = f"/{stage}"
        if path.startswith(stage_prefix + "/"):
            path = path[len(stage_prefix):]  # turns "/prod/health" -> "/health"
        elif path == stage_prefix:
            path = "/"  # edge case

    return method, path


def lambda_handler(event, context):
    try:
        method, path = get_method_and_path(event)

        # -------------------------
        # Health
        # -------------------------
        if path == "/health" and method == "GET":
            return response(200, {"ok": True, "service": "secure-fitness-api"})

        # -------------------------
        # POST /workouts
        # -------------------------
        if path == "/workouts" and method == "POST":
            body = json.loads(event.get("body") or "{}")

            required = ["userId", "exercise", "reps", "weight"]
            missing = [k for k in required if k not in body]
            if missing:
                return response(400, {"error": f"Missing fields: {missing}"})

            workout_id = str(uuid.uuid4())
            now_iso = datetime.now(timezone.utc).isoformat()

            item = {
                "userId": str(body["userId"]),
                "workoutId": workout_id,
                "exercise": str(body["exercise"]),
                "reps": int(body["reps"]),
                "weight": to_decimal(body["weight"]),
                "notes": str(body.get("notes", "")),
                "createdAt": now_iso,
            }

            table.put_item(Item=item)
            return response(201, {"message": "Workout created successfully", "item": item})

        # -------------------------
        # GET /workouts?userId=elvis
        # -------------------------
        if path == "/workouts" and method == "GET":
            qs = event.get("queryStringParameters") or {}
            user_id = qs.get("userId")
            if not user_id:
                return response(400, {"error": "Provide ?userId=..."})

            resp = table.query(KeyConditionExpression=Key("userId").eq(user_id))
            items = resp.get("Items", [])
            items.sort(key=lambda x: x.get("createdAt", ""), reverse=True)
            return response(200, {"count": len(items), "items": items})

        # -------------------------
        # DELETE /workouts/{workoutId}?userId=elvis
        # -------------------------
        if path.startswith("/workouts/") and method == "DELETE":
            workout_id = path.split("/workouts/")[1].strip()
            qs = event.get("queryStringParameters") or {}
            user_id = qs.get("userId")
            if not user_id:
                return response(400, {"error": "Provide ?userId=..."})

            table.delete_item(Key={"userId": user_id, "workoutId": workout_id})
            return response(200, {"message": "Workout deleted", "workoutId": workout_id})

        # fallback
        return response(404, {"error": "Route not found", "path": path, "method": method})

    except Exception as e:
        return response(500, {"error": str(e)})

