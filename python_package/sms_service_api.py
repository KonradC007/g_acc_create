import requests


class SmsServiceAPI(object):
    def __init__(self, API_key, lang):
        self. lang = lang
        self.url = f"https://sms-service-online.com/stubs/handler_api?api_key={API_key}"
        response = requests.get(self.url, params={"action": "getBalance", "lang": self.lang})
        print(f"The balance is {response.text} $")

    def get_service(self, **kwargs):
        kwargs["lang"] = self.lang
        response = requests.get(self.url, params=kwargs)

        return response.text
