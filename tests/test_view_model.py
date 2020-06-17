from todo_item import Item
from view_model import ViewModel


def test_categories_are_empty_if_no_matching_items():
    items = [
        Item(1, 'Task 1', 'Other Status')
    ]

    view_model = ViewModel(items)

    assert len(view_model.to_do_items) == 0
    assert len(view_model.doing_items) == 0
    assert len(view_model.done_items) == 0


def test_items_are_split_into_categories():
    items = [
        Item(1, 'Task 1', 'Other Status'),
        Item(2, 'Task 2', 'To Do'),
        Item(3, 'Task 3', 'Done'),
        Item(4, 'Task 4', 'To Do'),
        Item(5, 'Task 5', 'Doing')
    ]

    view_model = ViewModel(items)

    assert view_model.to_do_items == [
        Item(2, 'Task 2', 'To Do'),
        Item(4, 'Task 4', 'To Do')
    ]
    assert view_model.doing_items == [Item(5, 'Task 5', 'Doing')]
    assert view_model.done_items == [Item(3, 'Task 3', 'Done')]


def test_should_show_all_completed_items_if_there_are_three_or_fewer():
    items = [
        Item(1, 'Task 1', 'Done'),
        Item(2, 'Task 2', 'Done'),
        Item(3, 'Task 3', 'Done'),
    ]

    view_model = ViewModel(items)

    assert view_model.show_all_done_items is True


def test_should_not_show_all_completed_items_if_there_are_more_than_three():
    items = [
        Item(1, 'Task 1', 'Done'),
        Item(2, 'Task 2', 'Done'),
        Item(3, 'Task 3', 'Done'),
        Item(4, 'Task 4', 'Done'),
    ]

    view_model = ViewModel(items)

    assert view_model.show_all_done_items is False
