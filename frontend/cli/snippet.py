# snippet.py

import requests
from utils import console
from auth import get_token
from rich.syntax import Syntax
from rich.markdown import Markdown


def create_snippet():
    """Create a new snippet with optional auto-generation for title/tags/description."""
    token = get_token()
    if not token:
        print("Please login first.")
        return

    url = "http://localhost:5000/api/v1/snippets"
    headers = {"Authorization": f"Bearer {token}"}

    title = input("Enter snippet title (leave blank to auto-generate): ").strip()
    language = input("Enter snippet language: ").strip()

    print("Enter snippet code (press Ctrl+Z then Enter when done):")
    code_lines = []
    try:
        while True:
            line = input()
            code_lines.append(line)
    except EOFError:
        pass
    code = "\n".join(code_lines).strip()

    tags = input("Enter snippet tags (comma-separated, leave blank to auto-generate): ").strip()
    description = input("Enter snippet description (leave blank to auto-generate): ").strip()

    # Auto-generate fields as requested
    try:
        if not title:
            resp = requests.post("http://localhost:5000/api/autogen/title", json={"content": code}, headers=headers)
            if resp.ok:
                title = resp.json().get("title") or title
                if title:
                    print(f"Auto-generated title: {title}")

        if not tags:
            payload = {"content": code}
            if language:
                payload["language"] = language
            if title:
                payload["title"] = title
            resp = requests.post("http://localhost:5000/api/autogen/tags", json=payload, headers=headers)
            if resp.ok:
                tags = resp.json().get("tags") or tags
                if tags:
                    print(f"Auto-generated tags: {tags}")

        if not description:
            payload = {"content": code}
            if language:
                payload["language"] = language
            if title:
                payload["title"] = title
            resp = requests.post("http://localhost:5000/api/autogen/description", json=payload, headers=headers)
            if resp.ok:
                description = resp.json().get("description") or description
                if description:
                    print("Auto-generated description:")
                    print(description)
    except requests.exceptions.RequestException:
        pass

    try:
        res = requests.post(url, json={
            "title": title,
            "snippet": code,
            "tags": tags,
            "language": language,
            "description": description
        }, headers=headers)

        result = res.json()
        if result.get('id'):
            print(f"Snippet created with ID: {result.get('id')}")
        else:
            print(f"Failed to create snippet: {result}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to create snippet: {e}")


def show_snippets():
    """Retrieve all snippets"""
    token = get_token()
    if not token:
        print("Please login first.")
        return

    url = "http://localhost:5000/api/v1/snippets"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        snippets = res.json()

        for snip in snippets:
            code_info = {
                "title": snip.get("title"),
                "language": snip.get("language"),
                "tags": snip.get("tags"),
                "description": snip.get("description", "")
            }
            print(code_info)
            console.print("-" * 100)
            console.print(Syntax(snip.get("snippet", ""), snip.get("language", "text"), line_numbers=True))

            if snip.get("description"):
                console.print("\nDescription:\n")
                console.print(snip.get("description"))

            console.print("-" * 100)
            console.print("-" * 100)

    except requests.exceptions.RequestException as e:
        console.print(f"Failed to retrieve snippets: {e}")


def show_snippet(snippet_id):
    """Retrieve single snippet by ID"""
    token = get_token()
    if not token:
        print("Please login first.")
        return

    url = f"http://localhost:5000/api/v1/snippets/{snippet_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(url, headers=headers)
        snippet = res.json()

        if snippet.get('error'):
            print({'error': 'snippet not found'})
            return

        print({
            "title": snippet.get("title"),
            "language": snippet.get("language"),
            "tags": snippet.get("tags"),
            "description": snippet.get("description", "")
        })

        console.print("-" * 100)
        console.print(
            Syntax(snippet.get("snippet", ""), snippet.get("language", "text"), line_numbers=True)
        )
        console.print("-" * 100)

        if snippet.get("description"):
            console.print("\nDescription:")
            console.print(snippet.get("description"))
            console.print("-" * 100)

    except requests.exceptions.RequestException as e:
        console.print(f"Failed to retrieve snippet: {e}")


