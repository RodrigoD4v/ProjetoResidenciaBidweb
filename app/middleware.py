from django.middleware.csrf import CsrfViewMiddleware
from django.middleware.csrf import get_token
from django.http import HttpRequest

CORS_ORIGIN_WHITELIST = [
    'https://projetoresidenciabidweb-production.up.railway.app',
]

class CustomCsrfMiddleware(CsrfViewMiddleware):
    def process_request(self, request):
        # Verifica se a solicitação é segura (HTTPS) ou se a origem é confiável
        if request.is_secure() or self._allow_origin(request):
            return super().process_request(request)
        # Se não, apenas definimos um token CSRF na solicitação
        get_token(HttpRequest())

    def _allow_origin(self, request):
        # Verifica se a origem da solicitação está na lista de origens permitidas
        return any(
            request.headers.get("Origin") == origin
            for origin in CORS_ORIGIN_WHITELIST
        )
