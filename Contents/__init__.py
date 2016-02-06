import webtools


PREFIX = "/applications/UASViewer"
NAME = 'UASViewer'
ART = 'background.jpg'
ICON = 'plexwink.png'
# PREFS_ICON = 'plexwink.png'
# PROFILE_ICON = 'plexwink.png'


def Start():
    """ Run by Plex when the server starts
    """
    Log('Starting UASViewer')
    ObjectContainer.title = NAME
    ValidatePrefs()


@handler(PREFIX, NAME, art=R(ART), thumb=R(ICON))
def MainMenu(header=NAME, message="Hello"):
    oc = ObjectContainer(no_cache=True, no_history=True, replace_parent=True)
    for key, value in UAS.BUNDLE_TYPES:
        oc.add(DirectoryObject(key=Callback(MainMenu), title=key))


@route(PREFIX + '/ValidatePrefs')
def ValidatePrefs():
    """ Called by Plex every time the Preferences change
    """
    global UAS
    Log('Validating Prefs')
    Log('Initializing WebTools Session')
    UAS = webtools.WebToolsAPI(Prefs['PMS_ADDRESS'], Prefs['PMS_PORT'], Prefs['PLEX_USERNAME'], Prefs['PLEX_PASSWORD'])
