"""
Introduction to Web Development
================================
A web framework helps you build applications that respond to HTTP
requests from browsers or other clients. At its core, a framework's job
is "routing" (deciding which piece of code should run for a given URL
and HTTP method) and "request/response handling" (reading incoming data
and producing an outgoing response, often HTML, JSON, or a redirect).
Flask is one of the most popular lightweight Python web frameworks, and
learning its basic ideas transfers directly to almost every other web
framework you will encounter. Understanding routing is the single most
important concept for building any web backend.

This file covers:
- What a web framework does: routing and request/response
- A minimal conceptual Flask example (@app.route, app.run())
- Guarding the Flask import so the script runs even if Flask isn't installed
- A plain-Python simulation of routing (a dict-based router) that always runs
- A brief mention of FastAPI as a modern, async-friendly alternative
"""

# ---------------------------------------------------------------------------
# 1. What does a web framework do?
# ---------------------------------------------------------------------------
# When a browser visits a URL like http://example.com/hello, it sends an
# HTTP request to a server. A web framework's job is to:
#   1. ROUTING: match the incoming URL (and HTTP method) to a specific
#      Python function ("view" or "handler") that should handle it.
#   2. REQUEST: give that function easy access to the incoming data
#      (query parameters, form data, JSON body, headers, cookies).
#   3. RESPONSE: take whatever the function returns (a string, a dict,
#      a template) and turn it into a proper HTTP response with the
#      right status code and headers.
#
# Frameworks also typically add things like templating, sessions,
# middleware, and database integration, but routing + request/response
# handling is the essential core.

print("=== 1. Web framework core job ===")
print("Routing:  URL + method -> handler function")
print("Request:  handler reads incoming data (params, body, headers)")
print("Response: handler's return value -> HTTP response")

# ---------------------------------------------------------------------------
# 2. A minimal conceptual Flask example
# ---------------------------------------------------------------------------
# Flask is a third-party "micro" web framework. A tiny Flask app looks
# like this:
#
#   from flask import Flask
#   app = Flask(__name__)
#
#   @app.route("/")
#   def index():
#       return "Hello, World!"
#
#   @app.route("/greet/<name>")
#   def greet(name):
#       return f"Hello, {name}!"
#
#   if __name__ == "__main__":
#       app.run(debug=True)   # starts a local development web server
#
# `@app.route("/")` registers a route: when someone visits "/", Flask
# calls `index()` and sends its return value back as the HTTP response.
# `app.run()` starts a server that listens for real HTTP requests, which
# is why we do NOT call it in this educational script (it would block
# forever waiting for requests, and it requires the flask package).

print("\n=== 2. Flask example (guarded import) ===")
try:
    import flask
    from flask import Flask

    HAS_FLASK = True
    print("Flask is installed - version:", flask.__version__)

    app = Flask(__name__)

    @app.route("/")
    def index():
        return "Hello, World!"

    @app.route("/greet/<name>")
    def greet(name):
        return f"Hello, {name}!"

    print("Defined routes: '/' -> index(), '/greet/<name>' -> greet(name)")
    print("(app.run() is intentionally NOT called here - it would start a")
    print(" real server and block this script forever.)")

except ImportError:
    HAS_FLASK = False
    print("NOTE: 'flask' is not installed. Skipping the real Flask app.")
    print("Install it with: pip install flask")
    print("Showing an equivalent plain-Python routing simulation instead...")

# ---------------------------------------------------------------------------
# 3. Simulating routing in plain Python (always runs)
# ---------------------------------------------------------------------------
# Even without any framework, we can demonstrate the *core idea* of
# routing with nothing more than a dictionary mapping paths to functions.
# This is, in essence, what frameworks do under the hood (with a lot more
# features layered on top: pattern matching, HTTP methods, middleware...).

print("\n=== 3. Plain-Python routing simulation ===")


def handle_index():
    return "Hello, World!"


def handle_about():
    return "This is a tiny simulated web app."


def handle_not_found():
    return "404 Not Found"


# The "router": a dict mapping a URL path to the function that handles it.
routes = {
    "/": handle_index,
    "/about": handle_about,
}


def dispatch(path):
    """Simulate what a web framework does: look up the handler for a path
    and call it, or fall back to a 'not found' handler."""
    handler = routes.get(path, handle_not_found)
    return handler()


# Simulate a few incoming "requests" for different paths.
incoming_requests = ["/", "/about", "/missing-page"]
for path in incoming_requests:
    response_body = dispatch(path)
    print(f"GET {path!r} -> {response_body!r}")

# ---------------------------------------------------------------------------
# 4. Beyond Flask: FastAPI
# ---------------------------------------------------------------------------
# FastAPI is a more modern Python web framework built for high performance
# and great developer experience. Key differences from Flask:
#   - Native `async def` support, well suited to I/O-heavy workloads.
#   - Request/response validation is generated automatically from Python
#     type hints (using Pydantic models), e.g.:
#
#       from fastapi import FastAPI
#       app = FastAPI()
#
#       @app.get("/greet/{name}")
#       async def greet(name: str, loud: bool = False):
#           text = f"Hello, {name}!"
#           return {"message": text.upper() if loud else text}
#
#   - Automatic interactive API documentation (Swagger UI / ReDoc) is
#     generated for free from your route definitions and type hints.
# FastAPI is a great choice for building JSON APIs today, while Flask
# remains excellent for simplicity and for traditional server-rendered
# HTML sites.

print("\n=== 4. FastAPI (mentioned, not required) ===")
print("FastAPI: async-friendly, uses type hints for automatic validation")
print("and generates interactive API docs automatically. Great for JSON APIs.")

# Key takeaways:
# - A web framework's core job is routing (URL+method -> handler) plus
#   handling the request and producing a response.
# - Flask uses @app.route(...) decorators to register handlers, and
#   app.run() starts the development server.
# - You can simulate the essential idea of routing with nothing more than
#   a dictionary mapping paths to functions, no framework required.
# - Always guard optional framework imports with try/except so tutorial
#   and demo scripts keep running even without the package installed.
# - FastAPI is a modern alternative offering async support and automatic
#   validation/docs generation from Python type hints.
