from uuid import uuid1

from cassandra.cqlengine.models import Model
from cassandra.cqlengine.columns import *

from killranswers.ratings.models import AnswerRating, vote


class Answer(Model):
    question_id = TimeUUID(primary_key=True)
    answer_id = TimeUUID(primary_key=True, default=uuid1)
    user_id = Text()
    text = Text()

    @classmethod
    def create(cls, user, question, text):
        answer = super(cls, Answer).create(question_id=question.question_id,
                                           user_id=user.user_id,
                                           text=text)
        return answer

    @property
    def id(self):
        return self.answer_id

Answer.vote = vote(AnswerRating)
