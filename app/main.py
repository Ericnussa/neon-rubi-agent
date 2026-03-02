import argparse

from app.agent import AssistantAgent
from app.channels import run_discord, run_telegram


def main():
    parser = argparse.ArgumentParser(description="Neon Rubi Agent")
    parser.add_argument("--mode", choices=["cli", "telegram", "discord"], default="cli")
    args = parser.parse_args()

    agent = AssistantAgent()

    if args.mode == "telegram":
        run_telegram(agent)
        return

    if args.mode == "discord":
        run_discord(agent)
        return

    print("Neon Rubi Agent (MVP+) — type 'exit' to quit")
    while True:
        user_input = input("you> ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("agent> See you soon ✨")
            break
        reply = agent.respond(user_input)
        print(f"agent> {reply}")


if __name__ == "__main__":
    main()
