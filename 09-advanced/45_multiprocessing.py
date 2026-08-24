"""
Concurrency: Multiprocessing

Multiprocessing runs code in separate OS processes instead of threads within
one process. Because each process has its own Python interpreter and memory
space, each has its OWN Global Interpreter Lock (GIL) -- so multiprocessing
can achieve true parallelism for CPU-bound work across multiple CPU cores,
something threading cannot do in CPython. The cost is higher overhead: each
process needs its own memory, starting one is slower than starting a thread,
and passing data between processes requires serialization (pickling).

This file covers:
- The multiprocessing module: creating, starting, and joining processes
- Pool.map for parallel work across multiple worker processes
- Why multiprocessing bypasses the GIL (separate processes, separate interpreters)
- When to use multiprocessing vs threading vs asyncio
- Overhead considerations
- IMPORTANT (Windows): guarding launch code with `if __name__ == "__main__":`
  and keeping worker functions at module level so they can be pickled
"""

import multiprocessing
import time

# ---------------------------------------------------------------------------
# Worker functions MUST be defined at module level (not nested, not lambda)
# so that they are picklable -- multiprocessing needs to send the function
# reference to child processes, which on Windows re-import this module.
# ---------------------------------------------------------------------------

def cpu_bound_work(n):
    """A deliberately simple CPU-bound task: sum of squares up to n."""
    total = 0
    for i in range(n):
        total += i * i
    return total


def greet_process(name, delay):
    time.sleep(delay)
    print(f"  Hello from process for {name} (after {delay}s)")


def square(x):
    """Simple picklable worker used with Pool.map."""
    return x * x


# ---------------------------------------------------------------------------
# All process-launching code lives inside this guard. On Windows, child
# processes re-import this module, so code that starts processes must not
# run at import time -- otherwise it would recursively spawn more processes.
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    # -----------------------------------------------------------------------
    # 1. Creating, starting, and joining processes
    # -----------------------------------------------------------------------
    print("Creating and running two processes:")
    p1 = multiprocessing.Process(target=greet_process, args=("Alice", 0.02))
    p2 = multiprocessing.Process(target=greet_process, args=("Bob", 0.01))

    p1.start()
    p2.start()

    p1.join()  # wait for p1 to finish
    p2.join()  # wait for p2 to finish
    print("Both processes finished.")

    # -----------------------------------------------------------------------
    # 2. Pool.map for parallel work
    # -----------------------------------------------------------------------
    # A Pool manages a fixed group of worker processes and distributes work
    # from an iterable across them, collecting results in order.
    print("\nPool.map example:")
    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(square, [1, 2, 3, 4, 5, 6, 7, 8])
    print("  squares:", results)

    # -----------------------------------------------------------------------
    # 3. Why multiprocessing bypasses the GIL
    # -----------------------------------------------------------------------
    # Each process started by multiprocessing has its own Python interpreter
    # and its own GIL. Since they don't share the same GIL, they can each run
    # Python bytecode simultaneously on separate CPU cores -- true parallelism,
    # unlike threading where all threads share one GIL in one process.
    print("\nCPU-bound comparison: sequential vs multiprocessing")
    N = 3_000_000

    start = time.perf_counter()
    cpu_bound_work(N)
    cpu_bound_work(N)
    sequential_time = time.perf_counter() - start
    print(f"  Sequential (no processes): {sequential_time:.4f}s")

    start = time.perf_counter()
    with multiprocessing.Pool(processes=2) as pool:
        pool.map(cpu_bound_work, [N, N])
    parallel_time = time.perf_counter() - start
    print(f"  Two processes (parallel):  {parallel_time:.4f}s")
    print("  -> Unlike threading, multiprocessing CAN speed up CPU-bound work")
    print("     because each process has its own GIL and can use a separate core.")
    print("     (Actual speedup depends on CPU core count and process startup overhead.)")

    # -----------------------------------------------------------------------
    # 4. When to use multiprocessing vs threading vs asyncio
    # -----------------------------------------------------------------------
    print("\nWhen to use which concurrency tool:")
    print("  - threading:      I/O-bound work (network, disk, waiting) where you want")
    print("                    simple concurrency and shared memory between tasks.")
    print("  - multiprocessing: CPU-bound work (heavy computation) where you want true")
    print("                    parallel execution across multiple CPU cores.")
    print("  - asyncio:        High-volume I/O-bound work (many concurrent connections)")
    print("                    where you want low overhead and explicit control via")
    print("                    async/await, without the cost of threads or processes.")

    # -----------------------------------------------------------------------
    # 5. Overhead considerations
    # -----------------------------------------------------------------------
    print("\nOverhead considerations:")
    print("  - Starting a process is much slower than starting a thread (new")
    print("    interpreter, new memory space).")
    print("  - Data passed between processes must be pickled (serialized) and sent")
    print("    through inter-process communication -- this has a real cost for large")
    print("    or frequent data transfers.")
    print("  - For small or very fast tasks, the overhead of multiprocessing can")
    print("    outweigh its parallelism benefits -- always measure before committing.")
    print("  - Worker functions must be defined at module level (picklable), not as")
    print("    local closures or lambdas, especially for compatibility on Windows.")

# Key takeaways:
# - multiprocessing.Process / Pool run code in separate OS processes, each with
#   its own interpreter, memory space, and GIL.
# - Because each process has its own GIL, multiprocessing achieves true
#   parallelism for CPU-bound work, unlike threading in CPython.
# - Pool.map distributes an iterable of work across a fixed set of worker
#   processes and gathers the results in order.
# - Use threading for I/O-bound work, multiprocessing for CPU-bound work, and
#   asyncio for large-scale I/O-bound concurrency with low overhead.
# - On Windows, always guard process-launching code with
#   `if __name__ == "__main__":` and keep worker functions at module level so
#   they can be pickled and sent to child processes.
