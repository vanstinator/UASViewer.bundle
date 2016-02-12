import webtools

PREFIX = "/applications/UASViewer"
NAME = 'UASViewer'
ART = 'background.jpg'
ICON = 'icon-default.png'

####################################################################################################

def Start():
    """
    Run by Plex when the server starts
    """

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

    Log('Starting UASViewer')
    ObjectContainer.title1 = NAME
    ValidatePrefs()


####################################################################################################
@handler(PREFIX, NAME, art=R(ART), thumb=R(ICON))
@route(PREFIX + '/MainMenu')
def MainMenu(message=""):
    oc = ObjectContainer(no_cache=True, no_history=True, replace_parent=True)
    oc.message = message
    oc.add(DirectoryObject(key=Callback(DeadEnd), title="ANY USER CAN ACCESS THIS CHANNEL"))
    try:
        for value in UAS.channel_types:
            if Prefs['HIDE_ADULT']:
                if value != "Adult":
                    oc.add(DirectoryObject(key=Callback(CategoryMenu, bundle_type=value), title=value))
            else:
                oc.add(DirectoryObject(key=Callback(CategoryMenu, bundle_type=value), title=value))
        oc.add(DirectoryObject(key=Callback(InstalledMenu), title="Installed Channels"))
        oc.add(PrefsObject(title=L('Preferences'), thumb=R(ICON)))
        return oc
    except:
        ValidatePrefs()


def DeadEnd():
    return


####################################################################################################
@route(PREFIX + '/Category')
def CategoryMenu(bundle_type):
    oc = ObjectContainer(view_group="InfoList", title2=bundle_type + " Channels")
    for key, value in UAS.channel_dict:
        if bundle_type in value["type"]:
            if Prefs['HIDE_ADULT']:
                if "Adult" not in value["type"]:
                    oc.add(ChannelItem(key, value))
            else:
                oc.add(ChannelItem(key, value))
    return oc


####################################################################################################
@route(PREFIX + '/Installed')
def InstalledMenu():
    oc = ObjectContainer(no_cache=True, no_history=True, replace_parent=True)
    for key, value in UAS.channel_dict:
        if value["date"]:
            oc.add(ChannelItem(key, value))
    return oc


####################################################################################################
def ChannelItem(key, value):
    return DirectoryObject(key=Callback(ChannelInfo, key=key, name=value["bundle"], date=value["date"]),
                                           title=value["title"],
                                           summary=value["description"],
                                           thumb=Callback(Thumb,
                                                          url=
                                                          webtools_path +
                                                          '/uas/Resources/' +
                                                          value["icon"]))


####################################################################################################
@route(PREFIX + '/ChannelInfo')
def ChannelInfo(key, name, date):
    oc = ObjectContainer(no_cache=True, no_history=True, replace_parent=True)
    if date is not None:
        oc.add(DirectoryObject(key=Callback(UninstallChannel, name=name),
                               title="Uninstall Channel"))
    else:
        oc.add(DirectoryObject(key=Callback(InstallChannel, id=key),
                               title="Install Channel"))
    return oc


####################################################################################################
@route(PREFIX + '/InstallChannel')
def InstallChannel(id):
    if UAS.install_bundle(id):
        return MainMenu(message="Channel Installed Successfully.")
    return MainMenu(message="Channel Installation Failed. Please see WebTools logs.")


####################################################################################################
@route(PREFIX + '/UninstallChannel')
def UninstallChannel(name):
    if UAS.uninstall_bundle(name):
        return MainMenu(message="Channel Uninstalled Successfully.")
    return MainMenu(message="Channel Uninstallation Failed. Please see WebTools logs.")


####################################################################################################
@route(PREFIX + '/ValidatePrefs')
def ValidatePrefs():
    """ Called by Plex every time the Preferences change
    """
    global UAS, webtools_path
    Log('Validating Prefs')
    Log('Initializing WebTools Session')
    if Prefs['USE_SSL'] is not False:
        webtools_path = 'https://127.0.0.1:' + Prefs['WEB_TOOLS_PORT']
    else:
        webtools_path = 'http://127.0.0.1:' + Prefs['WEB_TOOLS_PORT']

    UAS = None
    UAS = webtools.WebToolsAPI(Prefs['PLEX_USERNAME'],
                               Prefs['PLEX_PASSWORD'],
                               webtools_path)
    if UAS.is_authenticated():
        Log('Connected to WebTools UAS successfully')
    else:
        Log('Connection to WebTools UAS was unsuccessful')


####################################################################################################
def Thumb(url):
    """ Go try to get the thumbnail and cache it into memory
    """
    Log('Attempting to cache image ' + url)
    try:
        data = HTTP.Request(url, cacheTime=CACHE_1MONTH).content
        Log('Caching image was successful')
        return DataObject(data, 'image/jpeg')
    except:
        Log('Caching image failed. Deferring to default channel icon')
        return Redirect(R(ICON))
