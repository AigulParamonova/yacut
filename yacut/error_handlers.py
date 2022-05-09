from flask import jsonify, render_template

from . import app, db
from .exceptions import ApiException


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Обработчик ошибки"""
    db.session.rollback()
    return render_template('500.html'), 500


@app.errorhandler(ApiException)
def api_exception(error):
    return jsonify(error.to_dict()), error.status_code
