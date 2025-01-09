import aiohttp
from common.settings import PROVERKACHEKA_TOKEN, PROVERKACHEKA_URL
import logging

logger = logging.getLogger(__name__)

async def get_cheque_from_api_service(qrraw: str):
    data = {
        "token": PROVERKACHEKA_TOKEN,
        "qrraw": qrraw,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(PROVERKACHEKA_URL, json=data) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_message = await response.text()
                logger.error(f"Error: {response.status}, Message: {error_message}")
                return None
