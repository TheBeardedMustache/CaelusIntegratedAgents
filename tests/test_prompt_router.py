from seraph_llm.prompt_router import agent_call_schema


def test_parses_json_with_prefix():
    data = {"CALL_AGENT": {"name": "foo", "intent": "bar", "kwargs": {}}}
    text = '{"CALL_AGENT": {"name": "foo", "intent": "bar", "kwargs": {}}}'
    assert agent_call_schema(text) == data


def test_parses_json_with_trailing_text():
    text = '{"CALL_AGENT": {"name": "foo", "intent": "bar", "kwargs": {}}} extra'
    result = agent_call_schema(text)
    assert result == {"CALL_AGENT": {"name": "foo", "intent": "bar", "kwargs": {}}}


def test_fallback_run_syntax():
    result = agent_call_schema('RUN:foo:bar')
    assert result == {"CALL_AGENT": {"name": "foo", "intent": "bar", "kwargs": {}}}


def test_returns_raw_on_invalid():
    assert agent_call_schema('hello') == 'hello'
