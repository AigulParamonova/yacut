import re
from flask import request, jsonify

from . import app, db
from .models import URL_map
from .exceptions import ApiException
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_short_link():
    """Создаёт короткую ссылку."""
    data = request.get_json()
    if data is None:
        raise ApiException('Отсутствует тело запроса')

    if 'url' not in data:
        raise ApiException('"url" является обязательным полем!')

    short_link = data.get('custom_id')
    if short_link:
        if len(short_link) > 16:
            raise ApiException('Указано недопустимое имя для короткой ссылки')
        if not re.match('^[A-Za-z0-9]*$', short_link):
            raise ApiException('Указано недопустимое имя для короткой ссылки')
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
    return jsonify(url_map.to_dict_post()), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    """Связывает короткую ссылку с оригинальной."""
    url_map = URL_map.query.filter_by(short=short_id).first()
    if url_map is None:
        raise ApiException('Указанный id не найден', 404)
    return jsonify(url_map.to_dict_get()), 200
