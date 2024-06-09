# state.py
from dataclasses import dataclass

class SelectedCoin:
    def __init__(self):
        self._coin = None

    @property
    def coin(self):
        return self._coin

    @coin.setter
    def coin(self, value):
        self._coin = value

@dataclass
class Completed:
    agents: int


# Create a single instance of State to be shared
selected_coin = SelectedCoin()
completed = Completed(agents=0)
