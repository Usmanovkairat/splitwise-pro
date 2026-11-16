"""Verify independent data using only disposable Compose test stacks."""
import json
from urllib.request import Request, urlopen
from uuid import uuid4


def groups(port, new_group=None):
    body = None if new_group is None else json.dumps({
        "name": new_group, "currency": "KZT", "description": "CI isolation fixture",
    }).encode()
    request = Request(
        f"http://127.0.0.1:{port}/api/groups",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    with urlopen(request, timeout=10) as response:
        return json.load(response)


def main():
    dev_name = f"dev-{uuid4()}"
    prod_name = f"prod-{uuid4()}"
    assert groups(8000, dev_name)["name"] == dev_name
    assert groups(8001, prod_name)["name"] == prod_name
    dev_names = {row["name"] for row in groups(8000)}
    prod_names = {row["name"] for row in groups(8001)}
    assert dev_name in dev_names and dev_name not in prod_names
    assert prod_name in prod_names and prod_name not in dev_names
    print("Development and production-like PostgreSQL ledgers are isolated")


if __name__ == "__main__":
    main()
