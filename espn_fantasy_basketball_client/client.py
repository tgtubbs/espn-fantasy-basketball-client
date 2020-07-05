from session import Session


class Client:

    def __init__(self, username: str, password: str):
        self.base_url = "https://fantasy.espn.com/apis/v3/games/fba"
        self.session = Session()
        self.session.authenticate(username=username, password=password)