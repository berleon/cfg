import inspect
import yaml


class ConfigDict(dict):
    def __getattr__(self, key):
        if key in self:
            return self[key]
        else:
            return super.__getattr__(key)

    def __setattr__(self, key, value):
        self[key] = value

    def __setitem__(self, key, value):
        if key not in self:
            raise Exception("Key not available: {}".format(key))
        else:
            super().__setitem__(key, value)

    def configure(self, dict):
        dict_copy = self.copy()
        dict_copy.update(dict)
        dict_copy.ensure_all_set()
        return dict_copy

    def update(self, other_dict):
        for k, v in other_dict.items():
            if k in self and issubclass(type(self[k]), ConfigDict):
                self[k].update(v)
            else:
                self[k] = v

    def not_set_values(self):
        not_set = []

        for k, v in self.items():
            if v == inspect.Parameter.empty:
                not_set.append(k)
            elif issubclass(type(v), ConfigDict):
                not_set.extend(["{}.{}".format(k, chl) for chl in v.not_set_values()])
        return not_set

    def ensure_all_set(self):
        not_set = self.not_set_values()
        if not_set:
            raise Exception("Following keys are not set: \n  - " + "\n  - ".join(not_set))

    def to_dict(self):
        d = {}
        for k, v in self.items():
            if issubclass(type(v), ConfigDict):
                d[k] = v.to_dict()
            else:
                d[k] = v
        return d

    def copy(self):
        new = self.__class__()
        for k, v in self.items():
            if issubclass(type(v), ConfigDict):
                v = v.copy()
            dict.__setitem__(new, k, v)
        return new

    def replace_default(self, value):
        c = self.copy()
        for k, v in c.items():
            if issubclass(type(v), ConfigDict):
                c[k] = v.replace_default(value)
            elif v == inspect.Parameter.empty:
                c[k] = value
        return c


class Config(ConfigDict):
    def __call__(self, name=None):
        def get_name(cls):
            if type(name) == str:
                return name
            else:
                return cls.__name__

        def wrapper(cls):
            sig = inspect.signature(cls)
            config = ConfigDict()
            for arg_name, param in sig.parameters.items():
                if arg_name == 'self':
                    continue
                dict.__setitem__(config, arg_name, param.default)

            assert cls.__name__ not in self

            cfg_name = get_name(cls)
            dict.__setitem__(self, cfg_name, config)

            old_new = cls.__new__
            old_init = cls.__init__

            def new(cls, *args, **kwargs):
                if len(args) == 1 and type(args[0]) == Config and not kwargs:
                    config = args[0]
                    obj = old_new(cls)
                    old_init(obj, **config[cfg_name])
                    obj.__config_constructed__ = True
                    return obj
                else:
                    obj = old_new(cls)
                    old_init(obj, *args, **kwargs)
                    return obj

            def init(obj, *args, **kwargs):
                pass

            cls.__new__ = new
            cls.__init__ = init
            return cls

        if type(name) != str and name is not None:
            return wrapper(name)
        else:
            return wrapper

    def dump(self, filename):
        with open(filename, 'w') as f:
            yaml.dump(self.replace_default("REQUIRED").to_dict(), f, default_flow_style=False)

    def load(self, filename):
        with open(filename) as f:
            config_dict = yaml.load(f)
            c = self.configure(config_dict)
            return c

    def to_yaml(self):
        return yaml.dumps(self.replace_default("REQUIRED").to_dict())
