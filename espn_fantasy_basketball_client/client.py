import requests
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
    
    def _get(self, url: str, **kwargs) -> requests.models.Response:
        response = self.session.get(url=url, params=kwargs)
        self._inspect_response(response)
        return response

    def get_nba_team_schedules(self, season: int) -> List[Dict]:
        url = f"{self.base_url}/seasons/{season}"
        response = self._get(url=url, view="proTeamSchedules_wl")
        return response.json()["settings"]["proTeams"]

    def get_league_history(self) -> List[Dict]:
        url = f"{self.base_url}/leagueHistory/{self.league_id}"
        response = self._get(url=url, view="kona_history_standings")
        return response.json()

    def get_league_members(self, season: int) -> List[Dict]:
        url = f"{self.base_url}/seasons/{season}/segments/0/leagues/{self.league_id}"
        response = self._get(url=url)
        return response.json()["members"]

    def get_league_status(self, season: int) -> Dict:
        url = f"{self.base_url}/seasons/{season}/segments/0/leagues/{self.league_id}"
        response = self._get(url=url, view="mStatus")
        return response.json()["status"]

    def get_league_matchup_scores(self, season: int) -> List[Dict]:
        url = f"{self.base_url}/seasons/{season}/segments/0/leagues/{self.league_id}"
        response = self._get(url=url, view="mMatchupScore")
        return response.json()["schedule"]
    
    def get_league_matchup_stats(self, season: int) -> List[Dict]:
        url = f"{self.base_url}/seasons/{season}/segments/0/leagues/{self.league_id}"
        response = self._get(url=url, view="mScoreboard")
        return response.json()["schedule"]
    
    def get_league_standings(self, season: int) -> List[Dict]:
        url = f"{self.base_url}/seasons/{season}/segments/0/leagues/{self.league_id}"
        response = self._get(url=url, view="mScoreboard")
        return response.json()["teams"]

    def get_league_settings(self, season: int) -> Dict:
        url = f"{self.base_url}/seasons/{season}/segments/0/leagues/{self.league_id}"
        response = self._get(url=url, view="mSettings")
        return response.json()["settings"]

    def get_league_players(self, season: int) -> List[Dict]:
        url = f"{self.base_url}/seasons/{season}/segments/0/leagues/{self.league_id}"
        response = self._get(url=url, view="kona_player_info")
        return response.json()["players"]
    
    def get_team_roster(self, season: int, team_id: int) -> List[Dict]:
        url = f"{self.base_url}/seasons/{season}/segments/0/leagues/{self.league_id}"
        response = self._get(url=url, view="mRoster", forTeamId=team_id)
        return response.json()["teams"][0]["roster"]["entries"]
