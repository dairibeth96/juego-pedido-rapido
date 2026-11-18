[app]
title = Pedido Rapido
package.name = pedidorapido
package.domain = org.tujuego
source.include_exts = py,png,jpg,kv,atlas
requirements = python3,pygame
orientation = portrait
android.permissions = INTERNET

# (int) Android API to target
android.api = 33

# (int) Minimum API your APK will support
android.min_api = 21

[buildozer]
log_level = 2
android.architectures = arm64-v8a, armeabi-v7a