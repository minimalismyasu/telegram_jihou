from __future__ import annotations

import json
import os
from datetime import datetime
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


TOKYO = ZoneInfo("Asia/Tokyo")


def telegram_enabled() -> bool:
    return bool(os.getenv("TELEGRAM_BOT_TOKEN")) and bool(os.getenv("TELEGRAM_CHAT_ID"))


def send_telegram(message: str) -> None:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = json.dumps(
        {
            "chat_id": chat_id,
            "text": message,
            "disable_web_page_preview": True,
        }
    ).encode("utf-8")
    request = Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            response.read()
    except HTTPError as exc:
        if exc.code == 401:
            raise RuntimeError(
                "Telegram bot token is unauthorized. Check TELEGRAM_BOT_TOKEN."
            ) from exc
        raise


def build_message(now: datetime | None = None) -> str:
    current = now or datetime.now(TOKYO)
    return f"時報 {current.strftime('%Y-%m-%d %H:%M:%S')}"


def main() -> int:
    if not telegram_enabled():
        print("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.")
        return 1

    message = build_message()
    try:
        send_telegram(message)
    except RuntimeError as exc:
        print(str(exc))
        return 1

    print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
