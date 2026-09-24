"""Digital Samba REST API wrapper — direct port of utils/digital_samba_video.py.
Only change: credentials come from config.settings instead of st.secrets.
"""

from datetime import datetime

import requests

from config import settings

API_BASE = "https://api.digitalsamba.com/api/v1"


def _auth():
    return (settings.DIGITALSAMBA_TEAM_ID, settings.DIGITALSAMBA_DEVELOPER_KEY)


def _raise_with_body(resp: requests.Response):
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        raise requests.HTTPError(f"{e} — response body: {resp.text}") from None


def create_room(room_name: str, expires_at: datetime) -> dict:
    payload = {
        "friendly_url": room_name,
        "privacy": "private",
        "expires_at": expires_at.strftime("%Y-%m-%d %H:%M:%S"),
        "roles": ["teacher", "student"],
        "default_role": "student",
    }
    resp = requests.post(f"{API_BASE}/rooms", json=payload, auth=_auth(), timeout=10)
    _raise_with_body(resp)
    data = resp.json()
    return {"id": data["id"], "friendly_url": data.get("friendly_url", room_name)}


def generate_join_link(room_id: str, display_name: str, role: str) -> str:
    payload = {"u": display_name, "role": role}
    resp = requests.post(f"{API_BASE}/rooms/{room_id}/token", json=payload, auth=_auth(), timeout=10)
    _raise_with_body(resp)
    return resp.json()["link"]


def end_room_now(room_id: str) -> None:
    resp = requests.delete(f"{API_BASE}/rooms/{room_id}", auth=_auth(), timeout=10)
    if resp.status_code not in (200, 204, 404):
        _raise_with_body(resp)
