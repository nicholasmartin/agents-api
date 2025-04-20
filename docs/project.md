# CrewAI Backend Implementation Plan for Render Deployment

Here's a detailed step-by-step implementation plan for creating your CrewAI backend server and deploying it to Render.

## Step 1: Project Setup and Environment Configuration

First, let's set up our project structure and environment:

```
agents-api/
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI application
│   ├── models.py           # Pydantic models
│   └── core/
│       ├── __init__.py
│       ├── agents.py       # Agent definitions
│       ├── crews.py        # Crew configurations
│       ├── tasks.py        # Task definitions
│       └── llm.py          # LLM configuration
├── requirements.txt
├── Dockerfile              # For containerized deployment
└── .env                    # Environment variables (local only)
```

### Example code for `requirements.txt`:

```
fastapi==0.103.1
uvicorn==0.23.2
pydantic==2.3.0
crewai==0.36.0
langchain==0.0.335
langchain-openai==0.0.2
python-dotenv==1.0.0
python-multipart==0.0.6
```

### Example code for `.env`:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Step 2: Create Pydantic Models for API Requests/Responses

Let's define our data models for API interactions:

### Example code for `app/models.py`:

```python
from pydantic import BaseModel
from typing import List, Optional, Dict

class IdeaGenerationRequest(BaseModel):
    """Request model for generating startup ideas."""
    constraints: Optional[str] = None
    industry: Optional[str] = None
    technology_focus: Optional[str] = None

class ValidationRequest(BaseModel):
    """Request model for validating a startup idea."""
    idea: str

class IdeasResponse(BaseModel):
    """Response model for generated ideas."""
    ideas: List[Dict[str, str]]

class ValidationResponse(BaseModel):
    """Response model for validation results."""
    market_analysis: str
    technical_evaluation: str
    business_plan: str
```

## Step 3: Configure Language Model Integration

Set up the connection to your LLM provider:

### Example code for `app/core/llm.py`:

```python
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_llm():
    """Initialize and return the language model."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY environment variable")
        
    return ChatOpenAI(
        model="gpt-4",  # or another model of your choice
        temperature=0.7,
        api_key=api_key
    )
```

## Step 4: Define Agent Roles and Personalities

Create specialized agents for different aspects of startup analysis:

### Example code for `app/core/agents.py`:

```python
from crewai import Agent

def create_idea_generator(llm):
    """Creates an agent specialized in generating startup ideas."""
    return Agent(
        role="Startup Idea Generator",
        goal="Generate innovative and viable startup ideas based on market trends and opportunities",
        backstory="""You are a visionary entrepreneur with experience in identifying market gaps and creating 
        innovative solutions. You have a knack for spotting upcoming trends and have successfully launched 
        multiple startups across various industries. Your ideas are always practical yet forward-thinking.""",
        verbose=True,
        llm=llm
    )

def create_market_researcher(llm):
    """Creates an agent specialized in market research."""
    return Agent(
        role="Market Research Analyst",
        goal="Analyze market demand, competition, and potential customer base for startup ideas",
        backstory="""You are an expert at understanding market dynamics and identifying whether an idea has 
        real-world demand. You have extensive experience in consumer behavior analysis, market sizing, and 
        competitive analysis. You know how to identify a product's target audience and market fit.""",
        verbose=True,
        llm=llm
    )

def create_technical_evaluator(llm):
    """Creates an agent specialized in technical evaluation."""
    return Agent(
        role="Technical Feasibility Expert",
        goal="Evaluate the technical requirements and challenges of implementing a startup idea",
        backstory="""You have deep technical knowledge across various domains including software development, 
        hardware engineering, and emerging technologies. You can quickly assess the technical complexity of 
        an idea and identify potential implementation challenges. You're familiar with modern tech stacks and 
        can recommend the most efficient approach to building a product.""",
        verbose=True,
        llm=llm
    )

def create_business_strategist(llm):
    """Creates an agent specialized in business planning."""
    return Agent(
        role="Business Strategist",
        goal="Develop business models, revenue streams, and go-to-market strategies",
        backstory="""You excel at turning ideas into viable businesses with clear paths to profitability. 
        You have helped numerous startups develop their business models, fundraising strategies, and 
        go-to-market plans. You understand what investors look for and how to position a startup for success.""",
        verbose=True,
        llm=llm
    )
```

