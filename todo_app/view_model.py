class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def to_do_items(self):
        return [item for item in self._items if item.status == 'To Do']

    @property
    def doing_items(self):
        return [item for item in self._items if item.status == 'Doing']

    @property
    def done_items(self):
        return [item for item in self._items if item.status == 'Done']

    @property
    def show_all_done_items(self):
        return len(self._items) <= 3
