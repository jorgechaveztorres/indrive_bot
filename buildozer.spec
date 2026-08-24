[app]
title = InDrive Bot
package.name = indrivebot
package.domain = org.kike
source.dir = .
source.include_exts = py,json
version = 1.0
requirements = python3,requests
orientation = portrait
fullscreen = 0
android.permissions = INTERNET, WAKE_LOCK, SYSTEM_ALERT_WINDOW

[buildozer]
log_level = 2
warn_on_root = 1
android.sdk = 30
android.min_api = 21
android.ndk = 25b
android.build_tools_version = 30.0.3
android.accept_sdk_license = True
