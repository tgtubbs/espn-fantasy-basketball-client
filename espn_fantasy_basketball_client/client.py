from session import Session
from typing import Dict, List


class Client:

    def __init__(self, username: str, password: str, league_id: int):
        self.base_url = "https://fantasy.espn.com/apis/v3/games/fba"
        self.league_id = league_id
        self.session = Session()
        self.session.authenticate(username=username, password=password)

    @staticmethod
    def _inspect_response(response):
        if response.status_code == 200:
            return
        else:
            raise Exception(f"Request failed with status {response.status}")
    
    def get_nba_team_schedules(self, season: int) -> Dict:
        url = f"{self.base_url}/seasons/{season}"
        params = {"view": "proTeamSchedules_wl"}
        response = self.session.get(url=url, params=params)
        self._inspect_response(response)
        return response.json()["settings"]["proTeams"]

    def get_league_history(self) -> Dict:
        url = f"{self.base_url}/leagueHistory/{self.league_id}"
        params = {"view": "kona_history_standings"}
        response = self.session.get(url=url, params=params)
        self._inspect_response(response)
        return response.json()
    
    def get_nba_players(self, season: int) -> Dict:
        url = f"{self.base_url}/seasons/{season}/players"
        params = {"view": "players_wl"}
        response = self.session.get(url=url, params=params)
        self._inspect_response(response)
        return response.json()

    def get_league_members(self, season: int) -> List[Dict]:
        url = f"{self.base_url}/seasons/{season}/segments/0/leagues/{self.league_id}"
        response = self.session.get(url=url)
        self._inspect_response(response)
        return response.json()["members"]
