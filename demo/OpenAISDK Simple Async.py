# The imports
from dotenv import load_dotenv 
from agents import Agent, Runner # Imports the Agent and Runner classes from your 'agents' module
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

# Print the created Agent object to the console to see its representation.
print("The Agent objects is: ", agent_math, "\n\n")

# Define an asynchronous function called 'main'.
# Asynchronous functions can perform operations concurrently, allowing other tasks to run while waiting for one to complete.
# async function is called a coroutine
async def main():
    # The 'await Runner.run(agent_math, v_user_prompt)' call is an asynchronous operation.
    # This means the program can do other things while waiting for the AI to respond.
    
    v_user_prompt = "What does a function mean? Explain in 1 paragraph"
    v_user_prompt2 = "What is Pythagoras' theorem?"
    
    # Call the 'run' method of the 'Runner' class.
    # This sends the user's prompt to the specified agent ('agent_math').
    # 'await' pauses the execution of 'main' until 'Runner.run' completes and returns a result.
    result = await Runner.run(agent_math, 
                              v_user_prompt2)
    
    # '.final_output' likely contains the complete text response from the AI.
    print(result.final_output, '\n\n')

    v_user_prompt3 = "Give a simple example."
    v_user_prompt4 = "When did he live?"
    result = await Runner.run(agent_math, 
                              v_user_prompt4)
    print(result.final_output)

# This is a standard Python construct.
# It checks if the script is being run directly (as opposed to being imported as a module into another script).
if __name__ == "__main__":
    # If the script is run directly, execute the 'main' asynchronous function.
    # 'asyncio.run()' is the entry point to run an async program.
    asyncio.run(main())
