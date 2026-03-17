from langchain_core.messages import HumanMessage
from app.graph_builder import build_graph

chatbot = build_graph()

def ask_question(query):

    result = chatbot.invoke({
        "messages":[HumanMessage(content=query)]
    })

    return result["messages"][-1].content