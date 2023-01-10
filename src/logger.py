from colorama import just_fix_windows_console, Fore

import datetime


class SingletonLogger(object):
    __DEBUG__ = True
    __VERBOSE__ = True
    colour = ""
    severity_info = {
        "INFO": "[I]",
        "DEBUG": "[D]",
        "WARNING": "[W]",
        "ERROR": "[E]",
        "VERBOSE": "[V]"
    }

    def __new__(cls, verbose=False, debug=False):
        if not hasattr(cls, 'instance'):
            cls.__VERBOSE__ = verbose
            cls.__DEBUG__ = debug
            cls.instance = super(SingletonLogger, cls).__new__(cls)
        return cls.instance

    def log(self, message, severity="INFO"):
        """Log a message to the console.

           :param severity: The severity of the message.
           :param message: The message to log.
           """
        just_fix_windows_console()

        now = datetime.datetime.now()
        newMessage = f"[{str(now)}] {message}"

        if severity == 'DEBUG':
            if self.__DEBUG__:
                print(Fore.BLUE + f'{self.severity_info[severity]}: {newMessage}')
        elif severity == "VERBOSE":
            if self.__VERBOSE__:
                print(Fore.MAGENTA + f'{self.severity_info[severity]}: {newMessage}')
        elif severity == "WARNING":
            print(Fore.YELLOW + f'{self.severity_info[severity]}: {newMessage}')
        elif severity == "ERROR":
            print(Fore.RED + f'{self.severity_info[severity]}: {newMessage}')
        else:
            print(Fore.GREEN + f'{self.severity_info["INFO"]}: {newMessage}')