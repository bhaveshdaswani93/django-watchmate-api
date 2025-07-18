from rest_framework import pagination 


class WatchListPagination(pagination.PageNumberPagination):
    page_size = 2
    page_query_param = 'p'
    page_size_query_param = 'size'
    # page_size_query_param = 'page_size'
    max_page_size = 3
    last_page_strings = ('last', 'end', 'final')

class WatchListLimitOffsetPagination(pagination.LimitOffsetPagination):
    # pass
    default_limit = 2
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 3
    # # max_limit = 1000
    # # default_limit = 10
    # # limit_query_param = 'page_size'
    # # offset_query_param = 'page'

class WatchListCursorPagination(pagination.CursorPagination):
    pass
    page_size = 3
    cursor_query_param = 'c'
    # page_size_query_param = 'size'
    # max_page_size = 3
    # cursor_query_param = 'cursor'
    # ordering = '-created'  # Assuming 'created' is a field in your model for ordering
    # ordering = 'name'  # Example of another field to order by
    # cursor_query_param = 'page'

