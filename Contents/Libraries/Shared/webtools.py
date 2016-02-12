import requests
from requests.exceptions import ConnectionError


class WebToolsAPI:
    """
    Interfaces between the UASViewer channel code and the WebTools 2.0 API
    """

    def __init__(self, plex_username, plex_password, webtools_path):
        """
        Instantiate a new authenticated WebToolsAPI session to interact with the WebTools Channel.

        :param plex_username:
        :param plex_password:
        :param plex_path:
        :param web_tools_port:
        :return:
        """

        # Variable Declaration
        self._session = requests.session()
        self.channel_types = None
        self.channel_dict = None
        self._auth_status = False
        self._username = plex_username
        self._password = plex_password
        self._full_path = webtools_path

        # Function calls
        self._auth_session()
        self._cache_bundle_data()

    def _auth_session(self):
        """
        Authenticates a user account against WebTools backend. Sets the auth_status to true if successful. Times out
        after 60 seconds. If WebTools isn't started first this will fail without a long timeout
        :return: boolean
        """
        payload = {'user': self._username, 'pwd': self._password}
        try:
            self._session.post(self._full_path + '/login', data=payload, timeout=60, verify=False)
            if self._session.cookies['WebTools'] is not None:
                self._auth_status = True
        except KeyError:
            # Essentially just swallow the exception. Keeps the logs clean.
            self._auth_status = False
        except ConnectionError:
            self._auth_status = False

    def _cache_bundle_data(self):
        """
        :return: Bundle Data from WebTools if authenticated properly
        """
        if self._auth_status:
            bundles = self._session.get(self._full_path + '/webtools2?module=pms&function=getAllBundleInfo', verify=False)
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
        """
        Pass in the github url of the bundle and it will be installed.
        :param bundle_id:
        :return: boolean
        """
        r = self._session.get(self._full_path + '/webtools2?module=git&function=getGit&url=' + bundle_id, verify=False)
        if r.status_code == 200:
            self._cache_bundle_data()
            return True
        return False

    def uninstall_bundle(self, bundle_name):
        """
       Pass in the bundle name and it will be uninstalled.
        :param bundle_name:
        :return: boolean
        """
        r = self._session.delete(self._full_path + '/webtools2?module=pms&function=delBundle&bundleName=' + bundle_name, verify=False)
        if r.status_code == 200:
            self._cache_bundle_data()
            return True
        return False
