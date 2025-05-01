from odoo import http
from odoo.http import request

class AutoLogin(http.Controller):
    @http.route('/auth/bypass', type='http', auth='none', csrf=False)
    def auto_login(self, **kwargs):
        session_id = request.httprequest.args.get('session_id')
        if session_id:
            return """
                <html>
                    <head>
                        <script>
                            document.cookie = "session_id=%s; path=/; SameSite=Lax";
                            window.location.href = "/web";
                        </script>
                    </head>
                    <body>
                        <p>Logging in...</p>
                    </body>
                </html>
            """ % session_id
        return http.redirect_with_hash('/web/login')
