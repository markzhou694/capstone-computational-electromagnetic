"""Editable wall-time reporting, console progress and FDTD FLOP estimates."""

from time import perf_counter
import yee_solver


def print_progress(done, total, label="Run"):
    """Print a 25-character bar at roughly 5-percent intervals."""
    stride = max(1, total // 20)
    if done not in (0, total) and done % stride:
        return
    filled = int(25 * done / total)
    bar = "#" * filled + "-" * (25 - filled)
    print(f"\r{label}: [{bar}] {100 * done / total:5.1f}% ({done}/{total})",
          end="\n" if done == total else "", flush=True)


def estimate_fdtd_flops(cells, steps, pml=False, aligned_outputs=1):
    """Estimate core array arithmetic, NOT measured hardware FLOPs.

    Count each scalar +, -, *, / and unary negation as one operation.
    Excludes source evaluation, initialization/PML coefficient construction,
    memory copies, boundary assignments, Python, callbacks, I/O and plotting.
    E/H sizes are sums of their three native Yee component sizes.
    Curl costs 5 operations per computed component value. Charge costs 10
    per interior node. PEC updates cost 2/H and 3/E; PML costs 12/E or H
    including drive construction (the implementation updates the full box).
    Each time-aligned H output costs 7/H (PEC) or 19/H (PML).
    Edit these counts if the solver equations or implementation change.
    """
    nx, ny, nz = map(int, cells)
    E = nx*(ny+1)*(nz+1) + (nx+1)*ny*(nz+1) + (nx+1)*(ny+1)*nz
    H = (nx+1)*ny*nz + nx*(ny+1)*nz + nx*ny*(nz+1)
    E_interior = nx*(ny-1)*(nz-1) + (nx-1)*ny*(nz-1) + (nx-1)*(ny-1)*nz
    nodes = (nx-1)*(ny-1)*(nz-1)
    curls = 5 * (H + E_interior)
    updates = 12*(E+H) if pml else 3*E + 2*H
    per_step = curls + updates + 10*nodes
    alignment = (19 if pml else 7) * H * aligned_outputs
    return int(steps * per_step + alignment)


def timed_call(label, function, *args, **kwargs):
    """Run a function, print elapsed wall seconds, return (value, seconds)."""
    start = perf_counter()
    value = function(*args, **kwargs)
    seconds = perf_counter() - start
    print(f"{label}: {seconds:.3f} s", flush=True)
    return value, seconds


def timed_solve(label, **settings):
    """Solve with progress; attach timing/FLOP estimates to the result.

    Wall time includes initialization, source evaluation and on_frame work
    (sampling, disk I/O or error comparison). It is not pure kernel time.
    FLOPs cover core updates and H alignment only, so no hardware GFLOP/s
    claim is made from these inclusive wall times.
    """
    settings = settings.copy()
    settings['on_progress'] = lambda done, total: print_progress(done, total, label)
    result, seconds = timed_call(label + " solve + callbacks", yee_solver.solve, **settings)
    steps = result['steps']
    stride = settings.get('frame_every', 1)
    outputs = 1  # The returned final H is always aligned.
    if settings.get('on_frame') is not None:
        outputs += (steps + stride - 1) // stride
    flops = estimate_fdtd_flops(result['cells'], steps, bool(settings.get('pml_cells', 0)), outputs)
    result['performance'] = dict(wall_seconds=seconds, estimated_core_flops=flops)
    print(f"{label}: estimated core FLOPs = {flops:,} ({flops/1e9:.3f} GFLOP)")
    return result
