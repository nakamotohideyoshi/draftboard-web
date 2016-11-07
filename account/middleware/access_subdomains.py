import re

from django.http import HttpResponseForbidden


class AccessSubdomainsMiddleware(object):
    def process_request(self, request):
      # URLs we want to allow for any subdomain, regardless of if they have permission. This is primarily for third
      # party developers or sites that need API access
        ignore_urls = (
            r'/api/*',
            r'/static/*',
        )
        ignore_urls = tuple([re.compile(url) for url in ignore_urls])

        # If the url is on the no redirect list, let it pass through as-is.
        for url in ignore_urls:
            if url.match(request.path) is not None:
                return None

        useragent = request.META.get('HTTP_USER_AGENT', '')

        if request.COOKIES.get('access_subdomains', 'false') != 'true' and 'faceb' not in useragent:
            return HttpResponseForbidden('Site access denied')
