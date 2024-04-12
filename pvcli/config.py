import yaml
import sys

CONF = None

# usage： Config().cli["cec_mod_db"]

CNF = None

class Config:
    def __init__(self, path=None):
        global CNF
        if CNF == None:
            if path == None:
                print("The configuration file must be obtained")
                sys.exit(1)
            CNF = self.load_config(path)

    def load_config(self,path):
        with open(path, 'r') as stream:
            try:
                config = yaml.safe_load(stream)
                return config
            except yaml.YAMLError as e:
                print(e)
                return None

    @property
    def cli(self):
        return CNF['cli']

