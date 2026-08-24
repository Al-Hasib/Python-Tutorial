"""
Asynchronous Programming

Async programming lets a single thread handle many I/O-bound tasks
concurrently by cooperatively switching between them whenever one is waiting
(e.g. for a network response). Instead of relying on OS threads or processes,
Python's asyncio uses an event loop that runs one coroutine at a time,
pausing it at each `await` point and resuming another that is ready to make
progress. This gives you concurrency with far less overhead than threads,
which makes it especially well suited to high-volume I/O-bound work like web
servers and network clients.

This file covers:
- async def and await
- The event loop and asyncio.run
- asyncio.sleep for simulating non-blocking waits
- Running multiple coroutines concurrently with asyncio.gather
- Why async helps for I/O-bound concurrency
- A brief contrast with threading and multiprocessing
"""

import asyncio
import time

# ---------------------------------------------------------------------------
# 1. async def and await
# ---------------------------------------------------------------------------
# `async def` defines a coroutine function -- calling it returns a coroutine
# object, not a result. `await` pauses the coroutine until the awaited thing
# (another coroutine, or an awaitable) completes, yielding control back to
# the event loop so other work can run in the meantime.

async def say_hello(name, delay):
    print(f"  {name}: starting, will wait {delay}s")
    await asyncio.sleep(delay)  # non-blocking wait -- other coroutines can run now
    print(f"  {name}: done waiting")
    return f"{name} finished"


# ---------------------------------------------------------------------------
# 2. The event loop and asyncio.run
# ---------------------------------------------------------------------------
# asyncio.run() creates an event loop, runs the given coroutine to completion,
# and cleans up the loop afterward. It is the standard entry point for a
# top-level async program.

print("Running a single coroutine with asyncio.run:")
result = asyncio.run(say_hello("Solo", 0.01))
print("  Result:", result)

# ---------------------------------------------------------------------------
# 3. Running multiple coroutines concurrently with asyncio.gather
# ---------------------------------------------------------------------------
# asyncio.gather schedules several coroutines to run concurrently on the same
# event loop/thread. While one is awaiting (e.g. asyncio.sleep), the loop can
# run another -- so the total time is close to the LONGEST individual wait,
# not the SUM of all waits.

async def run_concurrently():
    start = time.perf_counter()
    results = await asyncio.gather(
        say_hello("Alice", 0.03),
        say_hello("Bob", 0.02),
        say_hello("Carol", 0.01),
    )
    elapsed = time.perf_counter() - start
    return results, elapsed


print("\nRunning three coroutines concurrently with asyncio.gather:")
results, elapsed = asyncio.run(run_concurrently())
print("  Results:", results)
print(f"  Elapsed time: {elapsed:.4f}s (close to the longest single delay, ~0.03s)")


# For comparison, running them sequentially (one after another) with await:
async def run_sequentially():
    start = time.perf_counter()
    r1 = await say_hello("Dan", 0.03)
    r2 = await say_hello("Eve", 0.02)
    r3 = await say_hello("Frank", 0.01)
    elapsed = time.perf_counter() - start
    return [r1, r2, r3], elapsed


print("\nRunning the same three delays sequentially (await one at a time):")
seq_results, seq_elapsed = asyncio.run(run_sequentially())
print("  Results:", seq_results)
print(f"  Elapsed time: {seq_elapsed:.4f}s (close to the SUM of delays, ~0.06s)")

# ---------------------------------------------------------------------------
# 4. Why async helps for I/O-bound concurrency
# ---------------------------------------------------------------------------
# When a coroutine awaits I/O (a sleep standing in for a network call, a
# database query, a file read), it hands control back to the event loop
# instead of blocking the whole program. The loop then runs other coroutines
# that are ready to make progress. This lets a single thread juggle thousands
# of concurrent I/O-bound tasks (e.g. web requests) with very low overhead --
# no extra threads or processes are needed just to "wait".

async def fetch_data(source, delay):
    """Stands in for an I/O operation like an HTTP request or DB query."""
    await asyncio.sleep(delay)
    return f"data from {source}"


async def fetch_many():
    sources = [("server-A", 0.02), ("server-B", 0.015), ("server-C", 0.01)]
    tasks = [fetch_data(name, delay) for name, delay in sources]
    return await asyncio.gather(*tasks)


print("\nSimulating concurrent 'network calls' with asyncio.gather:")
fetched = asyncio.run(fetch_many())
for item in fetched:
    print("  ->", item)

# ---------------------------------------------------------------------------
# 5. Contrast with threading and multiprocessing
# ---------------------------------------------------------------------------
print("\nasyncio vs threading vs multiprocessing:")
print("  - asyncio:        one thread, cooperative multitasking via await points.")
print("                    Best for MANY lightweight I/O-bound tasks (low overhead,")
print("                    no locks needed since only one coroutine runs at a time).")
print("  - threading:      multiple OS threads, preemptively switched by the OS.")
print("                    Good for I/O-bound work too, but needs locks to protect")
print("                    shared state, and has more overhead per task than asyncio.")
print("  - multiprocessing: multiple OS processes, true parallel execution.")
print("                    Best for CPU-bound work; highest overhead of the three.")
print("  In short: asyncio scales to many concurrent I/O waits cheaply, but code must")
print("  be written with async/await throughout (or wrapped) to take advantage of it.")

# Key takeaways:
# - `async def` defines a coroutine; `await` pauses it at a suspension point,
#   letting the event loop run other coroutines in the meantime.
# - asyncio.run() creates the event loop, runs your top-level coroutine, and
#   cleans up -- it is the standard entry point for an async program.
# - asyncio.gather runs multiple coroutines concurrently; total time approaches
#   the longest single wait rather than the sum of all waits.
# - asyncio shines for I/O-bound concurrency with many tasks, using a single
#   thread and very little overhead compared to threads or processes.
# - Choose asyncio for many concurrent I/O waits, threading for simpler I/O
#   concurrency with shared memory, and multiprocessing for CPU-bound parallelism.
