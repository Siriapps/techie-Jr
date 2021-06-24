from flask import Blueprint,render_template

error_pages = Blueprint('error_pages',__name__)

@error_pages.app_errorhandler(404)# Not Found error page
def error_404(error):
    return render_template('error_pages/404.html.j2') , 404

@error_pages.app_errorhandler(403)# For forbidden access
def error_403(error):
    return render_template('error_pages/403.html.j2') , 403
