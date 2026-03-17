from langchain_core.tools import tool
from app.rag_pipeline import build_retriever

retriever = build_retriever()

@tool
def rag_tool(query: str):
    """Retrieve info from ML document."""

    docs = retriever.invoke(query)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return context


@tool
def calculator(expression: str):
    """Evaluate math expression."""

    try:
        return str(eval(expression))
    except:
        return "Invalid expression"


@tool
def summarize_document(query: str):
    """Summarize document sections."""

    docs = retriever.invoke(query)

    text = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return text[:1000]