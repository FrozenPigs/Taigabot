# for when you need to loop a big array but just want the first N items
def limit(j, arr):
    i = 0
    iterable = iter(arr)

    while True:
        yield next(iterable)
        i = i + 1
        if i == j:
            break
