from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from football_manager.models import Team


@dataclass(slots=True)
class MatchResult:
    home: Team
    away: Team
    home_goals: int
    away_goals: int

    @property
    def winner(self) -> Team | None:
        if self.home_goals > self.away_goals:
            return self.home
        if self.away_goals > self.home_goals:
            return self.away
        return None

    @property
    def is_draw(self) -> bool:
        return self.home_goals == self.away_goals


@dataclass(slots=True)
class MatchSimulator:
    rng_seed: int = 42

    def _roll_goals(self, rating: float, opponent_rating: float) -> int:
        base = max(0.2, rating / 20)
        defense_factor = max(0.1, opponent_rating / 25)
        expected = base / defense_factor
        # Deterministic-ish scoring curve using seed.
        return min(6, max(0, int(expected + self._random())))

    def _random(self) -> float:
        self.rng_seed = (1103515245 * self.rng_seed + 12345) % (2**31)
        return (self.rng_seed / (2**31)) * 1.8

    def simulate(self, home: Team, away: Team) -> MatchResult:
        home_goals = self._roll_goals(home.rating + 3, away.rating)
        away_goals = self._roll_goals(away.rating, home.rating)
        return MatchResult(home=home, away=away, home_goals=home_goals, away_goals=away_goals)


@dataclass(slots=True)
class StandingsEntry:
    team: Team
    played: int = 0
    wins: int = 0
    draws: int = 0
    losses: int = 0
    goals_for: int = 0
    goals_against: int = 0
    points: int = 0

    @property
    def goal_difference(self) -> int:
        return self.goals_for - self.goals_against


@dataclass(slots=True)
class League:
    teams: list[Team]
    simulator: MatchSimulator = field(default_factory=MatchSimulator)

    def _fixtures(self) -> Iterable[tuple[Team, Team]]:
        for i, home in enumerate(self.teams):
            for away in self.teams[i + 1 :]:
                yield home, away

    def play_season(self) -> list[StandingsEntry]:
        table = {team.name: StandingsEntry(team=team) for team in self.teams}
        for home, away in self._fixtures():
            result = self.simulator.simulate(home, away)
            self._apply_result(table[result.home.name], table[result.away.name], result)
        return sorted(
            table.values(),
            key=lambda entry: (entry.points, entry.goal_difference, entry.goals_for),
            reverse=True,
        )

    def _apply_result(
        self, home_entry: StandingsEntry, away_entry: StandingsEntry, result: MatchResult
    ) -> None:
        home_entry.played += 1
        away_entry.played += 1
        home_entry.goals_for += result.home_goals
        home_entry.goals_against += result.away_goals
        away_entry.goals_for += result.away_goals
        away_entry.goals_against += result.home_goals

        if result.is_draw:
            home_entry.draws += 1
            away_entry.draws += 1
            home_entry.points += 1
            away_entry.points += 1
        elif result.winner == result.home:
            home_entry.wins += 1
            home_entry.points += 3
            away_entry.losses += 1
        else:
            away_entry.wins += 1
            away_entry.points += 3
            home_entry.losses += 1
