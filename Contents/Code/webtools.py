import requests


class WebToolsAPI:
    """ Interfaces between the UASViewer channel code and the WebTools 2.0 API
    """

    def __init__(self, plex_username, plex_password, plex_path="localhost", web_tools_port="33400"):
        """
        Instantiate a new authenticated WebToolsAPI session to interact with the WebTools Channel.

        :param plex_username:
        :param plex_password:
        :param plex_path:
        :param web_tools_port:
        :return:
        """

        # Variable Declaration
        self.session = requests.session()
        self.channel_types = None
        self.channel_dict = None
        self._auth_status = False
        self._username = plex_username
        self._password = plex_password
        self._path = plex_path
        self._port = web_tools_port

        # Function calls
        self._auth_session()
        self._cache_bundle_data()

    def _auth_session(self):
        """
        Authenticates a user account against WebTools backend. Sets the auth_status to true if successful.
        :return: boolean
        """
        payload = {'user': self._username, 'pwd': self._password}
        self.session.post('http://' + self._path + ':' + self._port + '/login', data=payload)
        try:
            if self.session.cookies['WebTools'] is not None:
                self._auth_status = True
        except KeyError:
            # Essentially just swallow the exception. Keeps the logs clean.
            self._auth_status = False

    def _cache_bundle_data(self):
        """
        :return: Bundle Data from WebTools if authenticated properly
        """
        if self._auth_status:
            bundles = self.session.get('http://' + self._path + ':' + self._port + '/webtools2?module=pms&function=getAllBundleInfo')
            self._build_bundle_type_dict(bundles.json())
            self.channel_dict = bundles.json().items()

    def _build_bundle_type_dict(self, bundle_json):
        """
        Function used to cache the available bundles
        :param bundle_json:
        """
        self.channel_types = dict()
        for key, value in bundle_json.items():
            for index in value["type"]:
                self.channel_types[str(index)] = True

    def is_authenticated(self):
        """
        :return: current authentication status
        """
        return self._auth_status

    def install_bundle(self, bundle_id):
        # TODO figure out why WebTools doesn't register bundle as installed when installed via this function
        """
        Pass in the github url of the bundle and it will be installed.
        :param bundle_id:
        :return: boolean
        """
        r = self.session.get('http://' + self._path + ':' + self._port + '/webtools2?module=git&function=getGit&url=' + bundle_id)
        if r.status_code == 200:
            return True
        return False

    def uninstall_bundle(self, bundle_id):
        # TODO add uninstall logic
        return False
