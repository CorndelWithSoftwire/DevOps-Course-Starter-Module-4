from datetime import date, datetime


class Item:

    def __init__(self, id, name, last_modified, status='To Do'):
        self.id = id
        self.name = name
        self.last_modified = last_modified
        self.status = status

    @classmethod
    def fromTrelloCard(cls, card, list):
        return cls(
            card['id'],
            card['name'],
            datetime.strptime(card['dateLastActivity'], '%Y-%m-%dT%H:%M:%S.%fZ'),
            list['name']
        )

    def reset(self):
        self.status = 'To Do'

    def start(self):
        self.status = 'Doing'

    def complete(self):
        self.status = 'Done'

    def modified_today(self):
        return self.last_modified.date() == date.today()

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, status: {self.status}, last_modified: {self.last_modified}"

    def __eq__(self, other):
        if not isinstance(other, Item):
            return False

        return self.id == other.id \
            and self.name == other.name \
            and self.status == other.status
