# Command-line interface tool
import argparse
import requests
from rich.console import Console
from rich.syntax import Syntax
from rich.markdown import Markdown
from pathlib import Path
console = Console()

TOKEN_FILE = Path(__file__).parent / '.devlog_token'

##Register function in CLI
def register_user():
    """Register a new user."""
    url = "http://localhost:5000/register"

    email = input("Enter email: ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    try:
        res = requests.post(url, json={
            "email": email,
            "username": username,
            "password": password
        })

        data = res.json()

        if res.status_code == 201:
            print("Registration successful!")
        else:
            print("Registration failed:", data)

    except requests.exceptions.RequestException as e:
        print(f"Error during registration: {e}")

## login function in CLI
def login_user():
    """Login a user and store JWT token to file."""
    url = "http://localhost:5000/login"

    username = input("Enter username: ")
    password = input("Enter password: ")

    try:
        res = requests.post(url, json={
            "username": username,
            "password": password
        })

        data = res.json()

        if res.status_code == 200:
            access_token = data.get("access_token")
            try:
                TOKEN_FILE.write_text(access_token)
            except Exception:
                pass
            print("Login successful!")
            print(f"Token saved to {TOKEN_FILE}")
        else:
            print("Login failed:", data)

    except requests.exceptions.RequestException as e:
        print(f"Error during login: {e}")


def logout_user():
    """Clear saved token file."""
    try:
        if TOKEN_FILE.exists():
            TOKEN_FILE.unlink()
            print(f"Logged out and removed token file {TOKEN_FILE}")
        else:
            print("Logged out (no token file found)")
    except Exception as e:
        print(f"Logout error: {e}")


def get_token():
    """Read token from file if available."""
    try:
        if TOKEN_FILE.exists():
            return TOKEN_FILE.read_text().strip()
    except Exception:
        pass
    return ""


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
            resp = requests.post("http://localhost:5000/autogen/title", json={"content": code}, headers=headers)
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
            resp = requests.post("http://localhost:5000/autogen/tags", json=payload, headers=headers)
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
            resp = requests.post("http://localhost:5000/autogen/description", json=payload, headers=headers)
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
        },  headers=headers)
        result = res.json()
        if result.get('id'):
            print(f"Snippet created with ID: {result.get('id')}")
        else:
            print(f"Failed to create snippet: {result}")
    except requests.exceptions.RequestException as e:
            print(f"Failed to create snippet: {e}")

def create_entry():
    token = get_token()
    if not token:
        print("Please login first.")
        return

    url = "http://localhost:5000/api/v1/entries"
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

    # Auto-generate fields as requested
    try:
        if not title:
            resp = requests.post("http://localhost:5000/autogen/title", json={"content": content}, headers=headers)
            if resp.ok:
                title = resp.json().get("title") or title
                if title:
                    print(f"Auto-generated title: {title}")
        if not tags:
            payload = {"content": content, "language": "markdown"}
            if title:
                payload["title"] = title
            resp = requests.post("http://localhost:5000/autogen/tags", json=payload, headers=headers)
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
            console.print(
                Syntax(snip.get("snippet", ""), snip.get("language", "text"), line_numbers=True)
            )
            if snip.get("description"):
                console.print("\nDescription:\n")
                console.print(snip.get("description"))
            console.print("-" * 100)
            console.print("-" * 100)

    except requests.exceptions.RequestException as e:
        console.print(f"Failed to retrieve snippets: {e}")


def show_entries():
    """Retrieve all entries"""
    token = get_token()
    if not token:
        print("Please login first.")
        return

    url = "http://localhost:5000/api/v1/entries"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(url, headers=headers)
        entires = res.json()

        for entry in entires:
            entry_info = {
                "title": entry.get("title"),
                "tags": entry.get("tags"),
            }
            print(entry_info)
            console.print("-" * 100)
            console.print(
                Markdown(entry.get("content", ""))
            )
            console.print("-" * 100)
            console.print("-" * 100)

    except requests.exceptions.RequestException as e:
        console.print(f"Failed to retrieve snippets: {e}")

def show_snippet(snippet_id):
    """Retrieve single snippet by id"""
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


def show_entry(entry_id):
    """Retrieve single entry by Id"""
    token = get_token()
    if not token:
        print("Please login first.")
        return

    url = f"http://localhost:5000/api/v1/entries/{entry_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(url, headers=headers)
        entry = res.json()

        if entry.get('error'):
            print({'error': 'entry not found'})
            return
        
        print({
            "title": entry.get("title"),
            "tags": entry.get("tags"),
        })
        console.print("-" * 100)
        console.print(
            Markdown(entry.get("content", ""))
        )
    except requests.exceptions.RequestException as e:
        console.print(f"Failed to retrieve entry: {e}")


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


def delete_entry(entry_id):
    """Delete an entry by id."""
    token = get_token()
    if not token:
        print("Please login first.")
        return

    url = f"http://localhost:5000/api/v1/entries/{entry_id}"
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

