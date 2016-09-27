from django import template
from django.conf import settings
register = template.Library()


class ShowKissAnalyticsJS(template.Node):

    def render(self, context):
        code = getattr(settings, "KISS_ANALYTICS_CODE", False)
        if not code:
            return "<!-- KISS Analytics not included because you haven't set the settings.KISS_ANALYTICS_CODE variable! -->"

        return """
        <script type="text/javascript">var _kmq = _kmq || [];
            var _kmk = _kmk || '""" + str(code) + """';
            function _kms(u){
              setTimeout(function(){
                var d = document, f = d.getElementsByTagName('script')[0],
                s = d.createElement('script');
                s.type = 'text/javascript'; s.async = true; s.src = u;
                f.parentNode.insertBefore(s, f);
              }, 1);
            }
            _kms('//i.kissmetrics.com/i.js');
            _kms('//scripts.kissmetrics.com/' + _kmk + '.2.js');
        </script>
        """


def kissanalyticsjs(parser, token):
    return ShowKissAnalyticsJS()

kiss_analytics = register.tag(kissanalyticsjs)
