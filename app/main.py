from langchain_core.messages import HumanMessage
from app.graph_builder import build_graph

chatbot = build_graph()

# ✅ persistent memory
session_state = {
    "messages": []
}

def ask_question(query):

    session_state["messages"].append(
        HumanMessage(content=query)
    )

    result = chatbot.invoke(session_state)

    session_state["messages"] = result["messages"]

    return result["messages"][-1].content