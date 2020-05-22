def enumerate_small(limit, arr):
    i = 0
    iterable = iter(arr)

    while True:
        yield next(iterable)
        i = i + 1
        if i == limit:
            break

