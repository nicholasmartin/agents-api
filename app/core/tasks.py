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
        description=f"""Conduct a thorough market analysis for the following startup idea: {idea}
            
            Your analysis should include:
            1. Market Size: Estimate the total addressable market (TAM) and serviceable addressable market (SAM)
            2. Target Customer: Detailed profile of the ideal customer
            3. Competitive Landscape: Identify key competitors and their strengths/weaknesses
            4. Market Trends: Current and emerging trends that could impact this business
            5. Entry Barriers: Challenges in entering this market
            6. Growth Potential: Projected market growth over the next 3-5 years
            
            Base your analysis on realistic market conditions and provide specific numbers and facts where possible.
        """,
        agent=agent,
        expected_output="A comprehensive market analysis report covering all requested components."
    )

def create_technical_evaluation_task(agent, idea):
    """Creates a task for technical evaluation."""
    return Task(
        description=f"""Evaluate the technical feasibility of implementing the following startup idea: {idea}
            
            Your evaluation should include:
            1. Technology Stack: Recommended technologies and frameworks
            2. Development Complexity: Assessment of technical complexity (low/medium/high)
            3. Resource Requirements: Team composition and expertise needed
            4. Timeline: Estimated development timeline for MVP and full product
            5. Technical Challenges: Potential hurdles and how to overcome them
            6. Scalability Considerations: How the solution can scale with growth
            7. Integration Requirements: Third-party services or APIs needed
            
            Be realistic about the technical requirements and challenges.
        """,
        agent=agent,
        expected_output="A detailed technical evaluation covering all requested components."
    )

def create_business_plan_task(agent, idea, market_analysis=None, tech_evaluation=None):
    """Creates a task for business planning."""
    context = ""
    if market_analysis:
        context += f"\n\nMarket Analysis Summary:\n{market_analysis}"
    if tech_evaluation:
        context += f"\n\nTechnical Feasibility Summary:\n{tech_evaluation}"
        
    return Task(
        description=f"""Develop a business plan outline for the following startup idea: {idea}
            {context}
            
            Your business plan should include:
            1. Revenue Model: How the business will generate income
            2. Pricing Strategy: Recommended pricing structure
            3. Go-to-Market Strategy: Initial launch and customer acquisition plan
            4. Financial Projections: Estimated costs, revenue, and break-even timeline
            5. Funding Requirements: Capital needed and potential funding sources
            6. Key Metrics: Important KPIs to track success
            7. Growth Strategy: Plan for scaling the business after initial traction
            
            Make sure the business plan is realistic and aligned with the nature of the product/service.
            Base your plan on the market analysis and technical evaluation provided.
        """,
        agent=agent,
        expected_output="A comprehensive business plan covering all requested components."
    )
