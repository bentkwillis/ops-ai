DANGEROUS_PATTERNS = [
    "rm ",
    "shutdown",
    "reboot",
    "mkfs",
    ":(){", # fork bomb
    "dd ",
    "> /dev/sd",
    "rm -rf",
    "rm -r",
    "unlink",
    "shred",
    "wipefs",
    "> /",          # truncating root paths
    "> /etc",
    "mv /",         # moving critical dirs
    "cp /dev/zero", # overwrite via copy
    "/dev/sd",
    "/dev/nvme",
    "/dev/mmcblk",
    "mkfs.",
    "fdisk",
    "parted",
    "mount ",
    "umount",
    "while true",
    "for (;;)",
    "yes >",
    ":|:",          # variant fork bomb
    "nohup",        # runaway background jobs
    "& &",          # crude parallel spam
    "sudo",
    "su ",
    "chmod 777",
    "chown",
    "passwd",
    "useradd",
    "userdel",
    "bash -c",
    "sh -c",
    "eval",
    "`",        # backticks
    "$(",       # subshell execution
    "|",        # piping into another command
    ";",        # command chaining
    "&&",
    "||",
    "poweroff",
    "halt",
    "init 0",
    "init 6",
    "systemctl",
    "service ",
    "kill ",
    "killall",
    "pkill",
]

def is_dangerous(command: str) -> bool:
    command_lower = command.lower()

    for pattern in DANGEROUS_PATTERNS:
        if pattern in command_lower:
            return True
        
    return False