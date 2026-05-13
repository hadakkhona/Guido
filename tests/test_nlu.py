from PC.brain.nlu import NLU

nlu = NLU()


def test_destination_intent():
    intent, entities = nlu.process("guide me to youssef's office")

    print(intent)
    print(entities)

    assert intent == "GUIDE_TO"
    assert entities["destination"] == "youssef"


def test_unknown_input():
    intent, entities = nlu.process("bla bla random")

    assert intent == "UNKNOWN"