import os
from typing import NotRequired, TypedDict

import pymunge
import requests

nqstat_stat = TypedDict(
    "nqstat_stat",
    {
        "Job_ID": str,
        "Job_Name": str,
        "Job_Owner": str,
        "job_state": str,
        "queue": str,
        "Resource_List.jobfs": str,
        "Resource_List.mem": str,
        "Resource_List.ncpus": str,
        "Resource_List.storage": str,
        "Resource_List.walltime": str,
        "resources_used.cput": NotRequired[str],
        "resources_used.jobfs": NotRequired[str],
        "resources_used.mem": NotRequired[str],
        "resources_used.ncpus": NotRequired[str],
        "resources_used.walltime": NotRequired[str],
    },
)
nqstat_result = TypedDict(
    "nqstat_result", {"status": int, "project": str, "qstat": list[nqstat_stat]}
)


def nqstat(
    *, project: str | None = None, user: str | None = None, queue: str | None = None
) -> nqstat_result:
    if project is None:
        project = os.environ["PROJECT"]

    url = "http://gadi-pbs-01.gadi.nci.org.au:8812/qstat"
    headers = {
        "Authorization": f"MUNGE {pymunge.encode().decode('utf-8')}",
        "Content-Type": "application/json",
    }
    data = {
        "project": project,
        "user": user,
        "queue": queue,
    }

    r = requests.get(url, headers=headers, params=data, timeout=10)
    r.raise_for_status()

    return r.json()
