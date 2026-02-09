from __future__ import annotations

from football_manager.engine import League
from football_manager.models import Manager, Player, Team


def _sample_team(name: str, manager_name: str, base_skill: int) -> Team:
    manager = Manager(name=manager_name)
    players = [
        Player(name=f"{name} Player {idx+1}", position="MID", skill=base_skill + idx % 5)
        for idx in range(11)
    ]
    return Team(name=name, manager=manager, players=players)


def _print_table(entries: list) -> None:
    print("Takım            O  G  B  M  A  Y  AV  P")
    for entry in entries:
        print(
            f"{entry.team.name:<15} {entry.played:>2} {entry.wins:>2} {entry.draws:>2} "
            f"{entry.losses:>2} {entry.goals_for:>2} {entry.goals_against:>2} "
            f"{entry.goal_difference:>3} {entry.points:>3}"
        )


def main() -> None:
    teams = [
        _sample_team("Istanbul", "Kaan", 70),
        _sample_team("Ankara", "Deniz", 68),
        _sample_team("Izmir", "Ece", 66),
        _sample_team("Bursa", "Mert", 64),
    ]
    league = League(teams=teams)
    standings = league.play_season()
    print("Sezon tamamlandı! Puan tablosu:")
    _print_table(standings)


if __name__ == "__main__":
    main()