def filter_entries_by_tag(tag):
    token = get_token()
    if not token:
        print("Please login first.")
        return

    url = f"http://127.0.0.1:5000/api/v1/entries/filter/tag/{tag}"
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

    url = f"http://127.0.0.1:5000/api/v1/entries/filter/title/{title}"
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
            console.print(
                Markdown(entry.get("content", ""))
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

def download_snippet_md():
    token = get_token()
    if not token:
        print("Please login first.")
        return

    snippet_id = int(input("Enter id of the snippet to download: "))
    url = f"http://127.0.0.1:5000/export-snippet-md/v1/{snippet_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(url, headers=headers, stream=True)
        text = res.text.encode('utf-8')
        with open(f"Snippet_{snippet_id}.md", "wb") as f:
            f.write(text)
    except requests.exceptions.RequestException as e:
        console.print(f"Failed to download snippet: {e}")


def download_snippet_json():
    token = get_token()
    if not token:
        print("Please login first.")
        return

    snippet_id = int(input("Enter id of the snippet to download: "))
    url = f"http://127.0.0.1:5000/export-snippet-json/v1/{snippet_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(url, headers=headers, stream=True)
        text = res.text.encode('utf-8')
        with open(f"Snippet_{snippet_id}.json", "wb") as f:
            f.write(text)
    except requests.exceptions.RequestException as e:
        console.print(f"Failed to download snippet: {e}")


def download_entry_md():
    token = get_token()
    if not token:
        print("Please login first.")
        return

    entry_id = int(input("Enter id of the entry to download: "))
    url = f"http://127.0.0.1:5000/export-entry-md/v1/{entry_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(url, headers=headers, stream=True)
        text = res.text.encode('utf-8')
        with open(f"Entry_{entry_id}.md", "wb") as f:
            f.write(text)
    except requests.exceptions.RequestException as e:
        console.print(f"Failed to download snippet: {e}")


def download_entry_json():
    token = get_token()
    if not token:
        print("Please login first.")
        return

    entry_id = int(input("Enter id of the entry to download: "))
    url = f"http://127.0.0.1:5000/export-entry-json/v1/{entry_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(url, headers=headers, stream=True)
        text = res.text.encode('utf-8')
        with open(f"Entry_{entry_id}.json", "wb") as f:
            f.write(text)
    except requests.exceptions.RequestException as e:
        console.print(f"Failed to download snippet: {e}")

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

        # Display current snippet in formatted way
        print("\nCurrent Snippet:")
        print(f"Title: {snippet.get('title')}")
        print(f"Language: {snippet.get('language')}")
        print(f"Tags: {snippet.get('tags')}")
        if snippet.get('description'):
            print(f"Description: {snippet.get('description')}")
        print("\nCode:")
        print("-" * 100)
        print(
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
                resp = requests.post("http://localhost:5000/autogen/title", json={"content": content_for_gen}, headers=headers)
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
                resp = requests.post("http://localhost:5000/autogen/tags", json=payload, headers=headers)
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
                resp = requests.post("http://localhost:5000/autogen/description", json=payload, headers=headers)
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
        print(
            Syntax(result.get("snippet", ""), result.get("language", "text"), line_numbers=True)
        )
        print("-" * 100)
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to update snippet: {e}")


def update_entry(entry_id):
    token = get_token()
    if not token:
        print("Please login first.")
        return

    fetch_url = f"http://127.0.0.1:5000/api/v1/entries/{entry_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(fetch_url, headers=headers)
        entry = res.json()

        if entry.get('error'):
            print({'error': 'entry not found'})
            return

        # Display current entry in formatted way
        print("\nCurrent Entry:")
        print(f"Title: {entry.get('title')}")
        print(f"Tags: {entry.get('tags')}")
        print("\nContent:")
        print("-" * 100)
        print(entry.get("content", ""))
        print("-" * 100)
        print("\n")

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve entry: {e}")
        return

    update_url = f"http://127.0.0.1:5000/api/v1/entries"

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

    # Determine what content to use for auto-generation
    content_for_gen = content if content else entry.get("content", "")
    title_for_gen = title if title and title != 'auto' else entry.get("title", "")

    # Auto-generate fields
    try:
        if title == 'auto' or (not title and not entry.get('title')):
            yn = input("\nAuto-generate title? [y/N]: ").strip().lower()
            if yn == 'y':
                resp = requests.post("http://localhost:5000/autogen/title", json={"content": content_for_gen}, headers=headers)
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
                resp = requests.post("http://localhost:5000/autogen/tags", json=payload, headers=headers)
                if resp.ok:
                    tags = resp.json().get("tags", "")
                    if tags:
                        print(f"Auto-generated tags: {tags}")
    except requests.exceptions.RequestException:
        pass

    # Build update payload with only changed fields
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
        
        # Display updated entry in formatted way
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

# Function to call the search route for snippets
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


# Function to call the search route for snippets
def search_entries(query):
    token = get_token()
    if not token:
        print("Please login first.")
        return

    url = f"http://localhost:5000/api/v1/entries/search?q={query}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(url, headers=headers)
        entries = res.json()
        for entry in entries:
            code_info = {
                "title": entry.get("title"),
                "tags": entry.get("tags"),
            }
            print(code_info)
            console.print("-" * 100)
            console.print(
                Markdown(entry.get("content", ""))
            )
            console.print("-" * 100)
            console.print("-" * 100)
    except requests.exceptions.RequestException as e:
        console.print(f"Failed to search snippets: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="DevLog CLI — manage snippets and entries"
    )

    subparsers = parser.add_subparsers(dest='command', required=True)

    subparsers.add_parser('register', help='Register a new user')
    subparsers.add_parser('login', help='Login a user')
    subparsers.add_parser('logout', help='Logout user and clear saved token')


    subparsers.add_parser('create-snippet', help='Create a new snippet')
    subparsers.add_parser('create-entry', help='Create a new entry')
    subparsers.add_parser('show-snippets', help='Display all snippets')
    subparsers.add_parser('show-entries', help='Display all entries')
    parser_snip_one = subparsers.add_parser('show-snippet', help='Show one snippet by ID')
    parser_snip_one.add_argument('id', type=int, help='Snippet ID')
    parser_entry_one = subparsers.add_parser('show-entry', help='Show one entry by ID')
    parser_entry_one.add_argument('id', type=int, help='Entry ID')
    parser_up_snip = subparsers.add_parser('update-snippet', help='Update one snippet')
    parser_up_snip.add_argument('id', type=int, help='Snippet ID')
    parser_up_entry = subparsers.add_parser('update-entry', help='Update one entry')
    parser_up_entry.add_argument('id', type=int, help='Entry ID')
    parser_del_snip = subparsers.add_parser('delete-snippet', help='Delete a snippet')
    parser_del_snip.add_argument('id', type=int, help='Snippet ID')
    parser_del_entry = subparsers.add_parser('delete-entry', help='Delete an entry')
    parser_del_entry.add_argument('id', type=int, help='Entry ID')
    subparsers.add_parser('download-entry', help='Download all entries')
    subparsers.add_parser('download-snippet-md', help='Download snippet by id')
    subparsers.add_parser('download-entry-md', help='Download snippet by id')
    subparsers.add_parser('download-snippet-json', help='Download snippet by id')
    subparsers.add_parser('download-entry-json', help='Download snippet by id')
    filter_entry_by_tag = subparsers.add_parser('filter-entry-tag', help='Filter an entry by tag')
    filter_entry_by_tag.add_argument('tag', type=str, help='Tag')
    filter_entry_by_title = subparsers.add_parser('filter-entry-title', help='Filter an entry by title')
    filter_entry_by_title.add_argument('title', type=str, help='Title')
    filter_snippet_by_tag = subparsers.add_parser('filter-snippet-tag', help='Filter a snippet by tag')
    filter_snippet_by_tag.add_argument('tag', type=str, help='Tag')
    filter_snippet_by_title = subparsers.add_parser('filter-snippet-title', help='Filter a snippet by title')
    filter_snippet_by_title.add_argument('title', type=str, help='Title')
    filter_snippet_by_lang = subparsers.add_parser('filter-snippet-lang', help='Filter a snippet by lang')
    filter_snippet_by_lang.add_argument('lang', type=str, help='Language')
    search_snippet = subparsers.add_parser('search-snippet', help='Search a snippet')
    search_snippet.add_argument('query', type=str, help='query')
    search_entry = subparsers.add_parser('search-entry', help='Search a entry')
    search_entry.add_argument('query', type=str, help='query')

    args = parser.parse_args()

    match args.command:
        case 'register':
            register_user()
        case 'login':
            login_user()
        case 'create-snippet':
            create_snippet()
        case 'create-entry':
            create_entry()
        case 'show-snippets':
            show_snippets()
        case 'show-entries':
            show_entries()
        case 'show-snippet':
            show_snippet(args.id)
        case 'show-entry':
            show_entry(args.id)
        case 'update-snippet':
            update_snippet(args.id)
        case 'update-entry':
            update_entry(args.id)
        case 'delete-snippet':
            delete_snippet(args.id)
        case 'delete-entry':
            delete_entry(args.id)
        case 'download-snippet-md':
            download_snippet_md()
        case 'download-snippet-json':
            download_snippet_json()
        case 'download-entry-md':
            download_entry_md()
        case 'download-entry-json':
            download_entry_json()
        case 'filter-snippet-tag':
            filter_snippets_by_tag(args.tag)
        case 'filter-entry-tag':
            filter_entries_by_tag(args.tag)
        case 'filter-snippet-title':
            filter_snippets_by_title(args.title)
        case 'filter-entry-title':
            filter_entries_by_title(args.title)
        case 'filter-snippet-lang':
            filter_snippets_by_lang(args.lang)
        case 'search-snippet':
            search_snippets(args.query)
        case 'search-entry':
            search_entries(args.query)
        case 'logout':
            logout_user()
        case _:
            parser.print_help()


if __name__ == '__main__':
    main()