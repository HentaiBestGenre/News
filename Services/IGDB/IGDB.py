from exeptions import TooManyRequests
import requests
import json


class IGDB:    
    def __init__(self, client_id, secret_key, access_token=None) -> None:
        if access_token is None:
            access_token = self.create_access_token(secret_key, client_id)
        self.client_id = client_id
        self.secret_key = secret_key
        self.access_token = access_token

    def post(self, url: str, headers: dict, queue: dict, data: str):
        url = url + f"?" + "&".join([f"{i}={v}" for i, v in queue.items()])
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 429:
            raise TooManyRequests()
        elif response.status_code != 429:
            raise Exception(f"Error {response.status_code}\n{response.content}")
        return json.loads(response.content)
        
    def create_access_token(self, secret_key, client_id):
        url = f"https://id.twitch.tv/oauth2/token"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"
        }
        queue = {
            'client_secret': secret_key,
            'client_id': client_id,
            "grant_type": "client_credentials"
        }
        data = {}
        response = self.post(url, url, headers=headers, queue=queue, data=data)
        return response['access_token']
        
    def get_franchises(self, offset=0, limit=500):
        url = 'https://api.igdb.com/v4/franchises'
        headers = {
            'Client-ID': self.client_id, 
            'Authorization': f'Bearer {self.access_token}'
        }
        queue = {}
        data = f'''fields checksum,
            created_at,
            games.aggregated_rating, games.aggregated_rating_count, games.alternative_names.name, games.category, games.name,
            name,
            slug,
            updated_at,
            url;
            limit {limit};
            offset {offset};'''
        
        response = self.post(url, url, headers=headers, queue=queue, data=data)
        return response
        
    def __str__(self):
        return f"client_id: {self.client_id}\n\tsecret_key: {self.secret_key}\n\taccess_token: {self.access_token}"
    def __repr__(self):
        return f"client_id: {self.client_id}\nsecret_key: {self.secret_key}\naccess_token: {self.access_token}"
