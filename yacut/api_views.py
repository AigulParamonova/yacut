import re
from http import HTTPStatus

from flask import jsonify, request

from . import app
from . import constants as const
from . import db
from .exceptions import ApiException
from .models import URL_map
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """Создаёт короткую ссылку."""
    data = request.get_json()
    if data is None:
        raise ApiException(const.MISSING_REQUEST_BODY)

    if 'url' not in data:
        raise ApiException(const.REQUIRED_FIELD)

    short_link = data.get('custom_id')
    if short_link:
        if len(short_link) > 16:
            raise ApiException(const.SHORT_LINK_INVALID_NAME)
        if not re.match(const.ALLOWED_CHARACTERS, short_link):
            raise ApiException(const.SHORT_LINK_INVALID_NAME)
        if URL_map.query.filter_by(short=short_link).first():
            raise ApiException(f'Имя "{short_link}" уже занято.')
    if short_link is None or short_link == '':
        short_link = get_unique_short_id()
    url_map = URL_map(
        original=data.get('url'),
        short=short_link
    )
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict_post()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    """Связывает короткую ссылку с оригинальной."""
    url_map = URL_map.query.filter_by(short=short_id).first()
    if url_map is None:
        raise ApiException(const.ID_NOT_FOUND, HTTPStatus.NOT_FOUND)
    return jsonify(url_map.to_dict_get()), HTTPStatus.OK
