class BonitaAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated based on session cookies
        bonita_cookies = request.session.get('bonita_cookies')
        if bonita_cookies:
            # Add cookies to the request headers
            cookies_header = '; '.join([f'{name}={value}' for name, value in bonita_cookies.items()])
            request.META['HTTP_COOKIE'] = cookies_header  # Update the HTTP_COOKIE header

        response = self.get_response(request)
        return response