"""Download the raw inputs for one yearly run.

    python3 -I pipeline/fetch.py <raw_dir>

- WID.world France files, pulled out of the 900 MB bulk zip with HTTP range
  requests (only ~10 MB actually travels). The zip's ETag / Last-Modified are
  saved in <raw_dir>/wid_vintage.json so a build records which vintage it used.
- Every independent cross-check source registered in pipeline/sources.

Exits with a non-zero status if anything fails; files are written to a
temporary name and renamed only when complete.
"""
import datetime
import io
import json
import os
import sys
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # -I drops the script dir
from sources import SOURCES  # noqa: E402

WID_ZIP = "https://wid.world/bulk_download/wid_all_data.zip"
WID_FILES = ["WID_data_FR.csv", "WID_metadata_FR.csv"]
TIMEOUT = 60
RETRIES = 4


def open_url(url, headers=None, method=None):
    """urlopen with a timeout and exponential-backoff retries."""
    for attempt in range(RETRIES):
        try:
            req = urllib.request.Request(url, headers=headers or {}, method=method)
            return urllib.request.urlopen(req, timeout=TIMEOUT)
        except (urllib.error.URLError, TimeoutError, ConnectionError) as err:
            if attempt == RETRIES - 1:
                raise
            wait = 2 ** attempt
            print(f"  retrying {url} in {wait}s ({err})")
            time.sleep(wait)


class HttpRangeFile(io.RawIOBase):
    """Seekable read-only view of a remote file, so zipfile can read its index.

    Every range request carries If-Range with the ETag seen at the start: if the
    file changes mid-download the server answers 200 instead of 206 and we stop,
    rather than silently mixing two vintages.
    """

    def __init__(self, url):
        self.url, self.pos = url, 0
        head = open_url(url, method="HEAD")
        self.size = int(head.headers["Content-Length"])
        self.etag = head.headers.get("ETag")
        self.last_modified = head.headers.get("Last-Modified")

    def seekable(self):
        return True

    def readable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, offset, whence=0):
        base = {0: 0, 1: self.pos, 2: self.size}[whence]
        self.pos = base + offset
        return self.pos

    def readinto(self, buf):
        if self.pos >= self.size:
            return 0
        end = min(self.pos + len(buf), self.size) - 1
        headers = {"Range": f"bytes={self.pos}-{end}"}
        if self.etag:
            headers["If-Range"] = self.etag
        with open_url(self.url, headers=headers) as resp:
            if resp.status != 206:
                raise RuntimeError(f"{self.url}: expected a partial response (206), got {resp.status}; the file may have changed")
            data = resp.read()
        if len(data) != end - self.pos + 1:
            raise RuntimeError(f"{self.url}: short read at byte {self.pos}")
        buf[: len(data)] = data
        self.pos += len(data)
        return len(data)


def write_atomic(path, data):
    part = path.with_name(path.name + ".part")
    part.write_bytes(data)
    os.replace(part, path)


def main(raw_dir):
    raw = Path(raw_dir)
    raw.mkdir(parents=True, exist_ok=True)
    remote = HttpRangeFile(WID_ZIP)
    archive = zipfile.ZipFile(io.BufferedReader(remote, buffer_size=1 << 20))
    for name in WID_FILES:
        write_atomic(raw / name, archive.read(name))
        print("wrote", raw / name)
    vintage = {"url": WID_ZIP, "etag": remote.etag, "last_modified": remote.last_modified,
               "fetched": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")}
    write_atomic(raw / "wid_vintage.json", json.dumps(vintage, indent=1).encode())

    failed = {}
    for name, module in SOURCES.items():
        try:
            errors = module.fetch(str(raw))
        except Exception as err:  # report every source, then fail
            errors = {"fetch": repr(err)}
        if errors:
            failed[name] = errors
            print(f"FAILED cross-check source {name}: {errors}")
        else:
            print("fetched cross-check source", name)
    if failed:
        sys.exit(f"{len(failed)} source(s) failed: {', '.join(failed)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
