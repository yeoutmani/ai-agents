import asyncio

from dotenv import load_dotenv
from agents import Agent, Runner


load_dotenv()


python_agent = Agent(
    name="Prof Python",
    handoff_description="Specialiste des questions Python.",
    instructions="Explique Python avec des exemples simples et progressifs.",
)

agent_ia = Agent(
    name="Prof Agents IA",
    handoff_description="Specialiste des concepts d'agents IA.",
    instructions="Explique les agents IA, les outils, la memoire et l'orchestration.",
)

triage_agent = Agent(
    name="Routeur",
    instructions="Choisis le meilleur specialiste pour repondre a la question.",
    handoffs=[python_agent, agent_ia],
)


async def main() -> None:
    question = "Quelle est la difference entre une fonction Python et un outil d'agent IA ?"
    result = await Runner.run(triage_agent, question)
    print(result.final_output)
    print(f"\nRepondu par: {result.last_agent.name}")


if __name__ == "__main__":
    asyncio.run(main())
