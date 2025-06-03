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

async def main():
    # Instantiate the Runner.
    # The TypeError indicated that Runner() takes no arguments.
    # So, we create an instance of Runner without passing agent_math here.
    runner = Runner() 

    # The 'agent_math' will be passed to the 'run' method of the runner instance.
    v_user_prompt = "What does a function mean? Explain in 1 paragraph"
    v_user_prompt2 = "What is Pythagoras known for?"
    # Call the 'run' method on the 'runner' instance, passing both the agent and the prompt.
    result = await runner.run(starting_agent = agent_math,
                              input = v_user_prompt2,
                              context = None,
                              max_turns = 10,
                              hooks = None,
                              run_config = None,
                              previous_response_id = None
                             )
    print(result.final_output, '\n\n')

    # Similarly, for the second call, use the 'runner' instance.
    #even when using a instance of runner, the context of the previous interaction is not remembered.
    v_user_prompt4 = "When did he live?"
    result = await runner.run(agent_math, 
                              v_user_prompt4,)
    print(result.final_output)

# This is a standard Python construct.
# It checks if the script is being run directly (as opposed to being imported as a module into another script).
if __name__ == "__main__":
    # If the script is run directly, execute the 'main' asynchronous function.
    # 'asyncio.run()' is the entry point to run an async program.
    asyncio.run(main())
