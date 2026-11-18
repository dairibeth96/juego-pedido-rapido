[app]
title = Pedido Rapido
package.name = pedidorapido
package.domain = org.tujuego
source.include_exts = py,png,jpg,kv,atlas

# (str) Source directory where the application lives
source.dir = .

# (str) Application versioning
version = 0.1

requirements = python3,pygame
orientation = portrait
android.permissions = INTERNET

# (int) Android API to target
android.api = 33

# (int) Minimum API your APK will support
android.min_api = 21

# (bool) Indicate whether you accept the Android SDK License
android.accept_sdk_license = True

[buildozer]
log_level = 2
android.architectures = arm64-v8a, armeabi-v7a