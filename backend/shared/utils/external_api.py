import requests
from loguru import logger
from shared.core import config


class ExternalApi:
    async def connection_to_afiliasi(self, url_api, method: str):
        try:
            url = config.AFILIASI_BASE_URL + url_api
            headers = {
                "Accept": "application/json",
                "Authorization": config.AFILIASI_API_KEY,
            }

            match method:
                case "get":
                    response = requests.get(url, headers=headers)
                    return response.json()

        except Exception as e:
            raise e
