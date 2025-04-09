import os
from typing import TypedDict

import pymunge
import requests

nci_account_stakeholder = TypedDict(
    "nci_account_stakeholder",
    {"name": str, "grant": float, "balance": float, "used": float},
)
nci_account_user = TypedDict(
    "nci_account_user",
    {
        "usage": float,
        "aquired": float,
        "total_released": float,
        "total_reserved": float,
    },
)
nci_account_usage = TypedDict(
    "nci_account_usage",
    {
        "total_grant": float,
        "running_job_reserved": float,
        "used": float,
        "stakeholders": dict[str, nci_account_stakeholder],
        "users": dict[str, nci_account_user],
        "period": str,
    },
)
nci_account_storage_allocation = TypedDict(
    "nci_account_storage_allocation",
    {
        "db_id": int,
        "project": str,
        "filesytem": str,
        "funding_source": str,
        "block_allocation": float,
        "inode_allocation": int,
    },
)
nci_account_storage = TypedDict(
    "nci_account_storage",
    {
        "block_usage": int,
        "inode_usage": int,
        "allocations": list[nci_account_storage_allocation],
    },
)
nci_account_cloud = TypedDict(
    "nci_account_cloud", {"users": dict[str, float], "usage": float}
)
nci_account_result = TypedDict(
    "nci_account_result",
    {
        "status": int,
        "project": str,
        "usage": nci_account_usage,
        "storage": dict[str, nci_account_storage],
        "cloud": nci_account_cloud,
        "cloudstorage": nci_account_cloud,
    },
)


def nci_account(project: str | None = None) -> nci_account_result:
    if project is None:
        project = os.environ["PROJECT"]

    url = f"http://gadi-pbs-01.gadi.nci.org.au:8811/v0/nciaccount/project/{project}"
    headers = {"Authorization": f"MUNGE {pymunge.encode().decode('utf-8')}"}

    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()

    return r.json()
