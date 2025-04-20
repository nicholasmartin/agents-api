# Agents API Documentation

This document provides information on how to use the CrewAI Startup Ideas API.

## Base URL

Production: `https://agents-api-ucmd.onrender.com`

## Endpoints

### Health Check

```
GET /
```

Returns a simple message to verify the API is running.

**Response:**
```json
{
  "message": "Welcome to the CrewAI Startup Ideas API"
}
```

### Generate Startup Ideas

```
POST /generate-ideas
```

Generates startup ideas based on optional constraints.

**Request Body:**
```json
{
  "industry": "Search engine optimization",
  "technology_focus": "AI",
  "constraints": "Must be B2B focused"
}
```

All fields are optional. If no fields are provided, the API will generate general startup ideas.

**Response:**
```json
{
  "ideas": [
    {
      "name": "SEOGenius",
      "tagline": "AI-powered SEO optimization platform",
      "problem": "SEO optimization is time-consuming and requires expertise",
      "solution": "Automated AI platform that analyzes and optimizes website content",
      "target_market": "Small to medium-sized businesses",
      "unique_value_proposition": "Fully automated SEO optimization with minimal human intervention",
      "business_model": "SaaS subscription model with tiered pricing"
    },
    // Additional ideas...
  ]
}
```

### Validate Startup Idea

```
POST /validate-idea
```

Provides a comprehensive analysis of a startup idea.

**Request Body:**
```json
{
  "idea": "An AI-powered SEO tool that automatically optimizes website content"
}
```

**Response:**
```json
{
  "market_analysis": "Detailed market analysis text...",
  "technical_evaluation": "Detailed technical evaluation text...",
  "business_plan": "Detailed business plan text..."
}
```

## How to Call the API

### Windows Command Prompt (CMD)

```
curl -X POST "https://agents-api-ucmd.onrender.com/generate-ideas" -H "Content-Type: application/json" -d "{\"industry\": \"Search engine optimization\", \"technology_focus\": \"AI\"}"
```

```
curl -X POST "https://agents-api-ucmd.onrender.com/validate-idea" -H "Content-Type: application/json" -d "{\"idea\": \"An AI-powered SEO tool that automatically optimizes website content\"}"
```

### PowerShell

Method 1 (using variables):
```powershell
$body = '{"industry": "Search engine optimization", "technology_focus": "AI"}'
Invoke-WebRequest -Uri "https://agents-api-ucmd.onrender.com/generate-ideas" -Method POST -Headers @{"Content-Type"="application/json"} -Body $body
```

Method 2 (direct):
```powershell
Invoke-WebRequest -Uri "https://agents-api-ucmd.onrender.com/generate-ideas" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"industry": "Search engine optimization", "technology_focus": "AI"}'
```

For validation:
```powershell
$body = '{"idea": "An AI-powered SEO tool that automatically optimizes website content"}'
Invoke-WebRequest -Uri "https://agents-api-ucmd.onrender.com/validate-idea" -Method POST -Headers @{"Content-Type"="application/json"} -Body $body
```

### Unix/Linux/macOS Terminal

```bash
curl -X POST "https://agents-api-ucmd.onrender.com/generate-ideas" -H "Content-Type: application/json" -d '{"industry": "Search engine optimization", "technology_focus": "AI"}'
```

```bash
curl -X POST "https://agents-api-ucmd.onrender.com/validate-idea" -H "Content-Type: application/json" -d '{"idea": "An AI-powered SEO tool that automatically optimizes website content"}'
```

## Notes

- The API may take some time to respond, especially for the validation endpoint, as it involves multiple AI agents working together.
- The API is rate-limited to protect resources.
- For production use, make sure to use HTTPS for all requests.
