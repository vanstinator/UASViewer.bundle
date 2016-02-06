import webtools

PREFIX = "/applications/UASViewer"
NAME = 'UASViewer'
ART = 'background.jpg'
ICON = 'icon-default.png'  # TODO find a channel icon


def Start():
    """ Run by Plex when the server starts
    """
    Log('Starting UASViewer')
    ObjectContainer.title1 = NAME
    # Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
    # ObjectContainer.view_group = 'List'
    ValidatePrefs()


@handler(PREFIX, NAME, art=R(ART), thumb=R(ICON))
@route(PREFIX + '/MainMenu')
def MainMenu(message=""):
    oc = ObjectContainer(no_cache=True, no_history=True, replace_parent=True)
    oc.message = message
    for value in UAS.BUNDLE_TYPES:
        oc.add(DirectoryObject(key=Callback(CategoryMenu, bundle_type=value), title=value))
    return oc


@route(PREFIX + '/Category')
def CategoryMenu(bundle_type):
    oc = ObjectContainer(no_cache=True, no_history=True, replace_parent=True)
    for key, value in UAS.CHANNEL_DICT:
        if bundle_type in value["type"]:
            Log('http://' + Prefs['PLEX_PATH'] + ':' + Prefs['WEB_TOOLS_PORT'] + '/uas/Resources/' + value["icon"])
            oc.add(DirectoryObject(key=Callback(InstallChannel, id=key),
                                   title=value["title"],
                                   summary=value["description"],
                                   thumb=Callback(Thumb,
                                                  url='http://'
                                                        + Prefs['PLEX_PATH']
                                                        + ':'
                                                        + Prefs['WEB_TOOLS_PORT']
                                                        + '/uas/Resources/'
                                                        + value["icon"]
                                                  )
                                   )
                   )
    return oc

@route(PREFIX + '/InstallChannel')
def InstallChannel(id):
    if UAS.install_bundle(id, Prefs['PLEX_PATH'], Prefs['WEB_TOOLS_PORT']):
        return MainMenu(message="Channel Installed Successfully.")
    return MainMenu(message="Channel Installation Failed. Please see WebTools logs.")

@route(PREFIX + '/ValidatePrefs')
def ValidatePrefs():
    """ Called by Plex every time the Preferences change
    """
    global UAS
    Log('Validating Prefs')
    Log('Initializing WebTools Session')
    UAS = webtools.WebToolsAPI(Prefs['PLEX_PATH'], Prefs['WEB_TOOLS_PORT'], Prefs['PLEX_USERNAME'],
                               Prefs['PLEX_PASSWORD'])

def Thumb(url):
    """ Go try to get the thumbnail and cache it into memory
    """
    try:
        data = HTTP.Request(url, cacheTime=CACHE_1MONTH).content
        return DataObject(data, 'image/jpeg')
    except:
        return Redirect(R(ICON))
