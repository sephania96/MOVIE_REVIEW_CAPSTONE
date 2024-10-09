from rest_framework.pagination import PageNumberPagination

class ReviewPagination(PageNumberPagination):
    page_size = 5  # Number of reviews per page
    page_size_query_param = 'page_size'
    max_page_size = 10