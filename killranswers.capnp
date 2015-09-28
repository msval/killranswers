@0xce4c7cd66480f6f2;

interface KillrAnswers {
    ask @0 (text :Text, category :Text, user :Text) -> (question: Question);
    createCategory @1 (text :Text, parent :Text) -> (category: Category);
    getRootCategory @2 () -> (category: Category);
}

struct Question {
    id @0 : Text;
    text @1 : Text;
}

struct Category {
    id @0 : Text;
    name @1: Text;
}
