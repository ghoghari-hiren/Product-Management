from rest_framework.throttling import SimpleRateThrottle

class AdminUserRateThrottle(SimpleRateThrottle):
    scope = 'admin_user'

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated and request.user.is_staff:
            return self.cache_format % {
                'scope': self.scope,
                'ident': request.user.pk
            }
        return None

    def allow_request(self, request, view):
        if not request.user.is_authenticated or not request.user.is_staff:
            return True
        return super().allow_request(request, view)


class RegularUserRateThrottle(SimpleRateThrottle):
    scope = 'regular_user'

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated and not request.user.is_staff:
            return self.cache_format % {
                'scope': self.scope,
                'ident': request.user.pk
            }
        return None

    def allow_request(self, request, view):
        if not request.user.is_authenticated or request.user.is_staff:
            return True
        return super().allow_request(request, view)


class AnonymousRateThrottle(SimpleRateThrottle):
    scope = 'anon_user'

    def get_cache_key(self, request, view):
        if not request.user.is_authenticated:
            ident = self.get_ident(request)
            return self.cache_format % {
                'scope': self.scope,
                'ident': ident
            }
        return None

    def allow_request(self, request, view):
        if request.user.is_authenticated:
            return True
        return super().allow_request(request, view)
