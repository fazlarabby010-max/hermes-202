#!/usr/bin/env python3
"""
Google Integration Workflow CLI for Hermes Agent.

This script provides a command-line interface to the Google integration workflow
that creates a Gmail draft with an attachment from Google Drive.
"""

import argparse
import json
import sys
import os
from pathlib import Path

# Add the google_integration module to the path
hermes_home = Path(os.path.expanduser('~')) / '.hermes'
google_integration_path = hermes_home / 'google_integration'
if str(google_integration_path) not in sys.path:
    sys.path.insert(0, str(google_integration_path))

from workflow import create_email_with_attachment

def main():
    parser = argparse.ArgumentParser(
        description='Create a Gmail draft with an attachment from Google Drive.'
    )
    parser.add_argument(
        '--recipient',
        required=True,
        help='Email recipient'
    )
    parser.add_argument(
        '--subject',
        required=True,
        help='Email subject'
    )
    parser.add_argument(
        '--body',
        required=True,
        help='Email body'
    )
    parser.add_argument(
        '--drive-file',
        required=True,
        help='Name of the file to search for in Google Drive'
    )
    parser.add_argument(
        '--drive-folder',
        help='Optional: Limit search to this folder ID in Google Drive'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'text'],
        default='json',
        help='Output format (default: json)'
    )

    args = parser.parse_args()

    result = create_email_with_attachment(
        recipient=args.recipient,
        subject=args.subject,
        body=args.body,
        drive_file_name=args.drive_file,
        drive_folder_id=args.drive_folder
    )

    if args.format == 'json':
        print(json.dumps(result, indent=2))
    else:
        if result.get('status') == 'success':
            print(f"SUCCESS: Draft created")
            print(f"Draft ID: {result['draft_id']}")
            print(f"Draft Link: {result['draft_link']}")
            print(f"Attachment: {result['attachment']['file_name']} ({result['attachment']['mime_type']})")
        else:
            print(f"ERROR: {result['error']}", file=sys.stderr)
            sys.exit(1)

if __name__ == '__main__':
    main()