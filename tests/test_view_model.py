from datetime import date, datetime

from freezegun import freeze_time

from todo_item import Item
from view_model import ViewModel


def test_categories_are_empty_if_no_matching_items():
    items = [
        Item(1, 'Task 1',  date.today(), 'Other Status')
    ]

    view_model = ViewModel(items)

    assert len(view_model.to_do_items) == 0
    assert len(view_model.doing_items) == 0
    assert len(view_model.done_items) == 0


def test_items_are_split_into_categories():
    items = [
        Item(1, 'Task 1', date.today(), 'Other Status'),
        Item(2, 'Task 2', date.today(), 'To Do'),
        Item(3, 'Task 3', date.today(), 'Done'),
        Item(4, 'Task 4', date.today(), 'To Do'),
        Item(5, 'Task 5', date.today(), 'Doing')
    ]

    view_model = ViewModel(items)

    assert view_model.to_do_items == [
        Item(2, 'Task 2', date.today(), 'To Do'),
        Item(4, 'Task 4', date.today(), 'To Do')
    ]
    assert view_model.doing_items == [Item(5, 'Task 5', date.today(), 'Doing')]
    assert view_model.done_items == [Item(3, 'Task 3', date.today(), 'Done')]


def test_should_show_all_completed_items_if_there_are_three_or_fewer():
    items = [
        Item(1, 'Task 1', date.today(), 'Done'),
        Item(2, 'Task 2', date.today(), 'Done'),
        Item(3, 'Task 3', date.today(), 'Doing'),
        Item(4, 'Task 4', date.today(), 'Done'),
    ]

    view_model = ViewModel(items)

    assert view_model.show_all_done_items is True


def test_should_not_show_all_completed_items_if_there_are_more_than_three():
    items = [
        Item(1, 'Task 1', date.today(), 'Done'),
        Item(2, 'Task 2', date.today(), 'Done'),
        Item(3, 'Task 3', date.today(), 'Done'),
        Item(4, 'Task 4', date.today(), 'Done'),
    ]

    view_model = ViewModel(items)

    assert view_model.show_all_done_items is False


def test_recent_items_contain_only_items_last_modified_today():
    items = [
        Item(1, 'Done Yesterday', datetime(2020, 6, 15, 23, 59, 59), 'Done'),
        Item(2, 'Done Today', datetime(2020, 6, 16, 0, 0, 0), 'Done'),
        Item(3, 'Doing Today', datetime(2020, 6, 16, 9, 0, 0), 'Doing'),
    ]

    with freeze_time("2020-06-16 09:30:00"):
        view_model = ViewModel(items)

        assert view_model.recent_done_items == [
            Item(2, 'Done Today', datetime(2020, 6, 16, 0, 0, 0), 'Done'),
        ]


def test_older_items_contain_only_items_last_modified_before_today():
    items = [
        Item(1, 'Done Yesterday', datetime(2020, 6, 15, 23, 59, 59), 'Done'),
        Item(2, 'Done Today', datetime(2020, 6, 16, 0, 0, 0), 'Done'),
        Item(3, 'Doing Yesterday', datetime(2020, 6, 15, 9, 0, 0), 'Doing'),
    ]

    with freeze_time("2020-06-16 09:30:00"):
        view_model = ViewModel(items)

        assert view_model.older_done_items == [
            Item(1, 'Done Yesterday', datetime(2020, 6, 15, 23, 59, 59), 'Done'),
        ]
