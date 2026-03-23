import subprocess
import sys
import os
from llm import call_llm
import json
from validation import validate_response
from policy import is_dangerous

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
        "-O", "exit",
        host
    ])



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

            state["history"] = []

            MAX_STEPS = 5
            continue_agent = True

            while continue_agent:

                for step in range(MAX_STEPS):
                    print(f"\n--- Step {step + 1} ---")

                    parsed = None

                    for attempt in range(2):
                        llm_response = call_llm(state, user_input)

                        try:
                            candidate = json.loads(llm_response)

                            if validate_response(candidate):
                                parsed = candidate

                                print("\nAnalysis:")
                                print(parsed["analysis"])

                                print("\nPlan:")
                                for i, step_text in enumerate(parsed["plan"], start=1):
                                    print(f"{i}. {step_text}")

                                break

                        except json.JSONDecodeError:
                            print("Invalid JSON, retrying...")

                    if parsed is None:
                        print("LLM failed to produce valid output")
                        continue_agent = False
                        break

                    if parsed["done"]:
                        print("\n--- FINAL SUMMARY ---")
                        print(parsed["analysis"])

                        print("\n✅ Investigation complete")
                        continue_agent = False
                        break

                    cmd = parsed["next_command"]

                    print(f"\nProposed command: {cmd}")
                    print(f"Reason: {parsed['reason']}")
                    print(f"Confidence: {parsed['confidence']}")

                    approval = input("Run this command? (y/edit/n): ")

                    if approval == "n":
                        print("Stopping investigation")
                        continue_agent = False
                        break
                    elif approval == "edit":
                        cmd = input("Enter command: ")

                    if is_dangerous(cmd):
                        print("⚠️ Potentially dangerous command detected")
                        print(f"Command: {cmd}")
                        override = input("Run anyway? (y/n): ")
                        if override != "y":
                            print("Blocked dangerous command, stopping investigation")
                            continue_agent = False
                            break

                    output = run_ssh_command(host, cmd)

                    state["history"].append({
                        "command": cmd,
                        "output": output
                    })

                else:
                    print("\n⚠️ Investigation running for a while...")

                    summary_prompt = """
                    Summarise the investigation so far.

                    Include:
                    - key findings
                    - likely root cause
                    - recommended next steps
                    """

                    summary = call_llm(state, summary_prompt)

                    print("\n--- SUMMARY ---")
                    print(summary)

                    decision = input("\nContinue investigating based on current findings? (y/n): ")

                    if decision.lower() != "y":
                        continue_agent = False

    finally:
        print("Closing connection...")
        close_ssh_connection(host)


if __name__ == "__main__":
    main()