# AWS Serverless Fitness API

A fully serverless REST API built on AWS to track workouts, weights, reps, and notes.

Designed as a scalable cloud-native fitness backend using AWS Lambda, API Gateway, and DynamoDB.

This project demonstrates real-world cloud engineering skills including serverless architecture, API design, and cloud database integration.

---

## Features

- Create workout entries
- Retrieve workout history
- Delete workouts
- Health check endpoint for monitoring
- Fully serverless architecture (no servers to manage)
- JSON-based API responses
- Tested with Postman

---

## Architecture

Client → API Gateway → Lambda → DynamoDB → Response

---

## AWS Services Used

- AWS Lambda — Backend compute (Python)
- Amazon API Gateway — REST API routing
- Amazon DynamoDB — NoSQL database storage
- Amazon CloudWatch — Logging and monitoring

---

## Example Endpoints

### Health Check

GET /health

### Get Workouts

GET: /workouts?userId=elvis


### Create Workout

POST /workouts


Body:
```json
{
  "userId": "elvis",
  "exercise": "Deadlift",
  "reps": 8,
  "weight": 315,
  "notes": "Felt strong"
}
```

---

## Author

**Elvis Uzomah**  
Cloud Engineering Portfolio Project

### Base API URL
`https://sliwhg53yf.execute-api.us-east-1.amazonaws.com/prod`


