# entry.py

import requests
from utils import console
from auth import get_token
from rich.markdown import Markdown


def create_entry():
    token = get_token()
    if not token:
        print("Please login first.")
        return

    url = "http://localhost:5000/api/entries"
    headers = {"Authorization": f"Bearer {token}"}

    title = input("Enter entry title (leave blank to auto-generate): ").strip()

    print("Enter entry content (press Ctrl+Z then Enter when done):")
    content_lines = []
    try:
        while True:
            line = input()
            content_lines.append(line)
    except EOFError:
        pass
    content = "\n".join(content_lines).strip()

    tags = input("Enter entry tags (comma-separated, leave blank to auto-generate): ").strip()

    # Auto-generation
    try:
        if not title:
            resp = requests.post("http://localhost:5000/api/autogen/title", json={"content": content}, headers=headers)
            if resp.ok:
                title = resp.json().get("title") or title
                if title:
                    print(f"Auto-generated title: {title}")

        if not tags:
            payload = {"content": content, "language": "markdown"}
            if title:
                payload["title"] = title
            resp = requests.post("http://localhost:5000/api/autogen/tags", json=payload, headers=headers)
            if resp.ok:
                tags = resp.json().get("tags") or tags
                if tags:
                    print(f"Auto-generated tags: {tags}")

    except requests.exceptions.RequestException:
        pass

    try:
        res = requests.post(url, json={
            "title": title,
            "content": content,
            "tags": tags
        }, headers=headers)

        result = res.json()
        if result.get('id'):
            print(f"Entry created with ID: {result.get('id')}")
        else:
            print(f"Failed to create entry: {result}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to create entry: {e}")


def show_entries():
    token = get_token()
    if not token:
        print("Please login first.")
        return

    url = "http://localhost:5000/api/entries"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(url, headers=headers)
        entries = res.json()

        for entry in entries:
            entry_info = {
                "title": entry.get("title"),
                "tags": entry.get("tags"),
            }
            print(entry_info)

            console.print("-" * 100)
            console.print(Markdown(entry.get("content", "")))
            console.print("-" * 100)
            console.print("-" * 100)

    except requests.exceptions.RequestException as e:
        console.print(f"Failed to retrieve entries: {e}")


def show_entry(entry_id):
    token = get_token()
    if not token:
        print("Please login first.")
        return

    url = f"http://localhost:5000/api/entries/{entry_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(url, headers=headers)
        entry = res.json()

        if entry.get("error"):
            print({"error": "entry not found"})
            return

        print({
            "title": entry.get("title"),
            "tags": entry.get("tags"),
        })

        console.print("-" * 100)
        console.print(Markdown(entry.get("content", "")))

    except requests.exceptions.RequestException as e:
        console.print(f"Failed to retrieve entry: {e}")


