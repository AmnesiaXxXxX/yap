import os
import re
from typing import Callable, Generator, List

from dotenv import load_dotenv
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message

load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
PASSWORD = os.getenv("PASSWORD")

app = Client("yap", API_ID, API_HASH, password=PASSWORD)


def find_yap(text: str):
    """
    Uses the given regex pattern to find and return the matched text.

    Args:
        text (str): The input text to process.

    Returns:
        str: The matched text if found; otherwise, an empty string.
    """
    pattern = r"((.+)|(?=.))([юя]\s+п)"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        result = match.group().strip()
        return result if result != text else ""
    return ""


def find_amnesia(text: str):
    pattern = r"((.+)|(?=.))(а\s+мне)"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        result = match.group(0).strip() + " зия"

        return result if result != text else ""
    return ""


def find_shutka(text: str) -> str:
    shutki = {"я тоже": "на говно похоже"}
    if text in shutki.keys():
        return shutki[text.lower().strip()]
    return ""


def process_text(text: str) -> Generator[str, None, None]:
    """
    Processes the input text using available functions and yields the result if non-empty.

    Args:
        text (str): The input text to process.

    Yields:
        str: The processed text.
    """
    functions: List[Callable[[str], str]] = [find_amnesia, find_yap, find_shutka]
    for func in functions:
        result = func(text)
        if result:
            yield result


@app.on_message(~(filters.channel | filters.bot))  # type: ignore
async def me(_: Client, message: Message) -> None:
    for result in process_text(message.content):
        if result:
            await message.reply(result, reply_to_message_id=message.id)
    if "сосал?" in message.content.lower():
        await message.reply("ДА!", reply_to_message_id=message.id, quote=True, quote_text="сосал?")

@app.on_message_reaction_updated()  # type: ignore
async def reactions(_: Client, message: Message) -> None:
    # Логируем ID сообщения и его текст
    print("Обновлены реакции для сообщения с ID:", message.id)
    print("Содержимое сообщения:", message.text)

if __name__ == "__main__":
    app.run()
