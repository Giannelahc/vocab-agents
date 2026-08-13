from fastapi import HTTPException
from domain.models.user_example import UserExample
from domain.repositories.user_example_repository import UserExampleRepository

class UserExampleService:

    def __init__(self,  user_example_repository: UserExampleRepository):
        self.user_example_repository = user_example_repository

    async def save_examples(self, examples_list: list[str], word_sense_id: int):
        examples = [
            UserExample(word_sense_id=word_sense_id, sentence=example)
            for example in examples_list
        ]
        return await self.user_example_repository.save_all(examples)
