
from domain.models.home_info import HomeInfo
from domain.models.vocabulary_statistics import VocabularyStatistics
from schemas.user import HomeInfoResponse, VocabularyStatisticsDto


class HomeInfoMapper:

    @staticmethod
    def to_response(entity: HomeInfo) -> HomeInfoResponse:

        model = HomeInfoResponse(
            id=entity.id,
            name=entity.name,
            lastname=entity.lastname,
            username=entity.username,
            language_statistics= [
                HomeInfoMapper.to_vocabulary_statistics_dto(statistic)
                for statistic in entity.language_statistics
            ],
            streak=entity.streak,
            today_reviews=entity.today_reviews
        )

        return model

    @staticmethod
    def to_vocabulary_statistics_dto(entity: VocabularyStatistics) -> VocabularyStatisticsDto:
        return VocabularyStatisticsDto(
            language_id=entity.language_id,
            language_name=entity.language_name,
            learned_words=entity.learned_words,
            total_words=entity.total_words,
            new_words_current_week=entity.new_words_current_week
        )

    