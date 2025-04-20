from crewai import Agent

# Create a simple agent to test if CrewAI is working
agent = Agent(
    role="Tester",
    goal="Test if CrewAI is installed correctly",
    backstory="I am a test agent created to verify that CrewAI is installed correctly."
)

print("CrewAI is installed correctly!")
print(f"Agent created: {agent.role}")
