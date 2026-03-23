import subprocess
import sys
import os
from llm import call_llm
import json
from validation import validate_response

CONTROL_PATH = "/tmp/ops_ai_ssh_%h_%p_%r"

state = {
    "history": []
}

def open_ssh_connection(host: str):
    subprocess.run([
        "ssh",
        "-M",
        "-S", CONTROL_PATH,
        "-fnNT",
        host
    ])

def run_ssh_command(host: str, command: str) -> str:
    try:
        result = subprocess.run(
            ["ssh", "-S", CONTROL_PATH, host, command],
            capture_output=True,
            text=True
        )

        output = result.stdout + result.stderr

        # print for user
        print(output)

        return output

    except Exception as e:
        error = f"[ERROR] {str(e)}"
        print(error)
        return error
    
def close_ssh_connection(host:str):
    subprocess.run([
        "ssh",
        "-S", CONTROL_PATH,
        "-)", "exit",
        host
    ])

def validate_response(data):
    if not isinstance(data, dict):
        return False

    required_fields = ["analysis", "next_command", "reason", "confidence"]

    for field in required_fields:
        if field not in data:
            return False

    if not isinstance(data["next_command"], str):
        return False

    if not isinstance(data["confidence"], (int, float)):
        return False

    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <host>")
        sys.exit(1)

    host = sys.argv[1]

    print(f"Opening connection to {host}...")
    open_ssh_connection(host)

    try:
        while True:
            user_input = input("> ")

            if user_input.lower() in ["exit", "quit"]:
                break

            parsed = None

            for attempt in range(2):
                llm_response = call_llm(state, user_input)

                print("\nLLM RESPONSE:")
                print(llm_response)

                try:
                    candidate = json.loads(llm_response)

                    if validate_response(candidate):
                        parsed = candidate
                        break

                except json.JSONDecodeError:
                    print("Invalid JSON, retrying...")

            if parsed is None:
                print("LLM failed to produce valid output")
                continue

            cmd = parsed["next_command"]

            print(f"\nProposed command: {cmd}")
            approval = input("Run this command? (y/edit/n): ")

            if approval == "n":
                continue
            elif approval == "edit":
                cmd = input("Enter command: ")

            output = run_ssh_command(host, cmd)

            state["history"].append({
                "command": cmd,
                "output": output
            })

    finally:
        print("Closing connection...")
        close_ssh_connection(host)


if __name__ == "__main__":
    main()