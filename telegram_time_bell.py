from __future__ import annotations

import json
import os
from datetime import datetime
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
    with urlopen(request, timeout=30) as response:
        response.read()


def build_message(now: datetime | None = None) -> str:
    current = now or datetime.now(TOKYO)
    return f"時報 {current.strftime('%Y-%m-%d %H:%M:%S')}"


def main() -> int:
    if not telegram_enabled():
        print("TELEGRAM_BOT_TOKEN と TELEGRAM_CHAT_ID を設定してください")
        return 1

    message = build_message()
    send_telegram(message)
    print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
