from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import traceback
import logging
from typing import Dict, Any

from .models import (
    IdeaGenerationRequest,
    ValidationRequest,
    IdeasResponse,
    ValidationResponse
)
from .core.llm import create_llm
from .core.crews import (
    create_idea_generation_crew,
    create_idea_validation_crew
)

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="CrewAI Startup Ideas API",
    description="API for generating and validating startup ideas using CrewAI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://mvpmaker.vercel.app",  # Production frontend domain
        "http://localhost:3000",        # Frontend development server
        "http://localhost:8000",        # Local backend server
        "https://mvpmaker-nicks-projects-2e68032b.vercel.app"         # Vercel domain
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def root():
    """Root endpoint to check if API is running."""
    return {"message": "Welcome to the CrewAI Startup Ideas API"}

@app.post("/generate-ideas", response_model=IdeasResponse)
async def generate_ideas(request: IdeaGenerationRequest):
    """Generate startup ideas based on optional constraints."""
    try:
        # Log the request
        logging.debug(f"Received idea generation request: {request.dict()}")
        
        # Initialize language model
        logging.debug("Initializing language model")
        llm = create_llm()
        logging.debug("Language model initialized successfully")
        
        # Create and run crew
        logging.debug("Creating idea generation crew")
        crew = create_idea_generation_crew(
            llm=llm,
            constraints=request.constraints,
            industry=request.industry,
            technology_focus=request.technology_focus
        )
        logging.debug("Crew created successfully, starting kickoff")
        
        result = crew.kickoff()
        logging.debug(f"Crew kickoff completed with result type: {type(result)}")
        logging.debug(f"Raw result: {result}")
        
        # Parse the result into structured data
        ideas_list = []
        
        # Convert CrewOutput to string if necessary
        if hasattr(result, 'raw_output'):
            logging.debug("Processing CrewOutput object")
            result_text = str(result.raw_output)
        elif isinstance(result, str):
            logging.debug("Result is already a string")
            result_text = result
        else:
            logging.debug(f"Converting result of type {type(result)} to string")
            result_text = str(result)
        
        logging.debug(f"Processing result text: {result_text[:200]}...")
        
        try:
            # Try to parse as JSON first
            logging.debug("Attempting to parse result as JSON")
            ideas_list = json.loads(result_text)
            logging.debug("Successfully parsed result as JSON")
        except (json.JSONDecodeError, TypeError):
            # If not valid JSON, parse the text output into structured data
            logging.debug("Result is not JSON, parsing as text")
            ideas_list = []
            
            # Split by idea (assuming each idea is separated by double newlines)
            ideas_text = result_text.split("\n\n")
            current_idea = {}
            
            for idea_text in ideas_text:
                lines = idea_text.strip().split("\n")
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                        
                    if line.startswith("Name:") or line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("4.") or line.startswith("5."):
                        # Start of a new idea
                        if current_idea and "name" in current_idea:
                            ideas_list.append(current_idea)
                            current_idea = {}
                        
                        # Extract name
                        name_part = line.split(":", 1)
                        if len(name_part) > 1:
                            current_idea["name"] = name_part[1].strip()
                        else:
                            # If no colon, use the whole line as name
                            current_idea["name"] = line.strip()
                    elif ":" in line:
                        # Extract other fields
                        parts = line.split(":", 1)
                        key = parts[0].strip().lower().replace(" ", "_")
                        value = parts[1].strip()
                        current_idea[key] = value
            
            # Add the last idea if it exists
            if current_idea and "name" in current_idea:
                ideas_list.append(current_idea)
            
            logging.debug(f"Parsed {len(ideas_list)} ideas from text")
        
        logging.debug(f"Returning {len(ideas_list)} ideas")
        return {"ideas": ideas_list}
    
    except Exception as e:
        error_traceback = traceback.format_exc()
        logging.error(f"Error generating ideas: {str(e)}")
        logging.error(f"Traceback: {error_traceback}")
        raise HTTPException(status_code=500, detail=f"Error generating ideas: {str(e)}\n{error_traceback}")

@app.post("/validate-idea", response_model=ValidationResponse)
async def validate_idea(request: ValidationRequest):
    """Validate a startup idea with comprehensive analysis."""
    try:
        logging.debug(f"Received idea validation request: {request.dict()}")
        
        if not request.idea:
            logging.warning("Empty idea received in validation request")
            raise HTTPException(status_code=400, detail="Idea is required")
            
        # Initialize language model
        logging.debug("Initializing language model")
        llm = create_llm()
        logging.debug("Language model initialized successfully")
        
        # Create and run crew
        logging.debug("Creating idea validation crew")
        crew = create_idea_validation_crew(
            llm=llm,
            idea=request.idea
        )
        logging.debug("Crew created successfully, starting kickoff")
        
        results = crew.kickoff()
        logging.debug(f"Crew kickoff completed with result type: {type(results)}")
        logging.debug(f"Raw results: {results}")
        
        # Handle CrewOutput object if necessary
        if hasattr(results, 'raw_output'):
            logging.debug("Processing CrewOutput object")
            # If it's a CrewOutput object, try to get the raw output
            results_data = results.raw_output
            logging.debug(f"Extracted raw_output with type: {type(results_data)}")
        else:
            results_data = results
        
        # Parse results based on the data type
        if isinstance(results_data, dict):
            logging.debug("Processing results as dictionary")
            market_analysis = results_data.get("market_analysis", "Market analysis not available")
            technical_evaluation = results_data.get("technical_evaluation", "Technical evaluation not available")
            business_plan = results_data.get("business_plan", "Business plan not available")
        elif isinstance(results_data, list) and len(results_data) >= 3:
            logging.debug("Processing results as list")
            market_analysis = results_data[0]
            technical_evaluation = results_data[1]
            business_plan = results_data[2]
        elif isinstance(results_data, str):
            logging.debug("Processing results as string")
            # Try to extract sections if results is a single string
            market_analysis = "Market analysis not available"
            technical_evaluation = "Technical evaluation not available"
            business_plan = "Business plan not available"
            
            if "Market Analysis" in results_data:
                market_analysis = results_data.split("Market Analysis")[1].split("Technical Evaluation")[0].strip()
            if "Technical Evaluation" in results_data:
                technical_evaluation = results_data.split("Technical Evaluation")[1].split("Business Plan")[0].strip()
            if "Business Plan" in results_data:
                business_plan = results_data.split("Business Plan")[1].strip()
        else:
            logging.debug(f"Results not in expected format, type: {type(results_data)}")
            # Try to convert to string and extract information
            results_str = str(results_data)
            market_analysis = "Market analysis not available"
            technical_evaluation = "Technical evaluation not available"
            business_plan = "Business plan not available"
        
        logging.debug("Returning validation response")
        return ValidationResponse(
            market_analysis=market_analysis,
            technical_evaluation=technical_evaluation,
            business_plan=business_plan
        )
        
    except Exception as e:
        error_traceback = traceback.format_exc()
        logging.error(f"Error validating idea: {str(e)}")
        logging.error(f"Traceback: {error_traceback}")
        raise HTTPException(status_code=500, detail=f"Error validating idea: {str(e)}\n{error_traceback}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
