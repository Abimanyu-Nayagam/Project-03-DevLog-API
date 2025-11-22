# downloads.py

import requests
from utils import console
from auth import get_token


def download_snippet_md():
    token = get_token()
    if not token:
        print("Please login first.")
        return

    snippet_id = int(input("Enter id of the snippet to download: "))
    url = f"http://127.0.0.1:5000/api/export-snippet-md/{snippet_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(url, headers=headers, stream=True)
        text = res.text.encode('utf-8')
        with open(f"Snippet_{snippet_id}.md", "wb") as f:
            f.write(text)
        print(f"Snippet_{snippet_id}.md saved successfully.")
    except requests.exceptions.RequestException as e:
        console.print(f"Failed to download snippet: {e}")


def download_snippet_json():
    token = get_token()
    if not token:
        print("Please login first.")
        return

    snippet_id = int(input("Enter id of the snippet to download: "))
    url = f"http://127.0.0.1:5000/api/export-snippet-json/{snippet_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(url, headers=headers, stream=True)
        text = res.text.encode('utf-8')
        with open(f"Snippet_{snippet_id}.json", "wb") as f:
            f.write(text)
        print(f"Snippet_{snippet_id}.json saved successfully.")
    except requests.exceptions.RequestException as e:
        console.print(f"Failed to download snippet: {e}")


def download_entry_md():
    token = get_token()
    if not token:
        print("Please login first.")
        return

    entry_id = int(input("Enter id of the entry to download: "))
    url = f"http://127.0.0.1:5000/api/export-entry-md/{entry_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(url, headers=headers, stream=True)
        text = res.text.encode('utf-8')
        with open(f"Entry_{entry_id}.md", "wb") as f:
            f.write(text)
        print(f"Entry_{entry_id}.md saved successfully.")
    except requests.exceptions.RequestException as e:
        console.print(f"Failed to download entry: {e}")


def download_entry_json():
    token = get_token()
    if not token:
        print("Please login first.")
        return

    entry_id = int(input("Enter id of the entry to download: "))
    url = f"http://127.0.0.1:5000/api/export-entry-json/{entry_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(url, headers=headers, stream=True)
        text = res.text.encode('utf-8')
        with open(f"Entry_{entry_id}.json", "wb") as f:
            f.write(text)
        print(f"Entry_{entry_id}.json saved successfully.")
    except requests.exceptions.RequestException as e:
        console.print(f"Failed to download entry: {e}")
