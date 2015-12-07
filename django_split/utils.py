def overlapping(interval_a, interval_b):
    al, ah = interval_a
    bl, bh = interval_b

    if al > ah:
        raise ValueError("Interval A bounds are inverted")

    if bl > bh:
        raise ValueError("Interval B bounds are inverted")

    return ah >= bl and bh >= al
