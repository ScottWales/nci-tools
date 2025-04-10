import sys
import os
import grp
from pathlib import Path

sys.path.append('/opt/nci/lquota')
from lustre import LustreFilesystem

def lquota() -> list[dict]:
    result = []

    for fs in [Path('/scratch'), Path('/g/data')]:
        lfs = LustreFilesystem(str(fs))

        for gid in os.getgroups():
            gname = grp.getgrgid(gid).gr_name

            if (fs/gname).is_dir():
                try:
                    r = lfs.get_group_quota(gname)
                    r['fs'] = str(fs)
                    if r['block_hard_limit'] > 0:
                        result.append(r)
                except:
                    result.append({'fs': str(fs), 'group': gname})
                try:
                    r = lfs.get_project_quota(gname)
                    r['fs'] = str(fs)
                    if r['block_hard_limit'] > 0:
                        result.append(r)
                except:
                    result.append({'fs': str(fs), 'project': gname})

    return result
