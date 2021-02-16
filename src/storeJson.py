import os, json

def storeJson(filepath, obj):
  with open(filepath, 'w+', encoding='utf-8') as f:
    json.dump(obj, f, ensure_ascii=False, indent=2, default=lambda o: o.dict())
