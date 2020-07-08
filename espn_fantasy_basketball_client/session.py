import os
import pickle
import requests 


class Session(requests.Session):

    def __init__(self, *args, **kwargs):
        super(Session, self).__init__(*args, **kwargs)
        self.api_key_url = "https://registerdisney.go.com/jgc/v5/client/ESPN-FANTASYLM-PROD/api-key?langPref=en-US"
        self.login_url = "https://ha.registerdisney.go.com/jgc/v5/client/ESPN-FANTASYLM-PROD/guest/login?langPref=en-US"
        self.headers.update({"ContentType": "application/json"})
    
    def authenticate(self, username: str, password: str):
        """
        1. Add API key to session headers
        2. If cookies from a previous session exist, load them.
        3. If cookies from a previous session don't exist or have expired,
           authenticate with usename and password, save cookies.
        """
        self._get_api_key()  # Adds api key to session headers
        if self._cookies_exist():
            self.cookies = self._load_cookies()
        else:
            response = self.post(url=self.login_url, json={"loginValue": username, "password": password}).json()
            requests.utils.add_dict_to_cookiejar(
                cj=self.cookies,
                cookie_dict={
                    "espn_s2": response["data"]["s2"], 
                    "swid": response["data"]["profile"]["swid"]
                }
            )
            self._save_cookies()

    def _get_api_key(self) -> None:
        response = self.post(url=self.api_key_url)
        self.headers.update({"authorization": f"APIKEY {response.headers['api-key']}"})

    def _save_cookies(self) -> None:
        with open("cookies.pkl", "wb") as file:
            pickle.dump(self.cookies, file)

    def _load_cookies(self) -> requests.cookies:
        with open("cookies.pkl", "rb") as file:
            return pickle.load(file)

    def _cookies_exist(self) -> bool:
        return os.path.exists("cookies.pkl")
