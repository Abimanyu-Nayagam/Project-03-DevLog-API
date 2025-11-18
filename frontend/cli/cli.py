# cli.py

import argparse

# Import groups
from auth import register_user, login_user, logout_user
from snippet import (
    create_snippet,
    show_snippets,
    show_snippet,
    update_snippet,
    delete_snippet,
    filter_snippets_by_tag,
    filter_snippets_by_title,
    filter_snippets_by_lang,
    search_snippets
)
from entry import (
    create_entry,
    show_entries,
    show_entry,
    update_entry,
    delete_entry,
    filter_entries_by_tag,
    filter_entries_by_title,
    search_entries
)
from downloads import (
    download_snippet_md,
    download_snippet_json,
    download_entry_md,
    download_entry_json
)


def main():
    parser = argparse.ArgumentParser(
        description="DevLog CLI — manage snippets and entries"
    )

    subparsers = parser.add_subparsers(dest='command', required=True)

    # Auth
    subparsers.add_parser('register', help='Register a new user')
    subparsers.add_parser('login', help='Login a user')
    subparsers.add_parser('logout', help='Logout user')

    # Snippet creation, listing
    subparsers.add_parser('create-snippet', help='Create a new snippet')
    subparsers.add_parser('show-snippets', help='Display all snippets')

    # Entry creation, listing
    subparsers.add_parser('create-entry', help='Create a new entry')
    subparsers.add_parser('show-entries', help='Display all entries')

    # Show single snippet
    parser_snip_one = subparsers.add_parser('show-snippet', help='Show one snippet by ID')
    parser_snip_one.add_argument('id', type=int)

    # Show single entry
    parser_entry_one = subparsers.add_parser('show-entry', help='Show one entry by ID')
    parser_entry_one.add_argument('id', type=int)

    # Update snippet
    parser_up_snip = subparsers.add_parser('update-snippet', help='Update one snippet')
    parser_up_snip.add_argument('id', type=int)

    # Update entry
    parser_up_entry = subparsers.add_parser('update-entry', help='Update one entry')
    parser_up_entry.add_argument('id', type=int)

    # Delete snippet
    parser_del_snip = subparsers.add_parser('delete-snippet', help='Delete a snippet')
    parser_del_snip.add_argument('id', type=int)

    # Delete entry
    parser_del_entry = subparsers.add_parser('delete-entry', help='Delete an entry')
    parser_del_entry.add_argument('id', type=int)

    # Downloads
    subparsers.add_parser('download-snippet-md', help='Download snippet MD')
    subparsers.add_parser('download-snippet-json', help='Download snippet JSON')
    subparsers.add_parser('download-entry-md', help='Download entry MD')
    subparsers.add_parser('download-entry-json', help='Download entry JSON')

    # Filters
    filter_entry_by_tag = subparsers.add_parser('filter-entry-tag', help='Filter entries by tag')
    filter_entry_by_tag.add_argument('tag', type=str)

    filter_entry_by_title = subparsers.add_parser('filter-entry-title', help='Filter entries by title')
    filter_entry_by_title.add_argument('title', type=str)

    filter_snippet_by_tag = subparsers.add_parser('filter-snippet-tag', help='Filter snippets by tag')
    filter_snippet_by_tag.add_argument('tag', type=str)

    filter_snippet_by_title = subparsers.add_parser('filter-snippet-title', help='Filter snippets by title')
    filter_snippet_by_title.add_argument('title', type=str)

    filter_snippet_by_lang = subparsers.add_parser('filter-snippet-lang', help='Filter snippets by language')
    filter_snippet_by_lang.add_argument('lang', type=str)

    # Search
    search_snippet = subparsers.add_parser('search-snippet', help='Search snippets')
    search_snippet.add_argument('query', type=str)

    search_entry = subparsers.add_parser('search-entry', help='Search entries')
    search_entry.add_argument('query', type=str)

    args = parser.parse_args()

    match args.command:
        case 'register':
            register_user()
        case 'login':
            login_user()
        case 'logout':
            logout_user()
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
        case _:
            parser.print_help()


if __name__ == '__main__':
    main()
