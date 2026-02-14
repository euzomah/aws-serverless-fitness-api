# AWS Serverless Fitness API

A fully serverless REST API built on AWS to track workouts, including exercises, reps, weight, and notes.

This project demonstrates real-world cloud engineering skills using AWS Lambda, API Gateway, DynamoDB, and CloudWatch to build a scalable fitness tracking backend without managing servers.

---

## Project Overview

This API allows users to:

- Create workout entries
- Retrieve workout history
- Delete workouts
- Perform health checks for monitoring

Designed as a cloud-native backend for fitness applications.

---

## AWS Services Used

- AWS Lambda — Backend compute (Python)
- Amazon API Gateway — REST API routing
- Amazon DynamoDB — NoSQL database storage
- Amazon CloudWatch — Logging and monitoring

---

## Architecture

Client Request → API Gateway → Lambda Function → DynamoDB → Response

Fully serverless architecture:

- No server management
- Auto-scaling
- Pay-per-use
- Highly available

---

## Base API URL

```
https://sliwhg53yf.execute-api.us-east-1.amazonaws.com/prod
```

---

## Example Endpoints

### Health Check

**GET**
```
/health
```

**Response**
```json
{
  "ok": true,
  "service": "secure-fitness-api"
}
```

---

### Get Workouts

**GET**
```
/workouts?userId=elvis
```

Returns workout history for a user.

---

### Create Workout

**POST**
```
/workouts
```

**Body**
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

### Delete Workout

**DELETE**
```
/workouts/{workoutId}?userId=elvis
```

Deletes a specific workout entry.

---

## Testing

API tested using:

- Postman
- Direct API Gateway endpoint calls

---

## Future Improvements

- Authentication (Cognito / JWT)
- Frontend fitness dashboard
- Mobile app integration
- Analytics tracking
- CI/CD deployment pipeline

---

## Author

**Elvis Uzomah**  
Cloud Engineering Portfolio Project  

Focused on AWS Cloud Engineering, DevOps, and Security Architecture.

