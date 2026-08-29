"""
Working with APIs
==================
A REST API (Representational State Transfer) lets programs talk to each
other over HTTP. A server exposes "endpoints" (URLs) that a client can
call to read or change data. Instead of clicking buttons on a web page,
your Python program sends HTTP requests and receives structured data
back, usually as JSON. Knowing how to call APIs is essential because
almost every modern service (weather, payments, social media, maps,
internal company tools) exposes its functionality this way.

This file covers:
- What a REST API is and how HTTP methods map to actions
- Common HTTP status codes and what they mean
- Using the third-party `requests` library (GET/POST, headers, params, json())
- A stdlib-only alternative using `urllib.request`
- Making the whole file safe to run with no internet and without `requests`
"""

# ---------------------------------------------------------------------------
# 1. What is a REST API?
# ---------------------------------------------------------------------------
# REST is a style of designing web APIs around "resources" (things), each
# identified by a URL, e.g. https://api.example.com/users/42
# Clients act on resources using standard HTTP methods:
#   GET    -> read a resource (should not change anything on the server)
#   POST   -> create a new resource (e.g. submit a new user)
#   PUT    -> replace/update an existing resource entirely
#   PATCH  -> partially update a resource (not always mentioned, but common)
#   DELETE -> remove a resource
#
# The server responds with:
#   - A status code (see below)
#   - Headers (metadata, e.g. Content-Type: application/json)
#   - A body, very often JSON text that we parse into Python dicts/lists

print("=== 1. REST API concepts ===")
print("GET    -> read data")
print("POST   -> create data")
print("PUT    -> replace/update data")
print("DELETE -> remove data")

# ---------------------------------------------------------------------------
# 2. HTTP status codes
# ---------------------------------------------------------------------------
# Status codes are grouped by their first digit:
#   2xx -> success            (200 OK, 201 Created, 204 No Content)
#   3xx -> redirection        (301 Moved Permanently, 304 Not Modified)
#   4xx -> client error       (400 Bad Request, 401 Unauthorized,
#                              403 Forbidden, 404 Not Found)
#   5xx -> server error       (500 Internal Server Error, 503 Unavailable)

print("\n=== 2. Common status codes ===")
status_meanings = {
    200: "OK - request succeeded",
    201: "Created - a new resource was created",
    204: "No Content - success, nothing to return",
    400: "Bad Request - the request was malformed",
    401: "Unauthorized - authentication required",
    403: "Forbidden - you don't have permission",
    404: "Not Found - resource does not exist",
    500: "Internal Server Error - something broke on the server",
}
for code, meaning in status_meanings.items():
    print(f"{code}: {meaning}")

# ---------------------------------------------------------------------------
# 3. Using the third-party `requests` library
# ---------------------------------------------------------------------------
# `requests` is not part of the standard library; it must be installed via
# `pip install requests`. It provides a very friendly API:
#
#   response = requests.get(url, params={...}, headers={...}, timeout=5)
#   response.status_code   -> integer status code, e.g. 200
#   response.json()        -> parses the JSON body into Python data
#   response.text          -> raw text body
#   response.headers       -> response headers (dict-like)
#
#   requests.post(url, json={...})   -> sends a JSON body, e.g. to create data
#   requests.put(url, json={...})    -> replaces a resource
#   requests.delete(url)             -> deletes a resource
#
# We guard the import so this script still runs if `requests` is missing.

print("\n=== 3. The requests library ===")
try:
    import requests
    HAS_REQUESTS = True
    print("requests is installed - version:", requests.__version__)
except ImportError:
    HAS_REQUESTS = False
    print("NOTE: 'requests' is not installed. Skipping the live requests demo.")
    print("Install it with: pip install requests")

if HAS_REQUESTS:
    try:
        # GET request with query parameters and custom headers.
        # httpbin.org/get simply echoes back what we sent, great for learning.
        response = requests.get(
            "https://httpbin.org/get",
            params={"course": "python-tutorial", "topic": "apis"},
            headers={"User-Agent": "python-tutorial-demo"},
            timeout=5,
        )
        print("Status code:", response.status_code)
        if response.status_code == 200:
            data = response.json()  # parse JSON body into a Python dict
            print("Echoed query params:", data.get("args"))
        else:
            print("Request did not succeed as expected.")

        # A conceptual (not executed against a real endpoint) look at POST/PUT/DELETE:
        # requests.post(url, json={"name": "Alice"})   -> create
        # requests.put(url, json={"name": "Alice B."}) -> replace
        # requests.delete(url)                         -> delete
        print("POST/PUT/DELETE follow the same pattern, just with a different")
        print("method function and usually a 'json=' payload for the body.")
    except requests.exceptions.RequestException as exc:
        # Covers connection errors, timeouts, DNS failures, etc.
        print("Could not reach the network (no internet?). Details:", exc)

# ---------------------------------------------------------------------------
# 4. Stdlib-only alternative: urllib.request
# ---------------------------------------------------------------------------
# If you cannot install third-party packages, Python's standard library
# can still make HTTP requests using `urllib.request`. It is more verbose
# than `requests` but requires nothing extra to install.

print("\n=== 4. urllib.request (stdlib-only alternative) ===")
import json
import urllib.request
import urllib.error

url = "https://api.github.com"

try:
    req = urllib.request.Request(url, headers={"User-Agent": "python-tutorial-demo"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        status_code = resp.status
        body_text = resp.read().decode("utf-8")
        parsed = json.loads(body_text)  # manual JSON parsing (requests does this for you)
        print("Status code:", status_code)
        print("Sample key from GitHub API root:", "current_user_url ->", parsed.get("current_user_url"))
except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
    # No internet access, DNS failure, blocked network, etc. Fail gracefully.
    print("Could not reach the network for the urllib demo (no internet?).")
    print("This is expected in offline environments. Details:", exc)

# ---------------------------------------------------------------------------
# 5. Choosing between requests and urllib
# ---------------------------------------------------------------------------
print("\n=== 5. requests vs urllib ===")
print("requests: friendlier API, automatic JSON handling, third-party install.")
print("urllib.request: always available (stdlib), more boilerplate, no install.")

# Key takeaways:
# - REST APIs expose resources via URLs and standard HTTP methods
#   (GET=read, POST=create, PUT=update, DELETE=remove).
# - Status codes tell you the outcome: 2xx success, 4xx client error,
#   5xx server error.
# - `requests` is the popular third-party library: requests.get/post/put/delete,
#   with params=, headers=, json=, and response.status_code / response.json().
# - `urllib.request` from the standard library can do the same job without
#   installing anything, at the cost of more manual code.
# - Always guard network calls and optional imports with try/except so your
#   scripts stay usable offline or without extra dependencies installed.
