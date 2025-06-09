import logging

from django.http import JsonResponse


class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            # Логируем ошибку (можно отправлять куда угодно)
            logging.exception("Unhandled exception: %s", e)
            # Возвращаем JSON-ошибку (например, для DRF API)
            return JsonResponse(
                {"detail": "Internal server error", "error": str(e)},
                status=500
            )