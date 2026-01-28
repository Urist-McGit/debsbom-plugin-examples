# Copyright (C) 2025 Siemens
#
# SPDX-License-Identifier: MIT

from debsbom.download.plugin import ChecksumAlgo, Package, RemoteFile, ResolveError, Resolver
import logging
from requests import Session

SNAPSHOT_DOMAIN = "https://snapshot.debian.org"

logger = logging.getLogger(__name__)


class SimpleResolveError(ResolveError):
    """Error type for custom errors."""

    pass


def setup_resolver(session: Session):
    return SimpleUpstreamResolver(session)


class SimpleUpstreamResolver(Resolver):
    """
    A simple resolver for snapshot.debian.org.

    This is more or less a reimplementation of the resolver provided by debsbom already, but
    simpler (and incomplete!) to keep the code minimal.
    """

    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def resolve(self, p: Package) -> list[RemoteFile]:
        files = []
        if p.is_source():
            api = f"{SNAPSHOT_DOMAIN}/mr/package/{p.name}/{p.version}/srcfiles?fileinfo=1"
            try:
                r = self.session.get(api)
                data = r.json()
            except Exception as e:
                raise SimpleResolveError(e)
            fileinfo = data.get("fileinfo")
            for s in data.get("result"):
                hash_val = s["hash"]
                for res in fileinfo[hash_val]:
                    rf = RemoteFile(
                        checksums={ChecksumAlgo.SHA1SUM: hash_val},
                        filename=res["name"],
                        size=res["size"],
                        archive_name=res["archive_name"],
                        downloadurl=f"{SNAPSHOT_DOMAIN}/file/{hash_val}/{res['name']}",
                    )
                    files.append(rf)
        else:
            api = f"{SNAPSHOT_DOMAIN}/mr/binary/{p.name}/{p.version}/binfiles?fileinfo=1"
            try:
                r = self.session.get(api)
                data = r.json()
            except Exception as e:
                raise SimpleResolveError(e)
            fileinfo = data.get("fileinfo")
            for f in data.get("result"):
                if f["architecture"] != p.architecture:
                    continue
                hash_val = f["hash"]
                for res in fileinfo[hash_val]:
                    rf = RemoteFile(
                        checksums={ChecksumAlgo.SHA1SUM: hash_val},
                        filename=res["name"],
                        size=res["size"],
                        archive_name=res["archive_name"],
                        downloadurl=f"{SNAPSHOT_DOMAIN}/file/{hash_val}/{res['name']}",
                    )
                    files.append(rf)
        return files