## Step 5: Create Task Definitions

Define the specific tasks each agent will perform:

### Example code for `app/core/tasks.py`:

```python
from crewai import Task

def create_idea_generation_task(agent, constraints=None, industry=None, technology_focus=None):
    """Creates a task for generating startup ideas."""
    context = ""
    if constraints:
        context += f"Consider these constraints: {constraints}\n"
    if industry:
        context += f"Focus on this industry: {industry}\n"
    if technology_focus:
        context += f"Leverage this technology: {technology_focus}\n"
        
    return Task(
        description=f"""Generate 3-5 innovative startup ideas based on current market trends and opportunities.
            For each idea, provide:
            1. Name: A catchy, memorable name for the startup
            2. Tagline: A single sentence that explains what the company does
            3. Problem: A clear description of the problem this solves
            4. Solution: How your product/service solves this problem
            5. Target Market: Who would use this product/service
            6. Unique Value Proposition: Why this is different from existing solutions
            7. Business Model: How the startup would make money
            
            {context}
            
            Format each idea clearly with these headings and make sure ideas are realistic, 
            implementable, and have genuine market potential.
        """,
        agent=agent,
        expected_output="A structured list of 3-5 detailed startup ideas with all required components."
    )

def create_market_analysis_task(agent, idea):
    """Creates a task for market analysis."""
    return Task(
        description=f"""Analyze the market potential for the following startup idea: {idea}
            
            Provide a comprehensive market analysis covering:
            
            1. Market Size & Growth:
               - Estimate the total addressable market (TAM) in dollars
               - Identify market growth rate and trends
            
            2. Target Customer Analysis:
               - Create detailed customer personas
               - Identify their pain points and needs
               - Estimate customer acquisition cost
            
            3. Competitive Landscape:
               - Identify key direct and indirect competitors
               - Analyze their strengths and weaknesses
               - Identify gaps in the market
            
            4. Market Entry Strategy:
               - Recommend channels to reach customers
               - Identify potential partnerships or distribution channels
               - Outline marketing approach
            
            5. Potential Challenges:
               - Identify market-specific barriers to entry
               - Highlight regulatory considerations
               - Note market risks and how to mitigate them
            
            Provide concrete, actionable insights rather than generic advice.
        """,
        agent=agent,
        expected_output="A comprehensive market analysis report with actionable insights."
    )

def create_technical_evaluation_task(agent, idea):
    """Creates a task for technical evaluation."""
    return Task(
        description=f"""Evaluate the technical feasibility of implementing the following startup idea: {idea}
            
            Provide a detailed technical assessment covering:
            
            1. Technology Stack:
               - Recommend primary technologies and frameworks
               - Justify your technology choices
            
            2. Development Complexity:
               - Rate complexity (Low/Medium/High) and explain why
               - Estimate development timeline for MVP
               - Identify key technical challenges
            
            3. Infrastructure Requirements:
               - Outline cloud services or physical infrastructure needed
               - Consider scalability requirements
            
            4. Technical Talent:
               - Identify key technical roles needed
               - Suggest team composition for development
            
            5. Technical Risks:
               - Identify potential technical roadblocks
               - Suggest mitigation strategies
            
            Be specific about technologies rather than giving generic advice.
        """,
        agent=agent,
        expected_output="A detailed technical feasibility assessment with specific technology recommendations."
    )

def create_business_plan_task(agent, idea, market_analysis, tech_evaluation):
    """Creates a task for business plan development."""
    return Task(
        description=f"""Develop a business plan outline for the following startup idea: {idea}
            
            Based on these analyses:
            
            Market Analysis Summary:
            {market_analysis}
            
            Technical Feasibility Summary:
            {tech_evaluation}
            
            Create a comprehensive business plan including:
            
            1. Business Model:
               - Value proposition
               - Revenue streams
               - Cost structure
               - Key partnerships
            
            2. Financial Projections:
               - Initial capital requirements
               - Path to profitability
               - Key financial metrics to track
            
            3. Go-to-Market Strategy:
               - Customer acquisition strategy
               - Pricing strategy
               - Sales channels
            
            4. Growth Strategy:
               - Expansion opportunities
               - Future product development
            
            5. Key Milestones:
               - 18-month timeline with specific goals
               - Success metrics for each milestone
            
            Be specific, practical, and provide actionable insights for a founder.
        """,
        agent=agent,
        expected_output="A comprehensive business plan outline with financial projections and milestone timeline."
    )
```

