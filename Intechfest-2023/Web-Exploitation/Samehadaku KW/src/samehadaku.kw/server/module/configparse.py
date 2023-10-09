import yaml


def parse(filename: str):
    with open(filename, "r") as confile:
        return yaml.load(confile.read(), yaml.Loader)
