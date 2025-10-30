# Command-line interface tool
import argparse
import requests
from rich.console import Console
from rich.syntax import Syntax
from rich.markdown import Markdown
console = Console()

def create_snippet():

    """Insert a new Code.

    Expects JSON body with:
      - language (str, required)
      - snippet (str, required)
      - tags (str, optional)
"""

    url = "http://localhost:5000/api/v1/snippets"
    title = input("Enter snippet title: ")
    
    # Multi-line code input
    print("Enter snippet code (press Ctrl+Z on Windows when done)")
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
    try:
        res = requests.post(url, json={
            "title": title,
            "snippet": code,
            "tags": tags,
            "language": language
        })
        result = res.json()
        if result.get('id'):
            print(f"Snippet created with ID: {result.get('id')}")
        else:
            print(f"Failed to create snippet: {result}")
    except requests.exceptions.RequestException as e:
            print(f"Failed to create snippet: {e}")

def create_entry():
    """Insert a new Entry.

    Expects JSON body with:
      - title (str, required)
      - content (str, required)
      - tags (str, optional)
    """

    url = "http://localhost:5000/api/v1/entries"
    title = input("Enter entry title: ")
    
    # Multi-line content input
    print("Enter entry content (press Ctrl+Z on Windows when done): ")
    content_lines = []
    try:
        while True:
            line = input()
            content_lines.append(line)
    except EOFError:
        pass
    content = "\n".join(content_lines)
    
    tags = input("Enter entry tags (comma-separated): ")
    try:
        res = requests.post(url, json={
            "title": title,
            "content": content,
            "tags": tags
        })
        result = res.json()
        if result.get('id'):
            print(f"Entry created with ID: {result.get('id')}")
        else:
            print(f"Failed to create entry: {result}")
    except requests.exceptions.RequestException as e:
            print(f"Failed to create entry: {e}")

def show_snippets():

    """Retrieve all snippets"""

    url = "http://localhost:5000/api/v1/snippets"
    try:
        res = requests.get(url)
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

    """Retrieve all entries"""

    url = "http://localhost:5000/api/v1/entries"
    try:
        res = requests.get(url)
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

    url = f"http://localhost:5000/api/v1/snippets/{snippet_id}"
    try:
        res = requests.get(url)
        snippet = res.json()

        if snippet.get('error'):
            print({'error': 'snippet not found'})
            return 
        
        print({
            "title": snippet.get("title"),
            "language": snippet.get("language"),
            "tags": snippet.get("tags"),})
        console.print("-" * 100)
        console.print(
            Syntax(snippet.get("snippet", ""), snippet.get("language", "text"), line_numbers=True)
        )
    except requests.exceptions.RequestException as e:
        console.print(f"Failed to retrieve snippet: {e}")

def show_entry(entry_id):

    """Retrieve single entry by Id"""

    url = f"http://localhost:5000/api/v1/entries/{entry_id}"
    try:
        res = requests.get(url)
        entry = res.json()

        if entry.get('error'):
            print({'error': 'entry not found'})
            return
        
        print({
            "title": entry.get("title"),
            "tags": entry.get("tags"),})
        console.print("-" * 100)
        console.print(
            Markdown(entry.get("content", ""))
        )
    except requests.exceptions.RequestException as e:
        console.print(f"Failed to retrieve entry: {e}")

def delete_snippet(snippet_id):
    """Delete a snippet by id."""
    url = f"http://localhost:5000/api/v1/snippets/{snippet_id}"
    try:
        res = requests.delete(url)
        result = res.json()
        if res.status_code == 200:
            print(f"Snippet {snippet_id} deleted successfully.")
        else:
            print(f"Failed to delete snippet: {result}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to delete snippet: {e}")

def delete_entry(entry_id):
    """Delete an entry by id."""
    url = f"http://localhost:5000/api/v1/entries/{entry_id}"
    try:
        res = requests.delete(url)
        result = res.json()
        if res.status_code == 200:
            print(f"Entry {entry_id} deleted successfully.")
        else:
            print(f"Failed to delete entry: {result}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to delete entry: {e}")

def filter_snippets_by_tag(tag):
    url = f"http://127.0.0.1:5000/api/v1/snippets/filter/tag/{tag}"
    try:
        res = requests.get(url)
        snippets = res.json()

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
    url = f"http://127.0.0.1:5000/api/v1/entries/filter/tag/{tag}"
    try:
        res = requests.get(url)
        entries = res.json()

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

def filter_entries_by_title(title):
    url = f"http://127.0.0.1:5000/api/v1/entries/filter/title/{title}"
    try:
        res = requests.get(url)
        entries = res.json()

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
    url = f"http://127.0.0.1:5000/api/v1/snippets/filter/title/{title}"
    try:
        res = requests.get(url)
        snippets = res.json()

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
    url = f"http://127.0.0.1:5000/api/v1/snippets/filter/language/{language}"
    try:
        res = requests.get(url)
        snippets = res.json()

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
    snippet_id = int(input("Enter id of the snippet to download: "))
    url = f"http://127.0.0.1:5000/export-snippet-md/v1/{snippet_id}"
    try:
        res = requests.get(url, stream=True)
        text = res.text.encode('utf-8')
        with open(f"Snippet_{snippet_id}.md", "wb") as f:
            f.write(text)
    except requests.exceptions.RequestException as e:
        console.print(f"Failed to download snippet: {e}")

def download_snippet_json():
    snippet_id = int(input("Enter id of the snippet to download: "))
    url = f"http://127.0.0.1:5000/export-snippet-json/v1/{snippet_id}"
    try:
        res = requests.get(url, stream=True)
        text = res.text.encode('utf-8')
        with open(f"Snippet_{snippet_id}.json", "wb") as f:
            f.write(text)
    except requests.exceptions.RequestException as e:
        console.print(f"Failed to download snippet: {e}")

def download_entry_md():
    entry_id = int(input("Enter id of the snippet to download: "))
    url = f"http://127.0.0.1:5000/export-entry-md/v1/{entry_id}"
    try:
        res = requests.get(url, stream=True)
        text = res.text.encode('utf-8')
        with open(f"Entry_{entry_id}.md", "wb") as f:
            f.write(text)
    except requests.exceptions.RequestException as e:
        console.print(f"Failed to download snippet: {e}")

def download_entry_json():
    entry_id = int(input("Enter id of the snippet to download: "))
    url = f"http://127.0.0.1:5000/export-entry-json/v1/{entry_id}"
    try:
        res = requests.get(url, stream=True)
        text = res.text.encode('utf-8')
        with open(f"Entry_{entry_id}.json", "wb") as f:
            f.write(text)
    except requests.exceptions.RequestException as e:
        console.print(f"Failed to download snippet: {e}")

def update_snippet(snippet_id):
    pass

def update_entry(entry_id):
    pass

def main():
    parser = argparse.ArgumentParser(
        description="DevLog CLI — manage snippets and entries"
    )

    subparsers = parser.add_subparsers(dest='command', required=True)

   
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

    args = parser.parse_args()

    match args.command:
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
        case _: parser.print_help()


if __name__ == '__main__':
    main()