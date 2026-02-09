from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Player:
    name: str
    position: str
    skill: int


@dataclass(slots=True)
class Manager:
    name: str
    tactic: str = "balanced"


@dataclass(slots=True)
class Team:
    name: str
    manager: Manager
    players: list[Player] = field(default_factory=list)

    @property
    def rating(self) -> float:
        if not self.players:
            return 0.0
        total = sum(player.skill for player in self.players)
        return total / len(self.players)

    def add_player(self, player: Player) -> None:
        self.players.append(player)
