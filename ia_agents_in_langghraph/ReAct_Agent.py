import re
from dotenv import load_dotenv
import asyncio

import path_config
from utils.ollama_client import client

_ = load_dotenv()

response = client.chat(
    model="gpt-oss:20b-cloud",
    messages=[{"role": "user", "content": "Hello world"}]
)

class Agent:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        completion = client.chat(
                        model="gpt-oss:120b-cloud", 
                        options={
                            'temperature': 0.0,
                            "stop": ["PAUSE"]
                        },
                        messages=self.messages)
        result = completion["message"]["content"]

        if "PAUSE" in result:
            result = result.split("PAUSE")[0] + "PAUSE"

        return result
    
prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
Each Thought, Action, PAUSE, Observation and Answer must be on its own line.

At the end of the loop you output an Answer.
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

average_dog_weight:
e.g. average_dog_weight: Collie
returns average weight of a dog when given the breed

Example session:

Question: How much does a Bulldog weigh?
Thought: I should look the dogs weight using average_dog_weight
Action: average_dog_weight: Bulldog
PAUSE

You will be called again with this:

Observation: A Bulldog weights 51 lbs

You then output:

Answer: A bulldog weights 51 lbs
""".strip()

def calculate(what):
    return eval(what)

def average_dog_weight(name):
    name = name.strip()

    if name == "Scottish Terrier":
        return "Scottish Terriers average 20 lbs"

    elif name == "Border Collie":
        return "a Border Collies average weight is 37 lbs"

    elif name == "Toy Poodle":
        return "a toy poodles average weight is 7 lbs"

    else:
        return "An average dog weights 50 lbs"

known_actions = {
    "calculate": calculate,
    "average_dog_weight": average_dog_weight
}

# Regex qui détecte une ligne "Action", extrait le nom de l’action et son argument
action_re = re.compile(
    r'Action:\s*([a-zA-Z_]+):\s*(.*?)(?:PAUSE|$)',
    re.DOTALL
)  # python regular expression to selection action

def query(question, max_turns=5):
    agent = Agent(prompt)
    next_prompt = question
    turns = 0
    while turns < max_turns:
        turns += 1
        result = agent(next_prompt)
        print(f"Turn {turns} - Agent response:\n{result}\n")

        match = action_re.search(result)

        print(f"Detected actions: {match}")

        if match:
            action = match.group(1)
            action_input = match.group(2)
            print(f"Executing action: {action} with input: {action_input}")
            if action not in known_actions:
                raise ValueError(f"Unknown action: {action}")
            
            print(f"Running action {action} with input {action_input}")

            observation = known_actions[action](action_input)
            print(f"Observation: {observation}")
            next_prompt = "Observation: {}".format(observation)
        else:
            print("No action detected, assuming final answer.")
            return result

async def main() -> None:
    print("Starting agent...")
    question = "I have 2 dogs, a border collie and a scottish terrier. What is their combined weight"
    answer = query(question)
    print("Final answer:", answer)
    # abot = Agent(prompt)
    # result = abot("How much does a toy poodle weigh?")
    # print(response["message"]["content"])
    # print("Answer:", result)
    # result = average_dog_weight("Toy Poodle")
    # print("Answer:", result)
    # next_prompt = "Observation: {}".format(result)
    # abot(next_prompt) 
    # print("Messages:", abot.messages)

    # abot = Agent(prompt)
    # question = """I have 2 dogs, a border collie and a scottish terrier. \
    #     What is their combined weight"""
    # result = abot(question)
    # print("Agent response:", result)
    # next_prompt = "Observation: {}".format(average_dog_weight("Border Collie"))
    # print(next_prompt)
    # result = abot(next_prompt)
    # print("Agent response:", result)

    # next_prompt = "Observation: {}".format(eval("37 + 20"))
    # print(next_prompt)
    # result = abot(next_prompt)
    # print("Agent response:", result)



if __name__ == "__main__":
    asyncio.run(main())