def update_snippet(snippet_id):
    token = get_token()
    if not token:
        print("Please login first.")
        return

    fetch_url = f"http://127.0.0.1:5000/api/v1/snippets/{snippet_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(fetch_url, headers=headers)
        snippet = res.json()

        if snippet.get('error'):
            print({'error': 'snippet not found'})
            return

        print("\nCurrent Snippet:")
        print(f"Title: {snippet.get('title')}")
        print(f"Language: {snippet.get('language')}")
        print(f"Tags: {snippet.get('tags')}")
        if snippet.get('description'):
            print(f"Description: {snippet.get('description')}")
        print("\nCode:")
        print("-" * 100)
        console.print(
            Syntax(snippet.get("snippet", ""), snippet.get("language", "text"), line_numbers=True)
        )
        print("-" * 100)
        print("\n")

    except requests.exceptions.RequestException as e:
        console.print(f"Failed to retrieve snippet: {e}")
        return

    update_url = f"http://127.0.0.1:5000/api/v1/snippets"

    print("Update fields (leave blank to keep current, or type 'auto' to auto-generate):\n")

    title = input(f"Title [{snippet.get('title')}]: ").strip()
    language = input(f"Language [{snippet.get('language')}]: ").strip()
    tags = input(f"Tags [{snippet.get('tags')}]: ").strip()
    description = input(f"Description [{snippet.get('description', '')}]: ").strip()

    print("\nCode (press Ctrl+Z then Enter when done, or leave empty to keep current):")
    code_lines = []
    try:
        while True:
            line = input()
            code_lines.append(line)
    except EOFError:
        pass

    code = "\n".join(code_lines).strip()

    # Determine what content to use for auto-generation
    content_for_gen = code if code else snippet.get("snippet", "")
    lang_for_gen = language if language else snippet.get("language", "")
    title_for_gen = title if title and title != 'auto' else snippet.get("title", "")

    # Auto-generate fields
    try:
        if title == 'auto' or (not title and not snippet.get('title')):
            yn = input("\nAuto-generate title? [y/N]: ").strip().lower()
            if yn == 'y':
                resp = requests.post("http://localhost:5000/api/autogen/title", json={"content": content_for_gen}, headers=headers)
                if resp.ok:
                    title = resp.json().get("title", "")
                    if title:
                        print(f"Auto-generated title: {title}")

        if tags == 'auto' or (not tags and not snippet.get('tags')):
            yn = input("Auto-generate tags? [y/N]: ").strip().lower()
            if yn == 'y':
                payload = {"content": content_for_gen}
                if lang_for_gen:
                    payload["language"] = lang_for_gen
                if title_for_gen:
                    payload["title"] = title_for_gen
                resp = requests.post("http://localhost:5000/api/autogen/tags", json=payload, headers=headers)
                if resp.ok:
                    tags = resp.json().get("tags", "")
                    if tags:
                        print(f"Auto-generated tags: {tags}")

        if description == 'auto' or (not description and not snippet.get('description')):
            yn = input("Auto-generate description? [y/N]: ").strip().lower()
            if yn == 'y':
                payload = {"content": content_for_gen}
                if lang_for_gen:
                    payload["language"] = lang_for_gen
                if title_for_gen:
                    payload["title"] = title_for_gen
                resp = requests.post("http://localhost:5000/api/autogen/description", json=payload, headers=headers)
                if resp.ok:
                    description = resp.json().get("description", "")
                    if description:
                        print(f"Auto-generated description: {description}")
    except requests.exceptions.RequestException:
        pass

    # Build update payload with only changed fields
    update = {"id": snippet_id}
    if title:
        update["title"] = title
    if code:
        update["snippet"] = code
    if tags:
        update["tags"] = tags
    if language:
        update["language"] = language
    if description:
        update["description"] = description

    try:
        res = requests.patch(update_url, json=update, headers=headers)
        result = res.json()

        # Display updated snippet in formatted way
        print("\nSnippet Updated Successfully!\n")
        print("Updated Snippet:")
        print(f"Title: {result.get('title')}")
        print(f"Language: {result.get('language')}")
        print(f"Tags: {result.get('tags')}")
        if result.get('description'):
            print(f"Description: {result.get('description')}")
        print("\nCode:")
        print("-" * 100)
        console.print(
            Syntax(result.get("snippet", ""), result.get("language", "text"), line_numbers=True)
        )
        print("-" * 100)

    except requests.exceptions.RequestException as e:
        print(f"Failed to update snippet: {e}")


