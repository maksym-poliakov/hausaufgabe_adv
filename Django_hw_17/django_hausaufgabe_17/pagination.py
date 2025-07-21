from rest_framework.pagination import CursorPagination

class CustomPagination(CursorPagination):
    page_size = 6
    ordering = 'created_at'