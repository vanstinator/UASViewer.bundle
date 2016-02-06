import requests


class WebToolsAPI:
    """ Interfaces between the UASViewer channel code and the WebTools 2.0 API
    """

    SESSION = None
    BUNDLE_TYPES = None
    CHANNEL_DICT = None
    IS_AUTHENTICATED = False

    def __init__(self, plex_path, web_tools_port, plex_username, plex_password):
        global BUNDLE_TYPES, CHANNEL_DICT, SESSION, IS_AUTHENTICATED
        SESSION = requests.session()
        self.IS_AUTHENTICATED = self.auth_session(plex_path, web_tools_port, plex_username, plex_password)
        self.cache_bundle_data(plex_path, web_tools_port)

    def cache_bundle_data(self, plex_path, web_tools_port):
        """
        :param self:
        :param plex_path:
        :param web_tools_port:
        :return: Bundle Data from WebTools if authenticated properly
        """
        if self.IS_AUTHENTICATED:
            bundles = SESSION.get('http://' + plex_path + ':' + web_tools_port + '/webtools2?module=pms&function=getAllBundleInfo')
            self.BUNDLE_TYPES = self.build_bundle_type_dict(bundles.json())
            self.CHANNEL_DICT = bundles.json().items()

    @staticmethod
    def build_bundle_type_dict(json_obj):
        bundle_types = dict()
        for key, value in json_obj.items():
            for index in value["type"]:
                bundle_types[str(index)] = True
        return bundle_types

    @staticmethod
    def auth_session(plex_path, web_tools_port, plex_username, plex_password):
        payload = {'user': plex_username, 'pwd': plex_password}
        SESSION.post('http://' + plex_path + ':' + web_tools_port + '/login', data=payload)
        return SESSION.cookies['WebTools'] is not None

    @staticmethod
    def install_bundle(bundle_id, plex_path, web_tools_port):
        r = SESSION.get('http://' + plex_path + ':' + web_tools_port + '/webtools2?module=git&function=getGit&url=' + bundle_id)
        if r.status_code == 200:
            return True
        return False
