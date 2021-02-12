import os, json

def storeJson(filename, obj):
  dirpath = os.path.dirname(os.path.realpath(__file__))
  filepath = '/problems/' + filename
  with open(dirpath + filepath, 'w+', encoding='utf-8') as f:
    json.dump(obj, f, ensure_ascii=False, indent=2, default=lambda o: o.dict())
