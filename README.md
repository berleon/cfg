# cfg

[![Build Status](https://travis-ci.org/berleon/cfg.svg?branch=master)](https://travis-ci.org/berleon/cfg)

Simple tool to inject configuration into classes.

## Example:

```python
import cfg

config = cfg.Config()


@config
class Person:
    def __init__(self, name):
        self.name = name


@config('car')
class Car:
    def __init__(self, velocity=50, pos=[40, 20]):
        self.velocity = velocity
        self.pos = pos

# load from file
# content of myconfig.yaml: Person: {'name': 'Ben'}

config.load('myconfig.yaml')
ben = Person(c)
ben.name        # Ben

# or configure directly
c = config.configure({'Person': {'name': 'Ben'}})
ben = Person(c)

car = Car(c)
car.pos          # default [40, 20]
car.velocity     # 50

# save a default config
config.dump('default.yaml')

# cfg will not allow you to set unused parameters
config.configure({'Person': {'not_used_field': 'some value'}})      # throws an execption

```

Currently not form of nested configuration is supported
