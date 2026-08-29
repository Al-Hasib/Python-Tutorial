"""
Concurrency: Threading

Threading lets a Python program run multiple sequences of instructions
seemingly "at once" within a single process. In CPython, however, the Global
Interpreter Lock (GIL) ensures only one thread executes Python bytecode at a
time, which limits threading's usefulness for CPU-bound work but still makes
it valuable for I/O-bound work (network calls, file access, waiting on
external resources) where threads spend most of their time waiting rather
than computing. This file demonstrates creating threads, why the GIL matters,
and how to protect shared state with a Lock.

This file covers:
- The threading module: creating, starting, and joining threads
- The GIL: what it is and why threading doesn't speed up CPU-bound work
- When threading DOES help: I/O-bound work
- A race-condition demo without a Lock
- Fixing the race condition with threading.Lock
"""

import threading
import time

# ---------------------------------------------------------------------------
# 1. Creating, starting, and joining threads
# ---------------------------------------------------------------------------

def say_hello(name, delay):
    time.sleep(delay)  # simulate a small bit of work / waiting
    print(f"  Hello from thread for {name} (after {delay}s)")


print("Creating and running two threads:")
t1 = threading.Thread(target=say_hello, args=("Alice", 0.02))
t2 = threading.Thread(target=say_hello, args=("Bob", 0.01))

t1.start()  # begins running concurrently
t2.start()

t1.join()  # wait for t1 to finish before continuing
t2.join()  # wait for t2 to finish before continuing
print("Both threads finished.")

# ---------------------------------------------------------------------------
# 2. The GIL: what it is and why it limits CPU-bound threading
# ---------------------------------------------------------------------------
# The Global Interpreter Lock (GIL) is a mutex in CPython (the standard
# Python implementation) that allows only ONE thread to execute Python
# bytecode at any given instant, even on a multi-core machine. Threads take
# turns holding the GIL, switching periodically. This means that for
# CPU-bound work (pure computation), using threads does NOT give you a
# speedup -- the work is still serialized by the GIL, plus you pay the
# overhead of thread switching.

def cpu_bound_work(n):
    """A deliberately simple CPU-bound task: count up to n."""
    total = 0
    for i in range(n):
        total += i
    return total


N = 2_000_000

print("\nGIL demo: CPU-bound work, single-threaded vs threaded")
start = time.perf_counter()
cpu_bound_work(N)
cpu_bound_work(N)
single_thread_time = time.perf_counter() - start
print(f"  Sequential (no threads): {single_thread_time:.4f}s")

start = time.perf_counter()
threads = [threading.Thread(target=cpu_bound_work, args=(N,)) for _ in range(2)]
for t in threads:
    t.start()
for t in threads:
    t.join()
threaded_time = time.perf_counter() - start
print(f"  Two threads (CPU-bound):  {threaded_time:.4f}s")
print("  -> Threading rarely speeds up CPU-bound work in CPython due to the GIL.")
print("     (Timing can vary by machine, but there is no reliable ~2x speedup here.)")

# ---------------------------------------------------------------------------
# 3. When threading DOES help: I/O-bound work
# ---------------------------------------------------------------------------
# While one thread is BLOCKED waiting on I/O (network, disk, time.sleep), it
# releases the GIL so other threads can run. This makes threading effective
# for I/O-bound work, where the program spends most of its time waiting.

def io_bound_work(label, delay):
    time.sleep(delay)  # stands in for a network request, file read, etc.
    return f"{label} done"


print("\nI/O-bound demo: sequential vs threaded")
delays = [0.03, 0.03, 0.03]

start = time.perf_counter()
for i, d in enumerate(delays):
    io_bound_work(f"task-{i}", d)
sequential_io_time = time.perf_counter() - start
print(f"  Sequential I/O-bound: {sequential_io_time:.4f}s")

start = time.perf_counter()
io_threads = [
    threading.Thread(target=io_bound_work, args=(f"task-{i}", d))
    for i, d in enumerate(delays)
]
for t in io_threads:
    t.start()
for t in io_threads:
    t.join()
threaded_io_time = time.perf_counter() - start
print(f"  Threaded I/O-bound:   {threaded_io_time:.4f}s")
print("  -> Threading helps here because threads overlap their WAITING time.")

# ---------------------------------------------------------------------------
# 4. Race condition demo (without a Lock)
# ---------------------------------------------------------------------------
# When multiple threads read-modify-write shared state without coordination,
# updates can be lost. Incrementing a shared counter is a classic example.

counter_unsafe = 0


def increment_unsafe(times):
    global counter_unsafe
    for _ in range(times):
        # This looks atomic but is NOT: read, add 1, write back -- another
        # thread can interleave between these steps.
        current = counter_unsafe
        current += 1
        counter_unsafe = current


ITERATIONS = 50_000
print("\nRace condition demo (no Lock):")
threads = [threading.Thread(target=increment_unsafe, args=(ITERATIONS,)) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()

expected = 4 * ITERATIONS
print(f"  Expected counter value: {expected}")
print(f"  Actual counter value:   {counter_unsafe}")
if counter_unsafe != expected:
    print("  -> Lost updates occurred due to the unprotected race condition!")
else:
    print("  -> (No lost updates this run -- races are timing-dependent and may not"
          " always reproduce, but the code above is still unsafe.)")

# ---------------------------------------------------------------------------
# 5. Fixing the race condition with threading.Lock
# ---------------------------------------------------------------------------
# A Lock ensures only one thread at a time can execute the critical section
# (the read-modify-write sequence), making the increment effectively atomic.

counter_safe = 0
counter_lock = threading.Lock()


def increment_safe(times):
    global counter_safe
    for _ in range(times):
        with counter_lock:  # acquires the lock, releases automatically on exit
            current = counter_safe
            current += 1
            counter_safe = current


print("\nFixed version using threading.Lock:")
threads = [threading.Thread(target=increment_safe, args=(ITERATIONS,)) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"  Expected counter value: {expected}")
print(f"  Actual counter value:   {counter_safe}")
print("  -> With the Lock, the counter always matches the expected value.")

# Key takeaways:
# - threading.Thread(target=...).start()/.join() runs functions concurrently
#   within one process and waits for them to complete.
# - The GIL lets only one thread execute Python bytecode at a time in CPython,
#   so threading does not speed up pure CPU-bound work.
# - Threads release the GIL while blocked on I/O, so threading is effective
#   for I/O-bound work (network calls, file access, sleeping).
# - Unsynchronized access to shared mutable state from multiple threads causes
#   race conditions and lost updates.
# - threading.Lock (used as a context manager) protects a critical section so
#   only one thread can execute it at a time, fixing the race condition.
