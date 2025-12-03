from app.agents.coding_agent.agent import CodingAgent
from app.core.config import get_settings

settings = get_settings()

def main():
    agent = CodingAgent()

    print(f"--- Agent Initialized (Working Dir: {settings.WORK_DIR}) ---")

    user_query = f"""
    Please do the following:
    1. Write a Python function that generates the first 10 Fibonacci numbers.
    2. Run the function to get the numbers.
    3. Save the result into a file named 'fibonacci.txt' in '{settings.WORK_DIR}'.
    """

    print("\nUser Query:", user_query)
    print("\n--- Execution Start ---")

    try:
        for message in agent.stream(user_query):
            sender = message.type.upper()
            content = message.content

            if not content and hasattr(message, 'tool_calls') and message.tool_calls:
                tool_names = [tc['name'] for tc in message.tool_calls]
                print(f"[{sender}]: Requesting Tools -> {tool_names}")
            else:
                print(f"[{sender}]: {content}")

            print("-" * 40)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
