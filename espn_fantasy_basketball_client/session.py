import requests
import yaml


class Session(requests.Session):

    def __init__(self, *args, **kwargs):
        super(Session, self).__init__(*args, **kwargs)
        self.api_key_url = "https://registerdisney.go.com/jgc/v5/client/ESPN-FANTASYLM-PROD/api-key?langPref=en-US"
        self.login_url = "https://ha.registerdisney.go.com/jgc/v5/client/ESPN-FANTASYLM-PROD/guest/login?langPref=en-US"
        self.headers.update({"ContentType": "application/json"})
    
    def authenticate(self, username: str, password: str):
        '''
        Authenticate using username and password
        Add cookies to session
        '''
        self._get_api_key()  # Adds api key to session headers
        response = self.post(url=self.login_url, json={"loginValue": username, "password": password}).json()
        requests.utils.add_dict_to_cookiejar(
            cj=self.cookies,
            cookie_dict={
                "espn_s2": response["data"]["s2"], 
                "swid": response["data"]["profile"]["swid"]
            }
        )
    
    def _get_api_key(self):
        '''
        Add API key to session headers
        '''
        response = self.post(url=self.api_key_url)
        self.headers.update({"authorization": f"APIKEY {response.headers['api-key']}"})