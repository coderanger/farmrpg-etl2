import numpy as np


def simulate_drops(
    items: dict[int, int],
    batch_size: int = 1_000_000,
    batch_count: int = 100,
    seed: int | None = None,
) -> dict[int, int]:
    item_ids = list(items.keys())
    weights = list(items.values())
    drops = {i: 0 for i in item_ids}

    weights_ary = np.repeat(np.array([weights], dtype=np.int16), batch_size, axis=0)
    rng = np.random.default_rng(seed=seed)

    # Preallocate these arrays for speed.
    random_ary = np.empty((batch_size, len(items)), dtype=np.float64)
    argmin_ary = np.empty((batch_size,), dtype=np.int64)

    for _ in range(batch_count):
        rng.random(out=random_ary)
        random_ary *= weights_ary
        np.argmin(random_ary, axis=1, out=argmin_ary)
        unique, counts = np.unique(argmin_ary, return_counts=True)
        for index, count in zip(unique, counts):
            drops[item_ids[index]] += count

    return drops, batch_size * batch_count
