from odoo import http
from odoo.http import request, Response
from werkzeug.utils import redirect

class AutoLogin(http.Controller):
    @http.route('/auth/bypass', type='http', auth='none', csrf=False)
    def auto_login(self, **kwargs):
        session_id = request.httprequest.args.get('session_id')
        if not session_id:
            return redirect('/web/login')

        # Return HTML with JavaScript to set cookie before redirect
        return Response(f"""
            <html>
                <body>
                    <script>
                        document.cookie = 'session_id={session_id}; path=/; httponly';
                        window.location.href = '/web';
                    </script>
                </body>
            </html>
        """)
