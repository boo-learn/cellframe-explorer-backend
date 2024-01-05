class Colors:
    CEND = '\33[0m'
    CBOLD = '\33[1m'
    CITALIC = '\33[3m'
    CURL = '\33[4m'
    CBLINK = '\33[5m'
    CBLINK2 = '\33[6m'
    CSELECTED = '\33[7m'

    CBLACK = '\33[30m'
    CRED = '\33[31m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE = '\33[36m'
    CWHITE = '\33[37m'

    CBLACKBG = '\33[40m'
    CREDBG = '\33[41m'
    CGREENBG = '\33[42m'
    CYELLOWBG = '\33[43m'
    CBLUEBG = '\33[44m'
    CVIOLETBG = '\33[45m'
    CBEIGEBG = '\33[46m'
    CWHITEBG = '\33[47m'

    CGREY = '\33[90m'
    CRED2 = '\33[91m'
    CGREEN2 = '\33[92m'
    CYELLOW2 = '\33[93m'
    CBLUE2 = '\33[94m'
    CVIOLET2 = '\33[95m'
    CBEIGE2 = '\33[96m'
    CWHITE2 = '\33[97m'

    CGREYBG = '\33[100m'
    CREDBG2 = '\33[101m'
    CGREENBG2 = '\33[102m'
    CYELLOWBG2 = '\33[103m'
    CBLUEBG2 = '\33[104m'
    CVIOLETBG2 = '\33[105m'
    CBEIGEBG2 = '\33[106m'
    CWHITEBG2 = '\33[107m'


class logIt:
    @staticmethod
    def debug(message: str, name_plugin: str = "", /):
        """
        Log a message with the DEBUG level.
        """
        print(f"{Colors.CBLUE2} {message} {Colors.CEND}")

    @staticmethod
    def info(message: str, name_plugin: str = "", /):
        """
        Log a message with the INFO level.
        """
        print(f"{Colors.CBLUE2} {message} {Colors.CEND}")

    @staticmethod
    def notice(message: str, name_plugin: str = "", /):
        """
        Log a message with the NOTICE level.
        """
        print(f"{Colors.CBLUE2} {message} {Colors.CEND}")

    @staticmethod
    def message(message: str, name_plugin: str = "", /):
        """
        Log a message with the MESSAGE level.
        """
        print(f"{Colors.CYELLOW2} {message} {Colors.CEND}")

    @staticmethod
    def dap(message: str, name_plugin: str = "", /):
        """
        Log a message with the DAP level.
        """
        print(f"{Colors.CBLUE2} {message} {Colors.CEND}")

    @staticmethod
    def warning(message: str, name_plugin: str = "", /):
        """
        Log a message with the WARNING level.
        """
        print(f"{Colors.CBLUE2} {message} {Colors.CEND}")

    @staticmethod
    def att(message: str, name_plugin: str = "", /):
        """
        Log a message with the ATT level.
        """
        print(f"{Colors.CBLUE2} {message} {Colors.CEND}")

    @staticmethod
    def error(message: str, name_plugin: str = "", /):
        """
        Log a message with the ERROR level.
        """
        print(f"{Colors.CRED2} {message} {Colors.CEND}")

    @staticmethod
    def critical(message: str, name_plugin: str = "", /):
        """
        Log a message with the CRITICAL level.
        """
        print(f"{Colors.CREDBG} {message} {Colors.CEND}")
