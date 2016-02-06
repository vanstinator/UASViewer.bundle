# UASViewer.bundle
A Plex channel for the Unsupported App Store that works inside Plex

**What is it?**
UASViewer is a Plex Channel that gives you a user interface inside Plex for the Unsupported App Store V2. It's similar to the old UAS plugin in look and feel but it runs on the new hosted back end created by the WebTools 2.X team.

It's currently in a state of early development and is quite buggy. If you run into issues please also post a log file so I can help determine what is going on. Currently one can only browse and install chanels. To uninstall channels you'll need to go use the WebTools UI until I build this into the UASViewer. **Please be aware the due to how the channel system works if you share channels with users they will have full access to install channels.** I'll try to address this somehow in the future, for now just avoid the plugin if this is a problem.

Manual install: https://github.com/vanstinator/UASViewer.bundle/releases

Also available on the UAS V2

**Known Issues**

* Only works with http
* Doesn't usually start cleanly with Plex if it starts before WebTools does. Usually trying once or twice will get this working smoothly until the next restart.

**Roadmap**

* Uninstall channels
* Lock out none-admin users (maybe)

I'll take code submissions once I get a stable release.
