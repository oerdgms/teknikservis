import sys
import urllib.request
import server


def request_shutdown():
    req = urllib.request.Request(
        "http://127.0.0.1:8972/api/shutdown",
        data=b"{}",
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            return 200 <= response.status < 300
    except Exception:
        return False


if __name__ == "__main__":
    if "--shutdown" in sys.argv:
        request_shutdown()
        raise SystemExit(0)
    server.main()