def update_entry(entry_id):
    token = get_token()
    if not token:
        print("Please login first.")
        return

    fetch_url = f"http://127.0.0.1:5000/api/entries/{entry_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(fetch_url, headers=headers)
        entry = res.json()

        if entry.get("error"):
            print({"error": "entry not found"})
            return

        print("\nCurrent Entry:")
        print(f"Title: {entry.get('title')}")
        print(f"Tags: {entry.get('tags')}")
        print("\nContent:")
        print("-" * 100)
        console.print(Markdown(entry.get("content", "")))
        print("-" * 100)
        print("\n")

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve entry: {e}")
        return

    update_url = f"http://127.0.0.1:5000/api/entries"

    print("Update fields (leave blank to keep current, or type 'auto' to auto-generate):\n")

    title = input(f"Title [{entry.get('title')}]: ").strip()
    tags = input(f"Tags [{entry.get('tags')}]: ").strip()

    print("\nContent (press Ctrl+Z then Enter when done, or leave empty to keep current):")
    content_lines = []
    try:
        while True:
            line = input()
            content_lines.append(line)
    except EOFError:
        pass

    content = "\n".join(content_lines).strip()

    content_for_gen = content if content else entry.get("content", "")
    title_for_gen = title if title and title != 'auto' else entry.get("title", "")

    try:
        if title == 'auto' or (not title and not entry.get('title')):
            yn = input("\nAuto-generate title? [y/N]: ").strip().lower()
            if yn == 'y':
                resp = requests.post("http://localhost:5000/api/autogen/title",
                                     json={"content": content_for_gen},
                                     headers=headers)
                if resp.ok:
                    title = resp.json().get("title", "")
                    if title:
                        print(f"Auto-generated title: {title}")

        if tags == 'auto' or (not tags and not entry.get('tags')):
            yn = input("Auto-generate tags? [y/N]: ").strip().lower()
            if yn == 'y':
                payload = {"content": content_for_gen, "language": "markdown"}
                if title_for_gen:
                    payload["title"] = title_for_gen
                resp = requests.post("http://localhost:5000/api/autogen/tags",
                                     json=payload,
                                     headers=headers)
                if resp.ok:
                    tags = resp.json().get("tags", "")
                    if tags:
                        print(f"Auto-generated tags: {tags}")

    except requests.exceptions.RequestException:
        pass

    update = {"id": entry_id}
    if title:
        update["title"] = title
    if content:
        update["content"] = content
    if tags:
        update["tags"] = tags

    try:
        res = requests.patch(update_url, json=update, headers=headers)
        result = res.json()

        print("\nEntry Updated Successfully!\n")
        print("Updated Entry:")
        print(f"Title: {result.get('title')}")
        print(f"Tags: {result.get('tags')}")
        print("\nContent:")
        print("-" * 100)
        console.print(Markdown(result.get("content", "")))
        print("-" * 100)

    except requests.exceptions.RequestException as e:
        print(f"Failed to update entry: {e}")


def delete_entry(entry_id):
    token = get_token()
    if not token:
        print("Please login first.")
        return

    url = f"http://localhost:5000/api/entries/{entry_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.delete(url, headers=headers)
        result = res.json()

        if res.status_code == 200:
            print(f"Entry {entry_id} deleted successfully.")
        else:
            print(f"Failed to delete entry: {result}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to delete entry: {e}")


def filter_entries_by_tag(tag):
    token = get_token()
    if not token:
        print("Please login first.")
        return

    url = f"http://127.0.0.1:5000/api/entries/filter/tag/{tag}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(url, headers=headers)
        entries = res.json()

        if 'error' in entries:
            print({'error': 'no entries found with the given tag'})
            return

        for entry in entries:
            entry_info = {
                "title": entry.get("title"),
                "tags": entry.get("tags"),
            }
            print(entry_info)

            console.print("-" * 100)
            console.print(Markdown(entry.get("content", "")))
            console.print("-" * 100)
            console.print("-" * 100)

    except requests.exceptions.RequestException as e:
        console.print(f"Failed to retrieve entries: {e}")


def filter_entries_by_title(title):
    token = get_token()
    if not token:
        print("Please login first.")
        return

    url = f"http://127.0.0.1:5000/api/entries/filter/title/{title}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(url, headers=headers)
        entries = res.json()

        if 'error' in entries:
            print({'error': 'no snippets found with the given title'})
            return

        for entry in entries:
            entry_info = {
                "title": entry.get("title"),
                "tags": entry.get("tags"),
            }
            print(entry_info)

            console.print("-" * 100)
            console.print(Markdown(entry.get("content", "")))
            console.print("-" * 100)
            console.print("-" * 100)

    except requests.exceptions.RequestException as e:
        console.print(f"Failed to retrieve entries: {e}")


def search_entries(query):
    token = get_token()
    if not token:
        print("Please login first.")
        return

    url = f"http://localhost:5000/api/entries/search?q={query}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(url, headers=headers)
        entries = res.json()

        for entry in entries:
            entry_info = {
                "title": entry.get("title"),
                "tags": entry.get("tags"),
            }
            print(entry_info)

            console.print("-" * 100)
            console.print(Markdown(entry.get("content", "")))
            console.print("-" * 100)
            console.print("-" * 100)

    except requests.exceptions.RequestException as e:
        console.print(f"Failed to search entries: {e}")
