import os
import socket
import capnp
import killranswers_capnp as api
from killranswers import User, Category, Question, Answer


class KillrAnswersServer(api.KillrAnswers.Server):
    def ask(self, text, category, user, **kwargs):
        cat = Category.get(category)
        u = User.get(user)
        question = Question.create(cat, text, u)
        return str(question.question_id)

    def createCategory(self, text, parent, **kwargs):
        p = Category.get(category_id=parent)
        cat = p.create_sub(text)
        return str(cat.category_id)

    def getRootCategory(self, **kwargs):
        root = Category.get_root()
        cat = api.Category.new_message()
        cat.id = str(root.category_id)
        cat.name = root.name
        return cat

    def registerUser(self, user_id, **kwargs):
        User.create(user_id)

    def getChildCategories(self, parent, **kwargs):
        cat = Category.get(parent)
        children = cat.get_children()

        response = []

        for x in children:
            tmp = api.Category.new_message()
            tmp.id = str(x.category_id)
            tmp.name = x.child_category_name
            response.append(tmp)

        return response

    def answer(self, question, user, text, **kwargs):
        q = Question.get(question)
        u = User.get(user)

        answer = q.answer(user=u, text=text)
        return str(answer.answer_id)

    def getAnswers(self, question, **kwargs):
        q = Question.get(question)
        answers = q.get_answers()
        resp = []
        for a in answers:
            tmp = api.Answer.new_message()
            tmp.id = str(a.answer_id)
            tmp.question = str(a.question_id)
            tmp.user = str(a.user_id)
            tmp.text = a.text
            resp.append(tmp)
        return resp

    def voteQuestion(self, question, user, vote, **kwargs):
        q = Question.get(question)
        u = User.get(user)
        q.vote(u, vote)
        return vote

    def voteAnswer(self, answer, user, vote, **kwargs):
        a = Answer.get(answer)
        u = User.get(user)
        a.vote(user, vote)
        return vote


def get_server():
    server = capnp.TwoPartyServer('*:6000', bootstrap=KillrAnswersServer())
    return server

if __name__ == "__main__":
    from killranswers.connections import cassandra
    cassandra()
    server = get_server()
    print "Starting server.  To kill:\n\nkill %d" % os.getpid()
    server.run_forever()
