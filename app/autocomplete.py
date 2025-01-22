# https://docs.python.org/3/library/readline.html
# https://pymotw.com/3/readline/index.html
import readline

import logging
from typing import TextIO

from app.handlers import builtins
from app.utils import list_executables


class Autocompleter:
    def __init__(self, out: TextIO, logger: logging.Logger):
        # https://stackoverflow.com/questions/7124035/in-python-shell-b-letter-does-not-work-what-the
        if "libedit" in readline.__doc__:
            # MacOS binding syntax
            readline.parse_and_bind("bind ^I rl_complete")
        else:
            # Default binding syntax
            readline.parse_and_bind("tab: complete")

        readline.set_completer(self.complete)

        self.out = out
        self.logger = logger
        self.matches = []

        commands = list(builtins.keys()) + list_executables()
        # Sort commands by length - break ties with alphabetical order
        self.commands = sorted(set(commands), key=lambda x: (len(x), x))

    def complete(self, text: str, state: int) -> str | None:
        self.logger.debug(f"Complete called with text='{text}', state={state}")

        if state == 0:
            self.matches = [
                command + " " for command in self.commands if command.startswith(text)
            ]
            if len(self.matches) > 1:
                lcp = self._get_longest_common_prefix(self.matches)
                # Do we have a longest common prefix that
                # is longer than the current text? If so, we want
                # to autocomplete to it
                if len(lcp) > len(text):
                    return lcp

                # Otherwise, we have multiple matches to display
                self.out.write(f"\n{' '.join(self.matches)}")
                # Redisplay the prompt
                self.out.write(f"\n$ {text}")
                # We don't want to autocomplete immediately
                # when displaying multiple matches
                return

        try:
            value = self.matches[state]
            # Reset matches after autocompleting
            self.matches = []
            self.logger.debug(f"Returning match: '{value}'")
            return value
        except IndexError:
            self.logger.debug("No more matches available")
            return None

    def _get_longest_common_prefix(self, strings: list[str]) -> str:
        if not strings:
            return ""

        # Use the shortest string as the reference
        reference = sorted(strings)[0]

        for i in range(len(reference)):
            prefix = reference[: i + 1]
            if all(s.startswith(prefix) for s in strings):
                # If all commands still start with the prefix, we can
                # keep iterating on the reference to get the longest prefix
                continue
            else:
                # Go back a step - that's our longest common prefix
                return reference[:i]

        return reference
