class EmptyQueueError(Exception):
    pass

class Queue:
    FIFO = "FIFO"
    LIFO = "LIFO"
    STRATEGIES = [FIFO, LIFO]
    def __init__(self, strategy: str = FIFO):
        self.strategy = strategy
        self.storage = []
        if self.strategy not in self.STRATEGIES:
            raise TypeError("Strategy must be FIFO or LIFO")

    def add(self, item):
        if self.strategy == self.FIFO:
            self.storage.insert(0, item)

    def remove(self):
        if self.strategy == self.FIFO:
            if not self.storage:
                raise EmptyQueueError("Queue is empty")
            self.storage.pop()


class UniqueQueue:

    def __init__(self, lifo=False, initial_items=None):
        self.lifo = lifo
        self._items = []
        self._set = set()

        if initial_items is not None:
            for item in initial_items:
                self.push(item)

    def push(self, item):
        if item in self._set:
            return False

        self._items.append(item)
        self._set.add(item)
        return True

    def pop(self):
        if not self._items:
            raise IndexError("Cannot pop from empty queue")

        if self.lifo:
            item = self._items.pop()
        else:
            item = self._items.pop(0)

        self._set.remove(item)
        return item

    def peek(self):
        if not self._items:
            raise IndexError("Cannot peek at empty queue")

        if self.lifo:
            return self._items[-1]
        else:
            return self._items[0]

    @property
    def size(self):
        return len(self._items)

    @property
    def last(self):
        if not self._items:
            raise IndexError("Queue is empty, no last element")
        return self._items[-1]

    @property
    def first(self):
        if not self._items:
            raise IndexError("Queue is empty, no first element")
        return self._items[0]

    def __len__(self):
        return self.size

    def __contains__(self, item):
        return item in self._set

    def __repr__(self):
        mode = "LIFO" if self.lifo else "FIFO"
        return f"UniqueQueue({mode}, {self._items})"

    def clear(self):
        self._items.clear()
        self._set.clear()

    def to_list(self):
        return self._items.copy()
