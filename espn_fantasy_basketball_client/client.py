import requests
from session import Session
from typing import Dict, List


class Client:

    def __init__(self, username: str, password: str, league_id: int):
        self.base_url = "https://fantasy.espn.com/apis/v3/games/fba"
        self.league_id = league_id
        self.season = season
        self.session = Session()
        self.session.authenticate(username=username, password=password)

    @staticmethod
    def _inspect_response(response):
        if response.status_code == 200:
            return
        else:
            raise Exception(f"Request failed with status {response.status}")
    
    def _get(self, url: str, params: dict = None, headers: dict = None) -> requests.models.Response:
        response = self.session.get(url=url, params=params, headers=headers)
        self._inspect_response(response)
        return response

    def get_nba_team_schedules(self) -> List[Dict]:
        url = f"{self.base_url}/seasons/{self.season}"
        params = {"view": "proTeamSchedules_wl"}
        response = self._get(url=url, params=params)
        return response.json()["settings"]["proTeams"]

    def get_league_history(self) -> List[Dict]:
        url = f"{self.base_url}/leagueHistory/{self.league_id}"
        params = {"view": "kona_history_standings"}
        response = self._get(url=url, params=params)
        return response.json()

    def get_league_status(self) -> Dict:
        url = f"{self.base_url}/seasons/{self.season}/segments/0/leagues/{self.league_id}"
        params = {"view": "mStatus"}
        response = self._get(url=url, params=params)
        return response.json()["status"]

    def get_members(self) -> List[Dict]:
        url = f"{self.base_url}/seasons/{self.season}/segments/0/leagues/{self.league_id}"
        response = self._get(url=url)
        return response.json()["members"]

    def get_matchup_scores(self) -> List[Dict]:
        url = f"{self.base_url}/seasons/{self.season}/segments/0/leagues/{self.league_id}"
        params = {"view": "mMatchupScore"}
        response = self._get(url=url, params=params)
        return response.json()["schedule"]
    
    def get_matchup_stats(self) -> List[Dict]:
        url = f"{self.base_url}/seasons/{self.season}/segments/0/leagues/{self.league_id}"
        params = {"view": "mScoreboard"}
        response = self._get(url=url, params=params)
        return response.json()["schedule"]
    
    def get_standings(self) -> List[Dict]:
        url = f"{self.base_url}/seasons/{self.season}/segments/0/leagues/{self.league_id}"
        params = {"view": "mScoreboard"}
        response = self._get(url=url, params=params)
        return response.json()["teams"]

    def get_league_settings(self) -> Dict:
        url = f"{self.base_url}/seasons/{self.season}/segments/0/leagues/{self.league_id}"
        params = {"view": "mSettings"}
        response = self._get(url=url, params=params)
        return response.json()["settings"]
    
    def get_teams(self) -> List[Dict]:
        url = f"{self.base_url}/seasons/{self.season}/segments/0/leagues/{self.league_id}"
        response = self._get(url=url)
        return response.json()["teams"]

    def get_team(self, team_id: int) -> Dict:
        url = f"{self.base_url}/seasons/{self.season}/segments/0/leagues/{self.league_id}"
        response = self._get(url=url, forTeamId=team_id)
        return response.json()["teams"][0]

    def get_team_roster(self, team_id: int) -> List[Dict]:
        url = f"{self.base_url}/seasons/{self.season}/segments/0/leagues/{self.league_id}"
        response = self._get(url=url, view="mRoster", forTeamId=team_id)
        return response.json()["teams"][0]["roster"]["entries"]
