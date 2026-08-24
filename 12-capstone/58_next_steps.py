"""
Next Steps: Where to Go After This Curriculum
================================================

Finishing a Python tutorial series is a milestone, not a finish line. This
file is less about executable logic and more about a roadmap: what to do
in the weeks and months after you close the last lesson, so the skills you
just built turn into real ability instead of fading away. It is organized
as a set of commented sections you can read top to bottom, plus a couple
of small runnable snippets (a practice checklist and a dict of
specialization paths) so the file still runs cleanly end to end.

There is no single "correct" path forward. The sections below lay out how
to keep practicing in general, then describe four common specialization
paths (Web Development, Data Science & ML, Automation & Scripting, and
DevOps & Systems) along with concrete tools to look at for each, and close
with advice on choosing a direction, building a portfolio, and finding
good learning resources.

This file covers:
- How to keep practicing after finishing a tutorial (projects, open
  source, reading code)
- Specialization path: Web Development
- Specialization path: Data Science & Machine Learning
- Specialization path: Automation & Scripting
- Specialization path: DevOps & Systems
- Picking a path, building a portfolio, and finding good resources
"""

# ---------------------------------------------------------------------------
# 1. How to keep practicing
# ---------------------------------------------------------------------------
# Reading is necessary but not sufficient -- fluency comes from writing a lot
# of code and reading a lot of other people's code. Concretely:
#
#   - Build small projects on a schedule. Aim for something you can finish
#     in a weekend: a habit tracker, a markdown-to-HTML converter, a simple
#     game, a personal budgeting tool. Finishing many small things teaches
#     more than starting one huge thing you never ship.
#   - Rebuild something that already exists (a to-do app, a URL shortener,
#     a tiny key-value store) without copying a tutorial. Hitting your own
#     design decisions is where the real learning happens.
#   - Contribute to open source. Start small: fix a typo in docs, add a
#     test, tackle an issue labeled "good first issue". You will learn how
#     real codebases are organized, how code review works, and how to read
#     unfamiliar code under time pressure.
#   - Read other people's code deliberately. Pick a well-regarded, modestly
#     sized open-source project in a domain you like and read through its
#     source, not just its README. Notice naming, structure, and how errors
#     are handled.
#   - Write tests for your own old projects. Going back to code you wrote
#     months ago with fresh eyes (and an eye for edge cases) is one of the
#     fastest ways to notice how your skills have grown.


def practice_checklist():
    """Return a simple checklist of practice habits as a list of strings.
    A tiny runnable example -- nothing fancy, just something to print."""
    return [
        "Ship one small project this month, start to finish.",
        "Read the source of one library you already depend on.",
        "Find one 'good first issue' in a project you use and open a PR.",
        "Revisit an old project and add tests or fix a rough edge.",
        "Write a short note explaining something you just learned.",
    ]


# ---------------------------------------------------------------------------
# 2. Specialization path: Web Development
# ---------------------------------------------------------------------------
# Building things people can use through a browser or an API.
#
#   - Frameworks: Flask (small, explicit, great for learning the basics of
#     routing/templates/requests), Django (batteries-included: ORM, admin
#     panel, auth, migrations -- good for larger apps), FastAPI (modern,
#     async-friendly, built around type hints and automatic API docs).
#   - Core skills: HTTP fundamentals, building REST APIs, templating,
#     working with a database (SQL basics plus an ORM), authentication and
#     sessions, and basic frontend enough to wire up a UI (HTML/CSS/JS).
#   - Deployment: containerizing an app, environment configuration, a
#     WSGI/ASGI server (gunicorn/uvicorn) behind a reverse proxy, and at
#     least one deployment target (a PaaS or a small VM) end to end.

# ---------------------------------------------------------------------------
# 3. Specialization path: Data Science & Machine Learning
# ---------------------------------------------------------------------------
# Working with data to find patterns, build models, and communicate results.
#
#   - Core libraries: numpy (arrays and numeric computing), pandas (tabular
#     data wrangling), matplotlib/seaborn (visualization), scikit-learn
#     (classical ML: regression, classification, clustering), pytorch (deep
#     learning, when you get there).
#   - Core skills: descriptive statistics and probability fundamentals,
#     cleaning messy real-world data, exploratory data analysis, and
#     evaluating models honestly (train/validation/test splits, avoiding
#     leakage and overfitting).
#   - Tools of the trade: Jupyter notebooks for exploration, plus learning
#     to move working notebook code into plain, tested Python modules once
#     an approach proves out.

