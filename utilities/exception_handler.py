from django.utils.encoding import force_text
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler


#
class CustomValidation(APIException):
    """Return custom validation error for specific fields with custom detail message

    Example usage: 

    CustomValidation("username", "username already exists", status.HTTP_400_BAD_REQUEST)"""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Something went wrong."

    def __init__(self, field=None, detail=None, status_code=None):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = {field: [force_text(detail)]}
        else:
            self.detail = {"detail": [force_text(self.default_detail)]}


def custom_exception_handler(exc, context):
    """Encapsulate all validation error messages in errors dictionary and return the result"""

    response = exception_handler(exc, context)

    if response is not None:
        data = response.data
        response.data = {}
        response.data["errors"] = data
    # else:
    #     return Response({"errors": {"detail": ["There is a problem in our backend"]}})

    return response
