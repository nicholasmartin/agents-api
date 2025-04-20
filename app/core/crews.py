from crewai import Crew
from .agents import (
    create_mvp_idea_specialist,
    create_market_researcher,
    create_technical_evaluator,
    create_business_strategist
)
from .tasks import (
    create_idea_generation_task,
    create_market_analysis_task,
    create_technical_evaluation_task,
    create_business_plan_task
)

def create_idea_generation_crew(llm, constraints=None, industry=None, technology_focus=None):
    """Creates a crew for generating startup ideas."""
    # Create agent
    idea_generator = create_mvp_idea_specialist(llm)
    
    # Create task
    idea_task = create_idea_generation_task(
        agent=idea_generator,
        constraints=constraints,
        industry=industry,
        technology_focus=technology_focus
    )
    
    # Create crew
    crew = Crew(
        agents=[idea_generator],
        tasks=[idea_task],
        verbose=False
    )
    
    return crew

def create_idea_validation_crew(llm, idea):
    """Creates a crew for validating startup ideas."""
    # Create agents
    market_researcher = create_market_researcher(llm)
    tech_evaluator = create_technical_evaluator(llm)
    business_strategist = create_business_strategist(llm)
    
    # Create market and tech tasks
    market_task = create_market_analysis_task(
        agent=market_researcher,
        idea=idea
    )
    
    tech_task = create_technical_evaluation_task(
        agent=tech_evaluator,
        idea=idea
    )
    
    # Create first crew for market and tech analysis
    first_crew = Crew(
        agents=[market_researcher, tech_evaluator],
        tasks=[market_task, tech_task],
        verbose=False
    )
    
    # Get results from first tasks
    results = first_crew.kickoff()
    market_analysis = results[0]  # Result from market_task
    tech_evaluation = results[1]  # Result from tech_task
    
    # Create business plan task that depends on previous results
    business_task = create_business_plan_task(
        agent=business_strategist, 
        idea=idea,
        market_analysis=market_analysis,
        tech_evaluation=tech_evaluation
    )
    
    # Create final crew with business task
    final_crew = Crew(
        agents=[business_strategist],
        tasks=[business_task],
        verbose=False
    )
    
    final_result = final_crew.kickoff()
    
    # Return all results
    return {
        "market_analysis": market_analysis,
        "technical_evaluation": tech_evaluation,
        "business_plan": final_result
    }
