#!/usr/bin/env python3
"""
set_temporary_instance.py


Reads an openapi spec on stdin and adds the calculated version to it,
then prints it on stdout.
"""
import sys
import json


def main():
    """Main entrypoint"""
    data = json.loads(sys.stdin.read())
    data["x-nhsd-apim"]["temporary"] = "true"
    sys.stdout.write(json.dumps(data, indent=2))
    sys.stdout.close()


if __name__ == "__main__":
    main()
