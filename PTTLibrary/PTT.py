﻿import sys
import time

try:
    from . import DataType
    from . import Config
    from . import Util
    from . import i18n
    from . import Exceptions
    from . import ConnectCore
    from . import ErrorCode
    from . import Log
    from . import Synchronize
except FileNotFoundError:
    import DataType
    import Config
    import Util
    import i18n
    import Exceptions
    import ConnectCore
    import ErrorCode
    import Log
    import Synchronize

Version = Config.Version

ErrorCode = ErrorCode.ErrorCode()
Language = i18n.Language
ConnectMode = ConnectCore.ConnectMode
LogLevel = Log.Level
Command = ConnectCore.Command


class Library(Synchronize.SynchronizeAllMethod):
    def __init__(self,
                 Language: int=0,
                 ConnectMode: int=0,
                 LogLevel: int=0,
                 ):
        if LogLevel == 0:
            LogLevel = Config.LogLevel
        elif not Util.checkRange(Log.Level, LogLevel):
            raise Exceptions.ParameterError('Unknow LogLevel', LogLevel)
        else:
            Config.LogLevel = LogLevel

        if Language == 0:
            Language = Config.Language
        elif not Util.checkRange(i18n.Language, Language):
            raise Exceptions.ParameterError('Unknow language', Language)
        else:
            Config.Language = Language
        i18n.load(Language)

        if ConnectMode == 0:
            ConnectMode = Config.ConnectMode
        elif not Util.checkRange(DataType.ConnectMode, ConnectMode):
            raise Exceptions.ParameterError('Unknow ConnectMode',
                                            ConnectMode)
        else:
            Config.ConnectMode = ConnectMode
        self._ConnectCore = ConnectCore.API(ConnectMode)

        Log.showValue(Log.Level.INFO, [
            i18n.PTT,
            i18n.Library,
            ' v ' + Version,
            ],
            i18n.Init
        )

    def login(self, ID: str, Password: str, KickOtherLogin: bool=False):

        def KickOtherLoginDisplayMsg():
            if Config.KickOtherLogin:
                return i18n.KickOtherLogin
            return i18n.NotKickOtherLogin
        
        def KickOtherLoginResponse(Screen):
            if Config.KickOtherLogin:
                return 'y' + ConnectCore.Command.Enter
            return 'n' + ConnectCore.Command.Enter

        Config.KickOtherLogin = KickOtherLogin

        self._ConnectCore.connect()

        TargetList = [
            ConnectCore.TargetUnit(
                i18n.LoginSuccess,
                '我是' + ID,
                BreakDetect=True
            ),
            ConnectCore.TargetUnit(
                i18n.ErrorIDPW,
                '密碼不對或無此帳號',
                BreakDetect=True
            ),
            ConnectCore.TargetUnit(
                i18n.SigningUnPleaseWait,
                '登入中，請稍候',
            ),
            ConnectCore.TargetUnit(
                KickOtherLoginDisplayMsg,
                '您想刪除其他重複登入的連線嗎',
                KickOtherLoginResponse,
            ),
            ConnectCore.TargetUnit(
                i18n.SigningUpdate,
                '正在更新與同步線上使用者及好友名單',
            ),
            ConnectCore.TargetUnit(
                i18n.SigningUpdate,
                '任意鍵繼續',
            ),
        ]

        Msg = ID + ',' + ConnectCore.Command.Enter + Password + ConnectCore.Command.Enter
        index = self._ConnectCore.send(Msg, TargetList)
        # Log.showValue(Log.Level.INFO, 'index', index)

        if index != 0:
            raise ConnectCore.LoginError()
        return ErrorCode.Success

    def logout(self):
        pass

    def log(self, Msg):
        Log.log(Log.Level.INFO, Msg)

if __name__ == '__main__':

    print('PTT Library v ' + Version)
    print('Developed by PTT CodingMan')