def delete_snippet(snippet_id):
    """Delete a snippet by id."""
    token = get_token()
    if not token:
        print("Please login first.")
        return

    url = f"http://localhost:5000/api/v1/snippets/{snippet_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.delete(url, headers=headers)
        result = res.json()
        if res.status_code == 200:
            print(f"Snippet {snippet_id} deleted successfully.")
        else:
            print(f"Failed to delete snippet: {result}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to delete snippet: {e}")


def filter_snippets_by_tag(tag):
    token = get_token()
    if not token:
        print("Please login first.")
        return

    url = f"http://127.0.0.1:5000/api/v1/snippets/filter/tag/{tag}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(url, headers=headers)
        snippets = res.json()

        if 'error' in snippets:
            print({'error': 'no snippets found with the given tag'})
            return

        for snippet in snippets:
            snippets_info = {
                "title": snippet.get("title"),
                "language": snippet.get("language"),
                "tags": snippet.get("tags"),
            }
            print(snippets_info)
            console.print("-" * 100)
            console.print(
                Syntax(snippet.get("snippet", ""), snippet.get("language", "text"), line_numbers=True)
            )
            console.print("-" * 100)
            console.print("-" * 100)

    except requests.exceptions.RequestException as e:
        console.print(f"Failed to retrieve snippets: {e}")


def filter_snippets_by_title(title):
    token = get_token()
    if not token:
        print("Please login first.")
        return

    url = f"http://127.0.0.1:5000/api/v1/snippets/filter/title/{title}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(url, headers=headers)
        snippets = res.json()

        if 'error' in snippets:
            print({'error': 'no snippets found with the given title'})
            return

        for snippet in snippets:
            snippets_info = {
                "title": snippet.get("title"),
                "language": snippet.get("language"),
                "tags": snippet.get("tags"),
            }
            print(snippets_info)
            console.print("-" * 100)
            console.print(
                Syntax(snippet.get("snippet", ""), snippet.get("language", "text"), line_numbers=True)
            )
            console.print("-" * 100)
            console.print("-" * 100)

    except requests.exceptions.RequestException as e:
        console.print(f"Failed to retrieve snippets: {e}")


def filter_snippets_by_lang(language):
    token = get_token()
    if not token:
        print("Please login first.")
        return

    url = f"http://127.0.0.1:5000/api/v1/snippets/filter/language/{language}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(url, headers=headers)
        snippets = res.json()

        if 'error' in snippets:
            print({'error': 'no snippets found with the given language'})
            return

        for snippet in snippets:
            snippets_info = {
                "title": snippet.get("title"),
                "language": snippet.get("language"),
                "tags": snippet.get("tags"),
            }
            print(snippets_info)
            console.print("-" * 100)
            console.print(
                Syntax(snippet.get("snippet", ""), snippet.get("language", "text"), line_numbers=True)
            )
            console.print("-" * 100)
            console.print("-" * 100)

    except requests.exceptions.RequestException as e:
        console.print(f"Failed to retrieve snippets: {e}")


def search_snippets(query):
    token = get_token()
    if not token:
        print("Please login first.")
        return

    url = f"http://localhost:5000/api/v1/snippets/search?q={query}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(url, headers=headers)
        snippets = res.json()
        for snip in snippets:
            code_info = {
                "title": snip.get("title"),
                "language": snip.get("language"),
                "tags": snip.get("tags"),
            }
            print(code_info)
            console.print("-" * 100)
            console.print(
                Syntax(snip.get("snippet", ""), snip.get("language", "text"), line_numbers=True)
            )
            console.print("-" * 100)
            console.print("-" * 100)
    except requests.exceptions.RequestException as e:
        console.print(f"Failed to search snippets: {e}")
