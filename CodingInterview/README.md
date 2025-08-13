# AI Ticket Classification - Technical Interview

## Overview

Build an AI-powered API that classifies support tickets by priority (1-5, where 1 = highest priority).

## Core Requirements

- Returns priority score 1-5 (1 = highest)
- Must use ChromaDB for at least one lookup
- Minimum 2 LLM nodes/calls
- Use LangChain or similar framework

## Setup Instructions

### Quick Start

```bash
# Simply run the setup script
./start_interview.sh
```

### Manual Testing (Optional)

```bash
# Test FastAPI is running
curl http://localhost:8000/health

# Test ChromaDB connection
curl http://localhost:8001/api/v1/heartbeat

# Run the test suite
python test_requests.py

# View logs
docker-compose logs -f
```

## ChromaDB Schema

**Collection Name:** `historical_tickets`

**Schema:**

- **documents**: Full ticket descriptions/titles
- **metadata**:
  ```json
  {  
    "priority": 1-5,
    "category": "login|billing|technical|access|performance",  
    "resolution_time_hours": 1-72,
    "user_type": "premium|standard|enterprise",
    "resolved": true|false
  }
  ```
- **ids**: "ticket_001", "ticket_002", etc.


## API Specification

### Endpoint: `POST /classify`

**Input:**
```json
{
  "title": "Can't access my account",
  "description": "I've been locked out since yesterday",
  "user_type": "premium",
  "affected_systems": ["login", "dashboard"]
}
```

**Output:**
```json
{
  "priority": 2,
  "reasoning": "Account access issue for premium user",
  "confidence": 0.85
}
```

## Sample Test Cases

### Test Case 1 - High Priority:
```json
{
  "title": "Production system down",
  "description": "All users unable to access main application",
  "user_type": "enterprise",
  "affected_systems": ["core", "database"]
}
```

### Test Case 2 - Low Priority:
```json
{
  "title": "Password reset help",
  "description": "Need help resetting my password",
  "user_type": "standard",
  "affected_systems": ["login"]
}
```

### Test Case 3 - Medium Priority:
```json
{
  "title": "Billing discrepancy",
  "description": "My invoice shows incorrect charges",
  "user_type": "premium",
  "affected_systems": ["billing"]
}
```

## Additional Notes

- You may use any tools/resources at your disposal (StackOverflow, Google, Claude, etc), within reason (don't one-shot prompt the solution, we want to see thoughtful design).
- Start with a simple solution
- Iterate and improve if time allows.

Good luck! 🚀