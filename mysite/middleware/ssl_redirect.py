# http://djangosnippets.org/snippets/880/
import re

from django.conf import settings
from django.http import HttpResponseRedirect


class SSLRedirect:
    urls = tuple([re.compile(url) for url in settings.SSL_URLS])
    ignore_urls = tuple([re.compile(url) for url in settings.NO_REDIRECT_URLS])

    def process_request(self, request):

        # If the url is on the no redirect list, let it pass through as-is.
        for url in self.ignore_urls:
            if url.match(request.path) is not None:
                return None

        # Determine if the url should be redirected or not.
        url_matched = False
        for url in self.urls:
            if url.match(request.path) is not None:
                url_matched = True
                break
        if not url_matched == self._is_secure(request):
            return self._redirect(request, url_matched)

    def _is_secure(self, request):
        if any([request.is_secure(), request.META.get('HTTP_X_FORWARDED_PROTO', '') == 'https']):
            return True

        return False

    def _redirect(self, request, secure):
        protocol = secure and "https" or "http"

        if secure:
            host = getattr(settings, 'SSL_HOST', request.get_host())
        else:
            host = getattr(settings, 'HTTP_HOST', request.get_host())
        newurl = "%s://%s%s" % (protocol, host, request.get_full_path())

        return HttpResponseRedirect(newurl)
