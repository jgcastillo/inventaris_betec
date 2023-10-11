import uuid
from datetime import datetime
from typing import Dict

import pytz
from databases import Database
from shared.core import config


class DBSessionMixin:
    def __init__(self, db: Database):
        self.db = db


class AppService(DBSessionMixin):
    pass


class AppRepository(DBSessionMixin):
    @staticmethod
    def generate_uuid() -> uuid.UUID:
        return uuid.uuid4()

    def preprocess_update(self, values: Dict, updated_by: uuid.UUID) -> Dict:
        values["updated_at"] = self._preprocess_date()
        values["updated_by"] = updated_by
        return values

    def _preprocess_date(self) -> datetime:
        d = datetime.now()
        timezone = pytz.timezone(config.TIMEZONE)
        return timezone.localize(d)

    def preprocess_create(self, values: Dict) -> Dict:
        if "id" not in values:
            values["id"] = self.generate_uuid()
        if "is_active" not in values:
            values["is_active"] = True
        if "created_at" not in values:
            values["created_at"] = self._preprocess_date()
        if "updated_at" not in values:
            values["updated_at"] = self._preprocess_date()
        return values
