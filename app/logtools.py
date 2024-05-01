import sys

def log_print(*args) -> None:
    """
    Print `args` to sys.stderr

    This is exactly equivalent to `print(*args, file=sys.stderr)`
    """
    print(*args, file=sys.stderr)
