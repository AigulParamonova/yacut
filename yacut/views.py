import random
import string
from flask import abort, flash, redirect, render_template, flash

from . import app, db
from .forms import YacutForm
from .models import URL_map


def get_unique_short_id():
    """Генерирует короткие ссылки."""
    short_link = ''.join(random.choices(
        string.ascii_letters + string.digits, k=6)
    )
    if URL_map.query.filter_by(short=short_link).first():
        short_link = get_unique_short_id()
    return short_link


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Главная страница с формой для заполнения."""
    form = YacutForm()
    if form.validate_on_submit():
        short_name = form.custom_id.data
        if URL_map.query.filter_by(short=short_name).first():
            flash(f'Имя {short_name} уже занято!')
            return render_template('yacut.html', form=form)

        if short_name is None or short_name == '':
            short_name = get_unique_short_id()
        url_map = URL_map(
            original=form.original_link.data,
            short=short_name,
        )
        db.session.add(url_map)
        db.session.commit()
        return render_template('yacut.html', form=form, short=short_name), 200
    return render_template('yacut.html', form=form)


@app.route('/<string:short>')
def redirect_view(short):
    """Переадресация на исходный адрес при обращении к коротким ссылкам."""
    url_map = URL_map.query.filter_by(short=short).first()
    if url_map is not None:
        return redirect(url_map.original)
    abort(404)
