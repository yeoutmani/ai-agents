import re
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_tavily import TavilySearch
import path_config

from utils.ollama_longraph import model
from IPython.display import Image, display

_ = load_dotenv()

tool = TavilySearch(max_results=4) #increased number of results
print(type(tool))
print(tool.name)

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

class Agent:

    def __init__(self, model, tools, system=""):
        self.system = system
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_ollama)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END}
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile()
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def exists_action(self, state: AgentState):
        tool_calls = state["messages"][-1].tool_calls
        return len(tool_calls) > 0

    def call_ollama(self, state: AgentState):
        message = state["messages"]
        if self.system:
            message = [SystemMessage(content=self.system)] + message
        message = self.model.invoke(message)
        return {"messages": [message]}
    
    def take_action(self, state: AgentState):
        tool_calls = state["messages"][-1].tool_calls
        results = []
        for tool_call in tool_calls:
            print(f"calling {tool_call['name']} with args {tool_call['args']}")
            result= self.tools[tool_call['name']].invoke(tool_call['args'])
            results.append(ToolMessage(tool_call_id=tool_call['id'], name=tool_call['name'], content=str(result)))
        return {"messages": results}
    
prompt = """You are a smart research assistant. Use the search engine to look up information. \
You are allowed to make multiple calls (either together or in sequence). \
Only look up information when you are sure of what you want. \
If you need to look up some information before asking a follow up question, you are allowed to do that!
"""

abot = Agent(model, [tool], system=prompt)

print(abot.graph.get_graph().draw_mermaid())

png_data = abot.graph.get_graph().draw_mermaid_png()

with open("graph.png", "wb") as f:
    f.write(png_data)

print("Graph saved to graph.png")

messages = [HumanMessage(content="What is the weather in sf?")]
result = abot.graph.invoke({"messages": messages})

print("Graph after execution:", result['messages'][-1].content)

messages = [HumanMessage(content="What is the weather in SF and LA?")]
result = abot.graph.invoke({"messages": messages})

print("Graph after execution:", result['messages'][-1].content)

# Note, the query was modified to produce more consistent results. 
# Results may vary per run and over time as search information and models change.

query = "Who won the super bowl in 2024? In what state is the winning team headquarters located? \
What is the GDP of that state? Answer each question." 
messages = [HumanMessage(content=query)]


abot = Agent(model, [tool], system=prompt)
result = abot.graph.invoke({"messages": messages})
print("Graph after execution:", result['messages'][-1].content)