from odoo import http
from odoo.http import request
from werkzeug.utils import redirect

class AutoLogin(http.Controller):

    @http.route('/auth/bypass', type='http', auth='none', csrf=False)
    def auto_login(self, **kwargs):
        session_id = request.httprequest.args.get('session_id')
        if not session_id:
            return redirect('/web/login')

        # First step: set cookie and redirect to confirm
        response = redirect(f'/auth/confirm?retry=0')
        response.set_cookie('session_id', session_id, path='/', httponly=True)
        return response

    @http.route('/auth/confirm', type='http', auth='none', csrf=False)
    def confirm(self, **kwargs):
        retry = int(request.httprequest.args.get('retry', 0))
        max_retries = 3

        # Check if user is already authenticated
        if request.session.uid:
            return redirect('/web')

        # Retry logic
        if retry < max_retries:
            # Retry after a short pause
            return redirect(f'/auth/confirm?retry={retry + 1}')
        else:
            # If too many retries, go to login
            return redirect('/web/login')
