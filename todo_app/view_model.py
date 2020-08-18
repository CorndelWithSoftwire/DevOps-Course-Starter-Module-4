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
        return len(self.done_items) <= 3

    @property
    def recent_done_items(self):
        return [item for item in self.done_items if item.modified_today()]

    @property
    def older_done_items(self):
        return [item for item in self.done_items if not item.modified_today()]
