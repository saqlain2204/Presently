class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_success(message):
    """Print a success message in green"""
    print(f"{Colors.GREEN}{message}{Colors.END}")

def print_info(message):
    """Print an info message in blue"""
    print(f"{Colors.BLUE}{message}{Colors.END}")

def print_warning(message):
    """Print a warning message in yellow"""
    print(f"{Colors.YELLOW}{message}{Colors.END}")

def print_error(message):
    """Print an error message in red"""
    print(f"{Colors.RED}{message}{Colors.END}")

def print_header(message):
    """Print a header in bold"""
    print(f"\n{Colors.BOLD}{message}{Colors.END}")

def print_progress(step, total, message="Processing"):
    """Print a progress message with step/total format"""
    print(f"{message}: {step}/{total}")
