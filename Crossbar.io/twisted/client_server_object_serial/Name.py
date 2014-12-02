#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
   import ujson
   json_lib = ujson
   json_loads = ujson.loads
   json_dumps = lambda x: ujson.dumps(x, ensure_ascii=False)
except:
   import json
   json_lib = json
   json_loads = json.loads
   json_dumps = json.dumps

class Name(object):
    def __init__(self):
        self.nom = "Aboule"
        self.prenom = "Le Fric"

    @property
    def full_name(self):
        return "{} {}".format(self.nom, self.prenom)

    def test(self):
        return 81
