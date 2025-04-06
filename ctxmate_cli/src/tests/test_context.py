from ctxmate_cli.context import Context


def test_basic_context():
    c = Context()
    c.add_system_prompt("this is a system prompt")
    c.add_prompt("do this")
    c.flush()
    assert c.final_system_prompt == "this is a system prompt\n".encode("utf-8")
    assert c.final_prompt == "do this\n".encode("utf-8")
    try:
        c.add_prompt("should fail")
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == "I/O operation on closed file."
    try:
        c.add_system_prompt("should fail")
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == "I/O operation on closed file."
