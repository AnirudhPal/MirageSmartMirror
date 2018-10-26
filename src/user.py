import json
class User:
  def __init__(name):
    with open(name + '.json') as data_file:
        data = json.load(data_file)
    pprint(data)
    parsed_json = json.loads(json_string)
