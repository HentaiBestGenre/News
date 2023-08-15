from dataclasses import KW_ONLY
import requests



class APIWrap:
    def __init__(self, headers: str, queue_params: dict) -> None:
        self.queue_params = queue_params
        self.headers = headers 
    
    def set_queue(self, **kwargs):
        self.queue_params = kwargs
    
    def extend_queue(self, **kwargs):
        self.queue_params = {**self.queue_params, **kwargs}
    
    def set_headers(self, **kwargs):
        self.headers = kwargs
    
    def extend_headers(self, **kwargs):
        self.headers = {**self.headers, **kwargs}
    
    def _add_queue(self):
        return self.path + f"?" + "&".join([f"{i}={v}" for i, v in self.queue_params.items()])
    
    def get(self, url):
        return requests.get(self.add_queue(url), headers=self.headers)
    
    def post(self, url):
        return requests.post(self.add_queue(url), headers=self.headers)
