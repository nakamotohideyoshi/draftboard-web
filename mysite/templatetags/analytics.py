from django import template
from django.conf import settings
register = template.Library()


class ShowKissAnalyticsJS(template.Node):

    def render(self, context):
        code = getattr(settings, "KISS_ANALYTICS_CODE", False)
        if not code:
            return "<!-- KISS Analytics not included because you haven't set the settings.KISS_ANALYTICS_CODE variable! -->"

        script = """
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
        user = context['user']
        if user.is_authenticated():
            script += """
            <script type="text/javascript">
                _kmq.push(['identify', '""" + str(user.username) + """']);
            </script>
            """
        return script


def kissanalyticsjs(parser, token):
    return ShowKissAnalyticsJS()

kiss_analytics = register.tag(kissanalyticsjs)


class ShowGoogleAnalyticsJS(template.Node):

    def render(self, context):
        code = getattr(settings, "GOOGLE_ANALYTICS_CODE", False)
        if not code:
            return "<!-- Google Analytics not included because you haven't set the settings.GOOGLE_ANALYTICS_CODE variable! -->"

        return """
            <script>
            (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
            ga('create', '""" + str(code) + """', 'auto'); ga('send', 'pageview');
            </script>
        """


def googleanalyticsjs(parser, token):
    return ShowGoogleAnalyticsJS()

google_analytics = register.tag(googleanalyticsjs)