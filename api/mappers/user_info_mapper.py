
from domain.models.user_info import UserInfo
from api.mappers.user_preference_mapper import UserPreferenceMapper
from schemas.user import UserInfoResponse


class UserInfoMapper:

    @staticmethod
    def to_response(entity: UserInfo) -> UserInfoResponse:

        model = UserInfoResponse(
            id=entity.id,
            name= entity.name,
            lastname= entity.lastname,
            username= entity.username,
            email= entity.email,
            preference=UserPreferenceMapper.to_dto(entity.preference) if entity.preference is not None else None,
            created_at=entity.created_at
        )

        return model

    