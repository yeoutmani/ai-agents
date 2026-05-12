import asyncio

from dotenv import load_dotenv
from agents import Agent, Runner


load_dotenv()


agent = Agent(
    name="Coach Python",
    instructions=(
        "Tu aides un debutant a apprendre Python et les agents IA. "
        "Explique simplement, donne des exemples courts, et pose une petite question a la fin."
    ),
)


async def main() -> None:
    question = "Explique-moi ce qu'est un agent IA en Python."
    result = await Runner.run(agent, question)
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