# ---------------------------------------------------------------------------
# 4. Specialization path: Automation & Scripting
# ---------------------------------------------------------------------------
# Using Python to remove repetitive manual work.
#
#   - Task automation: scripts that rename/organize files, talk to APIs on
#     a schedule, generate reports, or glue together other tools -- often
#     the highest-leverage, most immediately useful Python you can write.
#   - Web scraping: BeautifulSoup for parsing static HTML, Selenium (or a
#     similar browser-automation tool) when a site needs real interaction
#     or renders content with JavaScript. Always check a site's terms of
#     use and robots.txt before scraping it.
#   - Building CLI tools: argparse (standard library, no dependencies) for
#     straightforward command-line interfaces; click for richer, more
#     ergonomic CLIs with less boilerplate as tools grow.

# ---------------------------------------------------------------------------
# 5. Specialization path: DevOps & Systems
# ---------------------------------------------------------------------------
# Building and operating the infrastructure other software runs on.
#
#   - Containers: Docker for packaging an app with its dependencies into a
#     reproducible image; understanding images, containers, volumes, and
#     basic networking.
#   - CI/CD: automated pipelines (build, test, deploy) triggered on every
#     commit or pull request, so humans stop doing deployments by hand.
#   - Cloud SDKs: e.g. boto3 for AWS, or the equivalent SDK for whichever
#     cloud you use, to provision and manage infrastructure from code
#     instead of only clicking through a console.
#   - Core skills: Linux command-line comfort, basic networking concepts,
#     logging/monitoring, and infrastructure-as-code (treating your
#     infrastructure configuration as version-controlled code).


def specialization_paths():
    """Return a dict mapping each specialization path to a short list of
    representative tools/topics to look into next."""
    return {
        "Web Development": ["Flask", "Django", "FastAPI", "REST APIs", "Deployment"],
        "Data Science & ML": ["numpy", "pandas", "scikit-learn", "pytorch", "Jupyter"],
        "Automation & Scripting": ["argparse", "click", "BeautifulSoup", "Selenium"],
        "DevOps & Systems": ["Docker", "CI/CD pipelines", "boto3", "Infrastructure as code"],
    }


# ---------------------------------------------------------------------------
# 6. Picking a path, building a portfolio, and finding resources
# ---------------------------------------------------------------------------
# Picking a path:
#   - You do not have to choose forever -- pick the path that matches what
#     you want to build right now, and let curiosity pull you into others
#     later. Most experienced developers end up knowing a bit of all four.
#   - A good filter: what kind of finished thing excites you? A website,
#     an insight from data, a script that saves you an hour a week, or a
#     system that keeps other software running? That answer points at a
#     path faster than any amount of research does.
#
# Building a portfolio:
#   - Two or three complete, working projects beat ten half-finished ones.
#     "Complete" means it has a README, runs from a clean checkout, and
#     handles at least the obvious error cases.
#   - Put projects in version control from day one (even solo ones) and
#     write commit messages as if someone else will read them, because
#     eventually someone -- including future you -- will.
#   - Pick projects that show a range: one that talks to a database or
#     API, one with some kind of algorithmic logic, one with tests.
#
# Finding good resources:
#   - Official documentation is almost always the most accurate and
#     up-to-date source -- get comfortable reading it directly instead of
#     only relying on secondhand tutorials.
#   - Look for community hubs built around real-world, example-driven
#     Python content (the kind of site that walks through practical
#     projects and idiomatic style rather than just syntax).
#   - Package/library documentation sites and their own tutorials are
#     usually better than random blog posts once you have the basics down.
#   - Local or online user groups and meetups are a good way to see how
#     other people actually use the language day to day.


if __name__ == "__main__":
    print("=== Practice Checklist ===")
    for item in practice_checklist():
        print("  [ ]", item)
    print()

    print("=== Specialization Paths ===")
    for path, tools in specialization_paths().items():
        print("  {}:".format(path))
        for tool in tools:
            print("    -", tool)
    print()

    print("Pick one path, build something real with it, and keep going.")


# Key takeaways:
# - Tutorials teach syntax; projects, open source, and reading real code
#   teach the judgment that makes you actually productive.
# - Web development, data science/ML, automation/scripting, and DevOps are
#   four common (and overlapping) directions to specialize in -- pick one
#   based on what kind of finished thing excites you.
# - A small number of complete, well-documented projects is a stronger
#   portfolio than many unfinished ones.
# - Official docs and example-driven community resources are worth trusting
#   more than random secondhand tutorials once you have the fundamentals.
# - This is the start of the next phase of learning, not the end of it --
#   keep building.
