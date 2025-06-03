# The imports
from dotenv import load_dotenv
from agents import Agent, Runner, trace 
from openai.types.responses import ResponseTextDeltaEvent
import os
import asyncio

# The usual starting point

load_dotenv(override=True)

# Make an agent with name, instructions, model
# instructions = systems prompt
agent_math = Agent(name="Math Tutor", 
            instructions="You are a brilliant math tutor. You are given a math problem and you need to solve it.", 
            model="gpt-4o-mini")

agent_english = Agent(name="English Tutor", 
            instructions="You are a linguistic and english tutor. You are given a linguistic and english question and you need to solve it.", 
            model="gpt-4o-mini")

# Define an async main function to run the agent operations
async def main():
    # Run the agent
    with trace("Different Tutors"):
        result = await Runner.run(agent_math, "What does a function mean?")
    # Print the result
        print("------------------------------------------------------------------------------")
        print("Math Tutor:")
        print(result.final_output)

        print("\n------------------------------------------------------------------------------")
        print("English Tutor:")
        result_streamed = Runner.run_streamed(agent_english, "What does a function mean?")
        async for event in result_streamed.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)
        print() # Add a newline after streaming is done
        # Print the result

if __name__ == "__main__":
    asyncio.run(main())
