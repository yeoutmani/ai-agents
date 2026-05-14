from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_tavily import TavilySearch
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
import path_config
from utils.ollama_longraph import model

_ = load_dotenv()

# Tavily tool
tool = TavilySearch(max_results=2)
memory = SqliteSaver.from_conn_string(":memory:")

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

class Agent:
    def __init__(self, model, tools, checkpointer, system=""):
        self.system = system
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_ollama)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges("llm", self.exists_action, {True: "action", False: END})
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile(checkpointer=checkpointer)
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def call_ollama(self, state: AgentState):
        message = state["messages"]
        if self.system:
            message = [SystemMessage(content=self.system)] + message
        message = self.model.invoke(message)
        return {"messages": [message]}

    def exists_action(self, state: AgentState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    def take_action(self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        print("Back to the model!")
        return {'messages': results}
    
prompt = """You are a smart research assistant. Use the search engine to look up information. \
You are allowed to make multiple calls (either together or in sequence). \
Only look up information when you are sure of what you want. \
If you need to look up some information before asking a follow up question, you are allowed to do that!
"""

# with SqliteSaver.from_conn_string(":memory:") as memory:
#     abot = Agent(model, [tool], system=prompt, checkpointer=memory)

#     messages = [HumanMessage(content="What is the weather in nador?")]
#     thread = {"configurable": {"thread_id": "1"}}

#     for event in abot.graph.stream({"messages": messages}, thread):
#         for v in event.values():
#             print(v['messages'])

#     messages = [HumanMessage(content="What about in oujda?")]
#     thread = {"configurable": {"thread_id": "1"}}
#     for event in abot.graph.stream({"messages": messages}, thread):
#         for v in event.values():
#             print(v)

## Streaming tokens
async def main():

    async with AsyncSqliteSaver.from_conn_string(":memory:") as memory:
        abot = Agent(model, [tool], system=prompt, checkpointer=memory)
        messages = [HumanMessage(content="What is the weather in Nador?")]
        
        thread = {"configurable": {"thread_id": "4"}}
        async for event in abot.graph.astream_events({"messages": messages}, thread, version="v1"):
            kind = event["event"]
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    # Empty content in the context of OpenAI means
                    # that the model is asking for a tool to be invoked.
                    # So we only print non-empty content
                    print(content, end="|")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
