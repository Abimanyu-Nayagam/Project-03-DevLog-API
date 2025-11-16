# Command-line interface tool
import argparse
import requests
from rich.console import Console
from rich.syntax import Syntax
from rich.markdown import Markdown
console = Console()

token = ""

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
    """Login a user and store JWT token globally."""
    global token

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
            token = data.get("access_token")
            print("Login successful!")
            print("Token saved.")
        else:
            print("Login failed:", data)

    except requests.exceptions.RequestException as e:
        print(f"Error during login: {e}")


def create_snippet():

    """Insert a new Code.

    Expects JSON body with:
      - language (str, required)
      - snippet (str, required)
      - tags (str, optional)
"""
    global token
    if not token:
        print("Please login first.")
        return
    
    url = "http://localhost:5000/api/v1/snippets"
    title = input("Enter snippet title: ")
    
    # Multi-line code input
    print("Enter snippet code (press Ctrl+Z and enter when done)")
    code_lines = []
    try:
        while True:
            line = input()
            code_lines.append(line)
    except EOFError:
        pass
    code = "\n".join(code_lines)
    
    tags = input("Enter snippet tags (comma-separated): ")
    language = input("Enter snippet language: ")

    headers = {"Authorization": f"Bearer {token}"}
    try:
        res = requests.post(url, json={
            "title": title,
            "snippet": code,
            "tags": tags,
            "language": language
        },  headers=headers)
        result = res.json()
        if result.get('id'):
            print(f"Snippet created with ID: {result.get('id')}")
        else:
            print(f"Failed to create snippet: {result}")
    except requests.exceptions.RequestException as e:
            print(f"Failed to create snippet: {e}")

def create_entry():
    global token
    if not token:
        print("Please login first.")
        return

    url = "http://localhost:5000/api/v1/entries"
    title = input("Enter entry title: ")
    
    print("Enter entry content (press Ctrl+Z and enter when done): ")
    content_lines = []
    try:
        while True:
            line = input()
            content_lines.append(line)
    except EOFError:
        pass
    content = "\n".join(content_lines)
    
    tags = input("Enter entry tags (comma-separated): ")
    
    headers = {"Authorization": f"Bearer {token}"}

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

    global token
    if not token:
        print("Please login first.")
        return

    """Retrieve all snippets"""

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
            }
            print(code_info)
            console.print("-" * 100)
            console.print(
                Syntax(snip.get("snippet", ""), snip.get("language", "text"), line_numbers=True)
            )
            console.print("-" * 100)
            console.print("-" * 100)

    except requests.exceptions.RequestException as e:
        console.print(f"Failed to retrieve snippets: {e}")


def show_entries():

    global token
    if not token:
        print("Please login first.")
        return

    """Retrieve all entries"""

    url = "http://localhost://localhost:5000/api/v1/entries"
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

    global token
    if not token:
        print("Please login first.")
        return

    """Retrieve single snippet by id"""

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
        })
        console.print("-" * 100)
        console.print(
            Syntax(snippet.get("snippet", ""), snippet.get("language", "text"), line_numbers=True)
        )
    except requests.exceptions.RequestException as e:
        console.print(f"Failed to retrieve snippet: {e}")


def show_entry(entry_id):

    global token
    if not token:
        print("Please login first.")
        return

    """Retrieve single entry by Id"""

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

    global token
    if not token:
        print("Please login first.")
        return

    """Delete a snippet by id."""
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

    global token
    if not token:
        print("Please login first.")
        return

    """Delete an entry by id."""
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

    global token
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



def filter_snippets_by_tag(tag):

    global token
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

    global token
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

    global token
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

    global token
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
                Syntax(snippet.get("code", ""), snippet.get("language", "text"), line_numbers=True)
            )
            console.print("-" * 100)
            console.print("-" * 100)

    except requests.exceptions.RequestException as e:
        console.print(f"Failed to retrieve snippets: {e}")

def filter_snippets_by_lang(language):

    global token
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

    global token
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

    global token
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

    global token
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

    global token
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

    global token
    if not token:
        print("Please login first.")
        return

    fetch_url = f"http://127.0.0.1:5000/api/v1/snippets/{snippet_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(fetch_url, headers=headers)
        snippet = res.json()
        print(f"Current Snippet Data for id {snippet_id}:")
        print(snippet)

        if snippet.get('error'):
            print({'error': 'snippet not found'})
            return
    except requests.exceptions.RequestException as e:
        console.print(f"Failed to retrieve snippet: {e}")
        return
    
    update_url=f"http://127.0.0.1:5000/api/v1/snippets"

    print("Add information for any field you wish to update, else leave it blank.")
    title = input("Title: ")
    tags = input("Tags (comma-separated): ")
    language = input("Language: ")
    code = input("Code: ")

    update = {"id": snippet_id}

    if title:
        update["title"] = title
    if code:
        update["snippet"] = code
    if tags:
        update["tags"] = tags
    if language:
        update["language"] = language
    
    try:
        res = requests.patch(update_url, json=update, headers=headers)
        result = res.json()
        print(result)
    except requests.exceptions.RequestException as e:
        print(f"Failed to update snippet: {e}")


def update_entry(entry_id):

    global token
    if not token:
        print("Please login first.")
        return

    fetch_url = f"http://127.0.0.1:5000/api/v1/entries/{entry_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(fetch_url, headers=headers)
        entry = res.json()
        print(f"Current Entry Data for id {entry_id}:")
        print(entry)

        if entry.get('error'):
            print({'error': 'entry not found'})
            return
    except requests.exceptions.RequestException as e:
        console.print(f"Failed to retrieve entry: {e}")
        return
    
    update_url=f"http://127.0.0.1:5000/api/v1/entries"

    print("Add information for any field you wish to update, else leave it blank.")
    title = input("Title: ")
    tags = input("Tags (comma-separated): ")
    content = input("content: ")

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
        print(result)
    except requests.exceptions.RequestException as e:
        print(f"Failed to update entry: {e}")

# Function to call the search route for snippets
def search_snippets(query):

    global token
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

    global token
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
        case 'register': register_user()
        case 'login': login_user()
        case 'create-snippet': create_snippet()
        case 'create-entry': create_entry()
        case 'show-snippets': show_snippets()
        case 'show-entries': show_entries()
        case 'show-snippet': show_snippet(args.id)
        case 'show-entry': show_entry(args.id)
        case 'update-snippet': update_snippet(args.id)
        case 'update-entry': update_entry(args.id)
        case 'delete-snippet': delete_snippet(args.id)
        case 'delete-entry': delete_entry(args.id)
        case 'download-snippet-md': download_snippet_md()
        case 'download-snippet-json': download_snippet_json()
        case 'download-entry-md': download_entry_md()
        case 'download-entry-json': download_entry_json()
        case 'filter-snippet-tag': filter_snippets_by_tag(args.tag),
        case 'filter-entry-tag': filter_entries_by_tag(args.tag),
        case 'filter-snippet-title': filter_snippets_by_title(args.title),
        case 'filter-entry-title': filter_entries_by_title(args.title),
        case 'filter-snippet-lang': filter_snippets_by_lang(args.lang),
        case 'search-snippet': search_snippets(args.query),
        case 'search-entry': search_entries(args.query),
        case _: parser.print_help()


if __name__ == '__main__':
    main()