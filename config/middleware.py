from django.conf import settings
from django.db import connection, reset_queries


class QueryCountHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.DEBUG:
            reset_queries()

        response = self.get_response(request)

        if settings.DEBUG:
            response["X-DB-Query-Count"] = str(len(connection.queries))

        return response