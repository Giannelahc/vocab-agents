
from domain.models.home_info import HomeInfo
from domain.models.user_info import UserInfo
from api.mappers.user_preference_mapper import UserPreferenceMapper
from schemas.user import HomeInfoResponse, UserInfoResponse


class HomeInfoMapper:

    @staticmethod
    def to_response(entity: HomeInfo) -> HomeInfoResponse:

        model = HomeInfoResponse(
            id=entity.id,
            name=entity.name,
            lastname=entity.lastname,
            username=entity.username,
            newWordsCurrentWeek=entity.newWordsCurrentWeek,
            learnedWords=entity.learnedWords
        )

        return model

    