from entities.user_preferences import UserPreference

class UserPreferenceService:
    def __init__(self, db_session):
        self.db = db_session

    def get_user_preferences(self, user_id):
        pref = self.db.query(UserPreference)\
                      .filter(UserPreference.user_id == user_id)\
                      .first()
        return pref