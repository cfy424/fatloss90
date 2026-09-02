#!/usr/bin/env python3
"""Send a message to a Feishu (Lark) custom bot webhook with signature verification."""

import argparse
import base64
import certifi
import hashlib
import hmac
import json
import ssl
import sys
import time
import urllib.request
from pathlib import Path


def load_config():
    cfg_path = Path(__file__).resolve().parent / "feishu_config.json"
    return json.loads(cfg_path.read_text(encoding="utf-8"))


def build_sign(timestamp: str, secret: str) -> str:
    string_to_sign = f"{timestamp}\n{secret}"
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
    return base64.b64encode(hmac_code).decode("utf-8")


def send(webhook: str, secret: str, text: str, msg_type: str = "text") -> dict:
    timestamp = str(int(time.time()))
    sign = build_sign(timestamp, secret)
    if msg_type == "text":
        payload = {
            "timestamp": timestamp,
            "sign": sign,
            "msg_type": "text",
            "content": {"text": text},
        }
    elif msg_type == "post":
        payload = {
            "timestamp": timestamp,
            "sign": sign,
            "msg_type": "post",
            "content": {"post": {"zh_cn": {"title": "", "content": [[{"tag": "text", "text": text}]]}}},
        }
    else:
        raise ValueError(f"Unsupported msg_type: {msg_type}")

    req = urllib.request.Request(
        webhook,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    context = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(req, timeout=15, context=context) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    parser = argparse.ArgumentParser(description="Send a message to Feishu custom bot")
    parser.add_argument("--text", required=True, help="Message text to send")
    parser.add_argument(
        "--msg-type",
        choices=["text", "post"],
        default="text",
        help="Feishu message type (default: text)",
    )
    args = parser.parse_args()

    config = load_config()
    result = send(config["webhook"], config["secret"], args.text, args.msg_type)
    print(json.dumps(result, ensure_ascii=False))
    if result.get("code") != 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
