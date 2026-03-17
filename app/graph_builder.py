from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from typing import Annotated, TypedDict

from app.tools import rag_tool, calculator, summarize_document


llm = ChatOpenAI(model="gpt-4o-mini")

tools = [
    rag_tool,
    calculator,
    summarize_document
]

llm_with_tools = llm.bind_tools(tools)


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def gaurdrail_node(state: ChatState):
    
    messages = state["messages"]

    user_input = messages[-1].content.lower()
    # Basic rule to check for harmful content
    blocked_keywords = ["hack", "exploit", "bypass", "password", "malware"
                        "bomb", "attack", "terror"]       

    for word in blocked_keywords:
        if word in user_input:
            return {
                "messages": [
                    {
                        "role": "assistant",
                        "content": "❌ Request blocked due to security policy."
                    }
                ]
            }

def chat_node(state: ChatState):

    messages = state["messages"]

    response = llm_with_tools.invoke(messages)

    return {"messages":[response]}


tool_node = ToolNode(tools)


def build_graph():

    graph = StateGraph(ChatState)
    graph.add_node("gaurdrail_node", gaurdrail_node)    
    graph.add_node("chat_node", chat_node)
    graph.add_node("tools", tool_node)

    graph.add_edge(START, "gaurdrail_node")
    graph.add_edge("gaurdrail_node", "chat_node")   

    graph.add_conditional_edges(
        "chat_node",
        tools_condition
    )

    graph.add_edge("tools", "chat_node")

    chatbot = graph.compile()
    #chatbot.visualize("chatbot_graph.html") 
    return chatbot