## Step 6: Configure Crew Orchestration

Set up the crews to coordinate agent activities:

### Example code for `app/core/crews.py`:

```python
from crewai import Crew, Process
from .agents import create_idea_generator, create_market_researcher, create_technical_evaluator, create_business_strategist
from .tasks import create_idea_generation_task, create_market_analysis_task, create_technical_evaluation_task, create_business_plan_task

def create_idea_generation_crew(llm, constraints=None, industry=None, technology_focus=None):
    """Creates a crew for generating startup ideas."""
    # Create agent
    generator = create_idea_generator(llm)
    
    # Create task
    generation_task = create_idea_generation_task(
        generator, 
        constraints=constraints,
        industry=industry,
        technology_focus=technology_focus
    )
    
    # Create crew
    crew = Crew(
        agents=[generator],
        tasks=[generation_task],
        verbose=True,
        process=Process.sequential
    )
    
    return crew

def create_idea_validation_crew(llm, idea):
    """Creates a crew for validating startup ideas."""
    # Create agents
    market_researcher = create_market_researcher(llm)
    tech_evaluator = create_technical_evaluator(llm)
    business_strategist = create_business_strategist(llm)
    
    # Create market and tech tasks
    market_task = create_market_analysis_task(market_researcher, idea)
    tech_task = create_technical_evaluation_task(tech_evaluator, idea)
    
    # Create first crew for market and tech analysis
    first_crew = Crew(
        agents=[market_researcher, tech_evaluator],
        tasks=[market_task, tech_task],
        verbose=True,
        process=Process.sequential  # Would use parallel if supported
    )
    
    # Get results from first tasks
    results = first_crew.kickoff()
    market_analysis = results[0]  # Result from market_task
    tech_evaluation = results[1]  # Result from tech_task
    
    # Create business plan task that depends on previous results
    business_task = create_business_plan_task(
        business_strategist, 
        idea, 
        market_analysis, 
        tech_evaluation
    )
    
    # Create final crew with business task
    final_crew = Crew(
        agents=[business_strategist],
        tasks=[business_task],
        verbose=True,
        process=Process.sequential
    )
    
    final_result = final_crew.kickoff()
    
    # Return all results
    return {
        "market_analysis": market_analysis,
        "technical_evaluation": tech_evaluation,
        "business_plan": final_result
    }
```

## Step 7: Create FastAPI Application

Set up the main FastAPI application with our endpoints:

