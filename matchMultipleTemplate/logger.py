from colorama import just_fix_windows_console, Fore, Style
import time

import datetime

__DEBUG__ = True
__VERBOSE__ = True


class SingletonLogger(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonLogger, cls).__new__(cls)
        return cls.instance

    def log(self, message, severity):
        if severity == 'DEBUG':
            if __DEBUG__:
                print(f'{severity}: {message}')
        elif severity == "VERBOSE":
            if __VERBOSE__:
                print(f'{severity}: {message}')
        else:
            print(f'{severity}: {message}')


severity_info = {
    "INFO": "[I]",
    "DEBUG": "[D]",
    "WARNING": "[W]",
    "ERROR": "[E]",
    "VERBOSE": "[V]"
}


def log(message, severity="INFO"):
    """Log a message to the console.

    :param severity: The severity of the message.
    :param message: The message to log.
    """
    just_fix_windows_console()

    now = datetime.datetime.now()
    newMessage = f"[{str(now)}] {message}"

    if severity == 'DEBUG':
        if __DEBUG__:
            print(Fore.BLUE + f'{severity_info[severity]}: {newMessage}')
    elif severity == "VERBOSE":
        if __VERBOSE__:
            # print()
            print(Fore.MAGENTA + f'{severity_info[severity]}: {newMessage}')
            # print(Style.RESET_ALL)
    elif severity == "WARNING":
        print(Fore.YELLOW + f'{severity_info[severity]}: {newMessage}')
    elif severity == "ERROR":
        print(Fore.RED + f'{severity_info[severity]}: {newMessage}')
    else:
        print(Fore.GREEN + f'{severity_info["INFO"]}: {newMessage}')
