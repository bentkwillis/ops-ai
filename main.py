import subprocess
import sys
import os

CONTROL_PATH = "/tmp/ops_ai_ssh_%h_%p_%r"

def open_ssh_connection(host: str):
    subprocess.run([
        "ssh",
        "-M",
        "-S", CONTROL_PATH,
        "-fnNT",
        host
    ])

def run_ssh_command(host: str, command: str):
    subprocess.run([
        "ssh",
        "-S", CONTROL_PATH,
        host,
        command
    ])
    
def close_ssh_connection(host:str):
    subprocess.run([
        "ssh",
        "-S", CONTROL_PATH,
        "-)", "exit",
        host
    ])

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <host>")
        sys.exit(1)

    host = sys.argv[1]

    print(f"Opening persistent connection to {host}...")
    open_ssh_connection(host)

    print(f"Connected to {host}")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("> ")

        if user_input.lower() in ["exit", "quit"]:
            break

        run_ssh_command(host, user_input)

    print("Closing connection...")
    close_ssh_connection(host)


if __name__ == "__main__":
    main()