### Example code for `app/main.py`:

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from .models import IdeaGenerationRequest, ValidationRequest
from .core.crews import create_idea_generation_crew, create_idea_validation_crew
from .core.llm import create_llm

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Startup Idea API",
    description="API for generating and validating startup ideas using AI agents",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint to verify the API is running."""
    return {"status": "healthy", "service": "startup-idea-api"}

# Generate ideas endpoint
@app.post("/generate")
async def generate_ideas(request: IdeaGenerationRequest):
    """Generate startup ideas based on optional constraints."""
    try:
        llm = create_llm()
        crew = create_idea_generation_crew(
            llm, 
            constraints=request.constraints,
            industry=request.industry,
            technology_focus=request.technology_focus
        )
        result = crew.kickoff()
        
        # Process the result to structure it better
        ideas = []
        raw_ideas = result.split("\n\n")
        for raw_idea in raw_ideas:
            if not raw_idea.strip():
                continue
                
            # Basic processing - this can be improved based on actual output format
            idea_dict = {}
            current_section = None
            
            for line in raw_idea.split("\n"):
                line = line.strip()
                if not line:
                    continue
                    
                # Check if this is a section header
                if ":" in line and len(line.split(":")[0]) < 30:
                    parts = line.split(":", 1)
                    key = parts[0].strip().lower().replace(" ", "_")
                    value = parts[1].strip() if len(parts) > 1 else ""
                    idea_dict[key] = value
                    current_section = key
                elif current_section:
                    # Append to current section
                    idea_dict[current_section] += " " + line
            
            if idea_dict:
                ideas.append(idea_dict)
        
        return {"ideas": ideas}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating ideas: {str(e)}")

# Validate idea endpoint
@app.post("/validate")
async def validate_idea(request: ValidationRequest):
    """Validate a startup idea with comprehensive analysis."""
    try:
        if not request.idea:
            raise HTTPException(status_code=400, detail="Idea is required")
        
        llm = create_llm()
        results = create_idea_validation_crew(llm, request.idea)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating idea: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
```

## Step 8: Create Dockerfile for Containerization

Prepare for deployment with a Dockerfile:

### Example code for `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PORT"]
```

## Step 9: Local Testing

Before deploying, test your application locally:

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

4. Test endpoints using curl or a tool like Postman:
   ```bash
   curl -X POST "http://localhost:8000/generate-ideas" -H "Content-Type: application/json" -d '{"industry": "Healthcare", "technology_focus": "AI"}'
   ```

## Step 10: Deploy to Render

Follow these steps to deploy your application to Render:

1. Create a Git repository for your project
2. Push your code to the repository
3. Log in to Render (render.com)
4. Create a new Web Service
5. Connect to your repository
6. Configure the deployment:
   - **Name**: `agents-api` (or your preferred name)
   - **Environment**: `Docker`
   - **Region**: Choose the region closest to your users
   - **Branch**: `main` (or your default branch)
   - **Environment Variables**: Add your `OPENAI_API_KEY`

7. Click "Create Web Service"

## Step 11: Update CORS Settings for Production

After deployment, update your CORS settings in `main.py` to only allow requests from your frontend domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mvpmaker.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Step 12: Test Your Deployed API

Verify your API is working correctly in production:

```bash
curl -X POST "https://agents-api.onrender.com/generate" -H "Content-Type: application/json" -d '{"industry": "Search engine optimization", "technology_focus": "AI"}'
```

## Step 13: Implement Rate Limiting and Monitoring (Optional)

For production use, consider adding rate limiting and monitoring:

### Example for adding rate limiting:

1. Add to requirements.txt:
   ```
   slowapi==0.1.7
   ```

2. Update `main.py`:
   ```python
   from slowapi import Limiter, _rate_limit_exceeded_handler
   from slowapi.util import get_remote_address
   from slowapi.errors import RateLimitExceeded

   limiter = Limiter(key_func=get_remote_address)
   app = FastAPI()
   app.state.limiter = limiter
   app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

   @app.post("/generate")
   @limiter.limit("5/hour")  # Limit to 5 requests per hour
   async def generate_ideas(request: IdeaGenerationRequest):
       # Existing code...
   ```

## Step 14: Set Up CI/CD Pipeline (Optional)

For continuous deployment, you can set up a GitHub Action:

### Example `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Render

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Render Deploy
        run: |
          curl -X POST "${{ secrets.RENDER_DEPLOY_HOOK_URL }}"
```

Then, set up a deploy hook in your Render dashboard and add it as a secret in your GitHub repository.

---

This implementation plan provides a complete guide to setting up your CrewAI backend server and deploying it to Render. By following these steps, you'll have a fully functional API that can generate and validate startup ideas using AI agents.

You can now connect this backend to your Next.js + Supabase frontend to complete your application.