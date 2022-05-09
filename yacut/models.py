from datetime import datetime

from flask import url_for

from . import db


class URL_map(db.Model):
    """Модель связывающая длинную ссылку с короткой."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict_post(self):
        return dict(
            url=self.original,
            short_link=url_for('redirect_view', short=self.short, _external=True)
        )

    def to_dict_get(self):
        return dict(
            url=self.original
        )
