try:
    import DataType
    import Log
    import i18n
    import ConnectCore
except ModuleNotFoundError:
    from . import DataType
    from . import Log
    from . import i18n
    from . import ConnectCore

Version = '0.8.0 beta'
Host = 'ptt.cc'
Port = '23'

# RetryWaitTime 秒後重新連線
RetryWaitTime = 3
# ScreenTimeOut 秒後判定此畫面沒有可辨識的目標
ScreenTimeOut = 3.0

Language = i18n.Language.Chinese
ConnectMode = ConnectCore.ConnectMode.WebSocket
LogLevel = Log.Level.INFO
KickOtherLogin = False


def load():
    global RetryWaitTime
    RetryWaitTime = 3
    global ScreenTimeOut
    ScreenTimeOut = 3.0

    global Language
    Language = i18n.Language.Chinese
    global ConnectMode
    ConnectMode = ConnectCore.ConnectMode.WebSocket
    global LogLevel
    LogLevel = Log.Level.INFO
    global KickOtherLogin
    KickOtherLogin = False
