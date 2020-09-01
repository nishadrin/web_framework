

class Category:
    """docstring for Category."""

    @property
    def name(self) -> str:
        return self.__name

    def set_name(self, name: str):
        self.__name = name
