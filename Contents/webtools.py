import requests

class WebToolsAPI:

    SESSION = requests.session()
    BUNDLE_TYPES = None
    CHANNEL_DICT = None

    def __init__(self):
        global BUNDLE_TYPES, CHANNEL_DICT, SESSION
        self.auth_session()
        bundles = SESSION.get('http://localhost:33400/webtools2?module=pms&function=getAllBundleInfo')
        BUNDLE_TYPES = self.build_bundle_type_dict(bundles.json())
        CHANNEL_DICT = bundles.json()

    @staticmethod
    def build_bundle_type_dict(json_obj):
        bundle_types = dict()
        for key, value in json_obj.items():
            for index in value["type"]:
                bundle_types[str(index)] = True
        return bundle_types

    @staticmethod
    def auth_session():
        payload = {'user': 'vanstinator', 'pwd': 'CHS50PEDIT3SbrbhXDyvTsu6'}
        SESSION.post('http://localhost:33400/login', data=payload)
