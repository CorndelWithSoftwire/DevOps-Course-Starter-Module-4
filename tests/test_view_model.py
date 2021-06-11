from datetime import datetime

from freezegun import freeze_time

from todo_app.data.trello_items import Item
from todo_app.view_model import ViewModel

def test_categories_are_empty_if_no_matching_items():
    items = [
        Item(1, 'Task 1', datetime.now(), 'Other Status')
    ]

    view_model = ViewModel(items)

    assert len(view_model.to_do_items) == 0
    assert len(view_model.doing_items) == 0
    assert len(view_model.done_items) == 0

@freeze_time()
def test_items_are_split_into_categories():
    items = [
        Item(1, 'Task 1', datetime.now(), 'Other Status'),
        Item(2, 'Task 2', datetime.now(), 'To Do'),
        Item(3, 'Task 3', datetime.now(), 'Done'),
        Item(4, 'Task 4', datetime.now(), 'To Do'),
        Item(5, 'Task 5', datetime.now(), 'Doing')
    ]

    view_model = ViewModel(items)

    assert view_model.to_do_items == [
        Item(2, 'Task 2', datetime.now(), 'To Do'),
        Item(4, 'Task 4', datetime.now(), 'To Do')
    ]
    assert view_model.doing_items == [Item(5, 'Task 5', datetime.now(), 'Doing')]
    assert view_model.done_items == [Item(3, 'Task 3', datetime.now(), 'Done')]


def test_should_show_all_completed_items_if_there_are_three_or_fewer():
    items = [
        Item(1, 'Task 1', datetime.now(), 'Done'),
        Item(2, 'Task 2', datetime.now(), 'Done'),
        Item(3, 'Task 3', datetime.now(), 'Doing'),
        Item(4, 'Task 4', datetime.now(), 'Done'),
    ]

    view_model = ViewModel(items)

    assert view_model.should_show_all_done_items is True


def test_should_not_show_all_completed_items_if_there_are_more_than_three():
    items = [
        Item(1, 'Task 1', datetime.now(), 'Done'),
        Item(2, 'Task 2', datetime.now(), 'Done'),
        Item(3, 'Task 3', datetime.now(), 'Done'),
        Item(4, 'Task 4', datetime.now(), 'Done'),
    ]

    view_model = ViewModel(items)

    assert view_model.should_show_all_done_items is False

@freeze_time("2020-06-16 09:30:00")
def test_recent_items_contain_only_items_last_modified_today():
    items = [
        Item(1, 'Done Yesterday', datetime(2020, 6, 15, 23, 59, 59), 'Done'),
        Item(2, 'Done Today', datetime(2020, 6, 16, 0, 0, 0), 'Done'),
        Item(3, 'Doing Today', datetime(2020, 6, 16, 9, 0, 0), 'Doing'),
    ]

    view_model = ViewModel(items)

    assert view_model.recent_done_items == [
        Item(2, 'Done Today', datetime(2020, 6, 16, 0, 0, 0), 'Done'),
    ]

@freeze_time("2020-06-16 09:30:00")
def test_older_items_contain_only_items_last_modified_before_today():
    items = [
        Item(1, 'Done Yesterday', datetime(2020, 6, 15, 23, 59, 59), 'Done'),
        Item(2, 'Done Today', datetime(2020, 6, 16, 0, 0, 0), 'Done'),
        Item(3, 'Doing Yesterday', datetime(2020, 6, 15, 9, 0, 0), 'Doing'),
    ]

    view_model = ViewModel(items)

    assert view_model.older_done_items == [
        Item(1, 'Done Yesterday', datetime(2020, 6, 15, 23, 59, 59), 'Done'),
    ]
