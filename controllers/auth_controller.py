from odoo import http
from odoo.http import request

class AutoLogin(http.Controller):
    @http.route('/auth/bypass', type='http', auth='none', csrf=False)
    def auto_login(self, **kwargs):
        session_id = request.httprequest.args.get('session_id')
        if session_id:
            return f"""
                <html>
                    <head>
                        <script>
                            const sessionId = "{session_id}";
                            const maxRetries = 10;
                            let attempts = 0;

                            function setCookie() {{
                                document.cookie = "session_id=" + sessionId + "; path=/; SameSite=Lax";
                            }}

                            function checkAndRedirect() {{
                                const cookies = document.cookie;
                                if (cookies.includes("session_id=" + sessionId)) {{
                                    window.location.href = "/web";
                                }} else if (attempts < maxRetries) {{
                                    attempts++;
                                    setTimeout(checkAndRedirect, 200);
                                }} else {{
                                    document.body.innerHTML = "<p>Failed to login. Please try again.</p>";
                                }}
                            }}

                            setCookie();
                            setTimeout(checkAndRedirect, 100);
                        </script>
                    </head>
                    <body>
                        <p>Logging in, please wait...</p>
                    </body>
                </html>
            """
        return http.redirect_with_hash('/web/login')
