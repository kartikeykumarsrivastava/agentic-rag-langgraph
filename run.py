from app.main import ask_question

while True:

    q = input("\nAsk Question: ")

    if q.lower() == "exit":
        break

    response = ask_question(q)

    print("\nAnswer:", response)