import asyncio
from datetime import date

from dotenv import load_dotenv
from agents import Agent, Runner, function_tool


load_dotenv()


@function_tool
def date_du_jour() -> str:
    """Retourne la date du jour."""
    return date.today().isoformat()


agent = Agent(
    name="Assistant organise",
    instructions=(
        "Tu aides l'utilisateur a organiser son apprentissage. "
        "Utilise l'outil date_du_jour si la date est utile."
    ),
    tools=[date_du_jour],
)


async def main() -> None:
    question = "Prepare-moi un petit plan d'apprentissage pour aujourd'hui."
    result = await Runner.run(agent, question)
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
