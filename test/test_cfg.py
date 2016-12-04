import cfg
import pytest

config = cfg.Config()


@config()
class Person:
    def __init__(self, name):
        self.name = name


@config('car')
class Car:
    def __init__(self, velocity=50, pos=[40, 40]):
        self.velocity = velocity
        self.pos = pos


@config
class Building:
    def __init__(self, size=20):
        pass


def test_config():
    assert 'Person' in config

    with pytest.raises(Exception):
        config.ensure_all_set()

    c = config.configure({'Person': {'name': 'David'}})
    david = Person(c)
    assert david.name == 'David'

    car = Car(c)
    assert car.velocity == c.car.velocity
    assert car.pos == c.car.pos


def test_load(tmpdir):
    tmpdir.join("config.yaml").write("""
        Person:
            name: Ben
        car:
            velocity: 40
    """)
    c = config.load(str(tmpdir.join("config.yaml")))
    ben = Person(c)
    assert ben.name == 'Ben'


def test_dump(tmpdir):
    fname = str(tmpdir.join('dumped_config.yaml'))
    config.dump(fname)
    c = config.load(fname)
    per = Person(c)
    assert per.name == 'REQUIRED'
