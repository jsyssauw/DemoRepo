# The imports
from dotenv import load_dotenv 
from agents import Agent, Runner, trace # Imports the Agent and Runner classes from your 'agents' module
import os 
import asyncio # Used for writing concurrent code using the async/await syntax

# The usual starting point
load_dotenv(override=True) # 'override=True' means it will overwrite existing environment variables.

# Make an agent with name, instructions, model
# This is a system prompt that defines the role and behavior of the AI agent.
v_system_prompt = "You are a brilliant, 6th grade math tutor. You are given a math problem and you need to solve it."

# Create an instance of the Agent class.
# 'name' is a descriptive name for the agent.
# 'instructions' provides the system prompt to guide the agent's behavior.
# 'model' specifies which OpenAI model to use (e.g., "gpt-4o-mini").
agent_math = Agent(name="Math Tutor", 
            instructions=v_system_prompt, 
            model="gpt-4o-mini")
# Define an async function to run the agent
async def main():
    # This is the user's math problem that the agent will solve.
    v_user_prompt2 = "I have 5 apples and I eat 2. How many apples do I have left?"
    v_user_prompt3 = "What is the square root of 16?"
    with trace("Beloved Math Tutor"):
        result = await Runner.run(starting_agent = agent_math,
                            input = v_user_prompt2,
                            context = None,
                            max_turns = 10,
                            hooks = None,
                            run_config = None,
                            previous_response_id = None
                            )
        print(result.final_output, '\n\n')

        result = await Runner.run(starting_agent = agent_math,
                            input = v_user_prompt2,
                            context = None,
                            max_turns = 10,
                            hooks = None,
                            run_config = None,
                            previous_response_id = None
                            )
        print(result.final_output, '\n\n')

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())
