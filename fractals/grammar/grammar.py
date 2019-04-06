import itertools


class Grammar:
    """Apply production rules to strings."""

    def __init__(self, productions):
        """Initialize a Grammar with the given production rules.

        :param productions: The production rules for the Grammar.
        :type productions: dict
        """
        self.productions = productions
        self.symbols = frozenset(filter(str.isalpha, productions.keys()))

    def __check_text_symbols(self, text):
        """Ensure the given text contains only known symbols."""
        for symbol in filter(str.isalpha, text):
            if symbol not in self.symbols:
                raise ValueError("Unknown symbol '{}'".format(symbol))

    @staticmethod
    def _apply_symbol(args):
        symbol, rules = args
        return rules.get(symbol, symbol)

    def apply(self, text):
        """Apply the production rules to the given text."""
        # self.__check_text_symbols(text)

        # Use a chunk size for efficiency with smaller text.
        return "".join(
            map(
                self._apply_symbol, zip(text, itertools.repeat(self.productions))
            )
        )

    def iapply(self, axiom):
        """Return an infinite iterator to apply the production rules to the given axiom."""
        while True:
            axiom = self.apply(axiom)
            yield axiom
