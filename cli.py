# Command-line interface tool
import argparse
import requests
from rich.console import Console
from rich.syntax import Syntax
console = Console()

def create_snippet():
    print("✅ Snippet created successfully!")

def create_entry():
    print("✅ Entry created successfully!")

def show_snippets():
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
            console.print(
                Syntax(snip.get("snippet", ""), snip.get("language", "text"), line_numbers=True)
            )
            console.print("-" * 50)

    except requests.exceptions.RequestException as e:
        console.print(f"Failed to retrieve snippets: {e}")

def show_entries():
    print("📄 Displaying all entries...")

def show_snippet(snippet_id):
    print(f"📄 Showing snippet with ID: {snippet_id}")

def show_entry(entry_id):
    print(f"📄 Showing entry with ID: {entry_id}")

def update_snippet(snippet_id):
    print(f"🛠️ Updating snippet {snippet_id}...")

def update_entry(entry_id):
    print(f"🛠️ Updating entry {entry_id}...")

def delete_snippet(snippet_id):
    print(f"🗑️ Deleted snippet {snippet_id}")

def delete_entry(entry_id):
    print(f"🗑️ Deleted entry {entry_id}")

def download_snippets():
    print("⬇️ Downloading all snippets...")

def download_entries():
    print("⬇️ Downloading all entries...")


# ------------------------------
# CLI setup
# ------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="DevLog CLI — manage snippets and entries"
    )

    subparsers = parser.add_subparsers(dest='command', required=True)

    # 1️⃣ Create snippet
    subparsers.add_parser('create-snippet', help='Create a new snippet')

    # 2️⃣ Create entry
    subparsers.add_parser('create-entry', help='Create a new entry')

    # 3️⃣ Display all snippets
    subparsers.add_parser('show-snippets', help='Display all snippets')

    # 4️⃣ Display all entries
    subparsers.add_parser('show-entries', help='Display all entries')

    # 5️⃣ Display one snippet
    parser_snip_one = subparsers.add_parser('show-snippet', help='Show one snippet by ID')
    parser_snip_one.add_argument('id', type=int, help='Snippet ID')

    # 6️⃣ Display one entry
    parser_entry_one = subparsers.add_parser('show-entry', help='Show one entry by ID')
    parser_entry_one.add_argument('id', type=int, help='Entry ID')

    # 7️⃣ Update one snippet
    parser_up_snip = subparsers.add_parser('update-snippet', help='Update one snippet')
    parser_up_snip.add_argument('id', type=int, help='Snippet ID')

    # 8️⃣ Update one entry
    parser_up_entry = subparsers.add_parser('update-entry', help='Update one entry')
    parser_up_entry.add_argument('id', type=int, help='Entry ID')

    # 9️⃣ Delete snippet
    parser_del_snip = subparsers.add_parser('delete-snippet', help='Delete a snippet')
    parser_del_snip.add_argument('id', type=int, help='Snippet ID')

    # 🔟 Delete entry
    parser_del_entry = subparsers.add_parser('delete-entry', help='Delete an entry')
    parser_del_entry.add_argument('id', type=int, help='Entry ID')

    # 11️⃣ Download entries
    subparsers.add_parser('download-entries', help='Download all entries')

    # 12️⃣ Download snippets
    subparsers.add_parser('download-snippets', help='Download all snippets')


    # ------------------------------
    # Parse arguments and route command
    # ------------------------------
    args = parser.parse_args()

    # Routing logic
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
        case 'download-snippets': download_snippets()
        case 'download-entries': download_entries()
        case _: parser.print_help()


if __name__ == '__main__':
    main()
