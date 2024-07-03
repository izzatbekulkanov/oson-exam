class RealIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get real IP address from X-Forwarded-For header
        real_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if real_ip:
            real_ip = real_ip.split(',')[0].strip()
        else:
            real_ip = request.META.get('REMOTE_ADDR')
        request.real_ip = real_ip  # Save real IP address in request object
        return self.get_response(request)