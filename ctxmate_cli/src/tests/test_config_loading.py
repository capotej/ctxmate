from ctxmate_cli.config import Config, default_config

def test_default_config():
    c = default_config()
    assert 2 == len(c.manager().loaders)


def test_config():
    c = Config(
        prompts_dir=("a:b",), extra_prompts_dir=("y:z",), backend="ctxmate-echo-backend"
    )
    assert 3 == len(c.manager().loaders)

def test_config2():
    c = Config(
        prompts_dir=(), extra_prompts_dir=("y:z",), backend="ctxmate-echo-backend"
    )
    assert 2 == len(c.manager().loaders)

def test_config3():
    prompts_dir: tuple[str,...] = ('project:prompts',)
    extra_prompts_dir: tuple[str,...] = ()
    c = Config(
        prompts_dir=prompts_dir, extra_prompts_dir=extra_prompts_dir, backend="ctxmate-echo-backend"
    )
    assert 2 == len(c.manager().loaders)