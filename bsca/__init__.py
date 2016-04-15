__version__ = '0.0.1'

from protecodesc.config import ClientConfig
from protecodesc.protecodesc import ProtecodeSC
from collections import Counter

import json


class BinarySCABirthCert:
    def __init__(self):
        self.processed = None
        self.cfg = ClientConfig()
        username, password = self.cfg.credentials()
        if not (username and password):
            raise IOError("Required ProtecodeSC config, please use protecodesc tool to set those")

        self.protecode = ProtecodeSC(creds=(username, password), host = self.cfg.get_host())

    def analyze_composition(self, components):

        counts = Counter()
        duplicates = Counter()
        complist = []

        for c in components:
            extended = c.get('extended-objects')
            ctype = extended[0]['type']
            counts[ctype] += 1
            if len(extended) > 1:
                duplicates[c['lib']] += (len(extended) - 1)

            component = {
                'name': c['lib'],
                'type': ctype,
                'sha1s': list(set([i['sha1'] for i in c['extended-objects']]))
            }

            cver = c['version']
            if cver:
                component['version'] = cver

            cdata = self.protecode.component(c['lib'], version=c.get('version', None))
            print cdata
            cs = cdata.get('component', []) 
            if len(cs) > 0 and cs[0].get('homepage'):
                component['homepage'] = cs[0].get('homepage')

            complist.append(component)

        res = {
            'counts': { i: counts[i] for i in counts },
            'duplicates': { i: duplicates[i] for i in duplicates },
            'components': complist
        }
        return res

    def analyze_file(self, to_analyze):
        res = self.protecode.upload_file(to_analyze, group=self.cfg.get_default_group(), poll=True)
        data = res.get('results', {})

        self.processed = {
            'analyzed': data.get('last_updated'),
            'report_url': data.get('report_url'),
            'sha1': data.get('sha1sum'),
            'filename': data.get('filename'),
            'composition': self.analyze_composition(data.get('components'))
        }


    def dump_cert(self, target):
        print json.dumps(self.processed, indent=4)



