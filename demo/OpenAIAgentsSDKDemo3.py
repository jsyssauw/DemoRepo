# The imports
import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, trace, InputGuardrail, GuardrailFunctionOutput, \
    InputGuardrailTripwireTriggered

from pydantic import BaseModel
import os

# The usual starting point
load_dotenv(override=True)

class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
)

async def main():
    # result = await Runner.run(triage_agent, "Who was the first president of the united states?")
    # print(result.final_output)

    try:
        print("Attempting to run triage_agent with 'What is life?'...")
        result = await Runner.run(triage_agent, "Write an essay about 'What is life?'")
        print("Triage agent result:")
        print(result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print("\nInput was blocked by the homework guardrail.")
        if hasattr(e, 'output_info') and e.output_info:
            homework_details = e.output_info
            print(f"Guardrail decision: Is homework? {homework_details.is_homework}")
            print(f"Reasoning: {homework_details.reasoning}")
        else:
            print("No additional details provided by the guardrail exception.")


    # with trace(enabled=True):
    # agent = Agent(name="Healtht Assistant", 
    #               instructions="You are a helpful assistant that can answer questions about health and fitness.", 
    #               model="gpt-4o-mini")
    # result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
    # print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())

# Code within the code,
# Functions calling themselves,
# Infinite loop's dance.