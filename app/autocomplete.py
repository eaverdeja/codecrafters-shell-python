# https://docs.python.org/3/library/readline.html
# https://pymotw.com/3/readline/index.html
import readline

from app.handlers import builtins
from app.utils import list_executables


class Autocompleter:
    def __init__(self):
        # https://stackoverflow.com/questions/7124035/in-python-shell-b-letter-does-not-work-what-the
        if "libedit" in readline.__doc__:
            # MacOS binding syntax
            readline.parse_and_bind("bind ^I rl_complete")
        else:
            # Default binding syntax
            readline.parse_and_bind("tab: complete")

        readline.set_completer(self.complete)
        self.matches = []

        commands = list(builtins.keys()) + list_executables()
        # Sort commands by length - break ties with alphabetical order
        self.commands = sorted(set(commands), key=lambda x: (len(x), x))

    def complete(self, text, state):
        current_word = text.split(" ")[-1]
        if state == 0:
            if current_word:
                self.matches = [
                    command + " "
                    for command in self.commands
                    if command.startswith(current_word)
                ]

        try:
            value = self.matches[state]
            self.matches = []
            return value
        except IndexError:
            return None
