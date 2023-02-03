from rest_framework.response import Response
from rest_framework import status


class SuccessResponse(Response):

    def __init__(self, data=None, template_name=None, headers=None, exception=False, content_type=None):

        self.data = data
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        super().__init__(None, status=status.HTTP_200_OK)
