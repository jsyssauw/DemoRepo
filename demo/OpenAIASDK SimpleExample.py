# The imports
from dotenv import load_dotenv
from agents import Agent, Runner

# The usual starting point
load_dotenv(override=True)

# Make an agent with name, instructions, model
# instructions = systems prompt
v_system_prompt = "You are a brilliant, 6th grade math tutor. You are given a math problem and you need to solve it."
agent_math = Agent(name="Math Tutor", 
            instructions=v_system_prompt, 
            model="gpt-4o-mini")

print("The Agent objects is: ", agent_math, "\n\n")

v_user_prompt = "What does a function mean? Explain in 1 paragraph"
## Runner.run_sync(...) is a blocking (synchronous) call.  --> no asyncio or wait needed
result = Runner.run_sync(agent_math, v_user_prompt)
print(result.final_output)