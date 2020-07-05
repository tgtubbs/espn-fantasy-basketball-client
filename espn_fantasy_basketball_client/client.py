from session import Session
from typing import Dict


class Client:

    def __init__(self, username: str, password: str, league_id: int):
        self.base_url = "https://fantasy.espn.com/apis/v3/games/fba"
        self.session = Session()
        self.session.authenticate(username=username, password=password)
        self.league_id = league_id

    @staticmethod
    def _inspect_response(response):
        if response.status_code == 200:
            return
        else:
            raise Exception(f"Request failed with status {response.status}")
    
    def get_nba_team_schedules(self, season: int) -> Dict:
        url = f"{self.base_url}/seasons/{season}"
        params = {"view": ["proTeamSchedules_wl"]}
        response = self.session.get(url=url, params=params)
        self._inspect_response(response)
        return response.json()["settings"]["proTeams"]

    def get_league_history(self):
        url = f"{self.base_url}/leagueHistory/{self.league_id}"
        params = {"view": ["kona_history_standings"]}
        response = self.session.get(url=url, params=params)
        self._inspect_response(response)
        return response.json()
