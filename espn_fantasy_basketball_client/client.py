import requests
from session import Session
from typing import Dict, List, Union


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
    
    def _get(self, url: str, view: str = None) -> requests.models.Response:
        response = self.session.get(url=url, params={"view": view})
        self._inspect_response(response)
        return response

    def get_nba_team_schedules(self, season: int) -> Dict:
        url = f"{self.base_url}/seasons/{season}"
        response = self._get(url=url, view="proTeamSchedules_wl")
        return response.json()["settings"]["proTeams"]

    def get_league_history(self) -> Dict:
        url = f"{self.base_url}/leagueHistory/{self.league_id}"
        reponse = self._get(url=url, view="kona_history_standings")
        return response.json()
    
    def get_nba_players(self, season: int) -> Dict:
        url = f"{self.base_url}/seasons/{season}/players"
        reponse = self._get(url=url, view="players_wl")
        return response.json()

    def get_league_members(self, season: int) -> List[Dict]:
        url = f"{self.base_url}/seasons/{season}/segments/0/leagues/{self.league_id}"
        response = self._get(url=url)
        return response.json()["members"]

    def get_league_status(self, season: int) -> Dict:
        url = f"{self.base_url}/seasons/{season}/segments/0/leagues/{self.league_id}"
        response = self._get(url=url, view="mStatus")
        return response.json()

    def get_league_matchup_scores(self, season: int) -> List[Dict]:
        url = f"{self.base_url}/seasons/{season}/segments/0/leagues/{self.league_id}"
        response = self._get(url=url, view="mMatchupScore")
        return response.json()["schedule"]
    
    def get_league_matchup_stats(self, season: int) -> Dict:
        url = f"{self.base_url}/seasons/{season}/segments/0/leagues/{self.league_id}"
        response = self._get(url=url, view="mScoreboard")
        return response.json()["schedule"]