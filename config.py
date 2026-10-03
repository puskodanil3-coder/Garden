FILE_PATH = 'garden.db'
TABLE_WIDTH = 50

RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[96m"
RESET = "\033[0m"

def print_error(msg):
    print(f'{RED}{msg}{RESET}')


def print_success(msg):
    print(f'{GREEN}{msg}{RESET}')


def print_info(msg):
    print(f'{BLUE}{msg}{RESET}')
