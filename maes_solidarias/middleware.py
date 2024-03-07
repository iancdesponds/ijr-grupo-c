from django.shortcuts import redirect

class AddTrailingSlashMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Adiciona uma barra final se não houver uma
        if not request.path.endswith('/'):
            return redirect(request.path + '/')

        response = self.get_response(request)
        return response