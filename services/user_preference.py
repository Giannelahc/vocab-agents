from sqlalchemy import select
from entities.user_preferences import UserPreference

class UserPreferenceService:
    def __init__(self, db_session):
        self.db = db_session

    async def get_user_preferences(self, user_id):
        stmt = select(UserPreference).filter(UserPreference.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
