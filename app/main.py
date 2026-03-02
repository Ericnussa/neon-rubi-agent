from app.agent import AssistantAgent


def main():
    agent = AssistantAgent()
    print("Neon Rubi Agent (MVP) — type 'exit' to quit")

    while True:
        user_input = input("you> ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("agent> See you soon ✨")
            break

        reply = agent.respond(user_input)
        print(f"agent> {reply}")


if __name__ == "__main__":
    main()
