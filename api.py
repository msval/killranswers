import os
import socket
import capnp
import killranswers_capnp
from killranswers.categories import Category

class KillrAnswersServer(killranswers_capnp.KillrAnswers.Server):
    def ask(self, text, **kwargs):
        print "incoming"
        print str(text)
        q = killranswers_capnp.Question.new_message(questionId="test",
                                        questionText="blah")
        return q

    def createCategory(self, name, parent, **kwargs):
        cat = killranswers_capnp.Category.new_message()
        return cat

    def getRootCategory(self, **kwargs):
        root = Category.get_root()
        cat = killranswers_capnp.Category.new_message()
        # cat.categoryId = root.category_id
        # cat.name = root.name
        return cat


def get_server():
    server = capnp.TwoPartyServer('*:6000', bootstrap=KillrAnswersServer())
    return server

if __name__ == "__main__":
    server = get_server()
    print "Starting server.  To kill:\n\nkill %d" % os.getpid()
    server.run_forever()
