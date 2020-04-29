"""
API Endpoint Abstract Class
"""


class Endpoint:
    def run(self, db, request):
        raise NotImplementedError()
