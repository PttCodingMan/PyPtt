try:
    from . import data_type
    from . import i18n
    from . import ConnectCore
    from . import log
    from . import screens
    from . import exceptions
    from . import Command
except ModuleNotFoundError:
    import data_type
    import i18n
    import ConnectCore
    import log
    import screens
    import exceptions
    import Command


def logout(api) -> None:

    CmdList = []
    CmdList.append(Command.GoMainMenu)
    CmdList.append('g')
    CmdList.append(Command.Enter)
    CmdList.append('y')
    CmdList.append(Command.Enter)

    Cmd = ''.join(CmdList)

    TargetList = [
        ConnectCore.TargetUnit(
            [
                i18n.logout,
                i18n.Success,
            ],
            '任意鍵',
            break_detect=True,
        ),
    ]

    log.log(
        api.config,
        log.Level.INFO,
        [
            i18n.Start,
            i18n.logout
        ]
    )

    try:
        api.connect_core.send(Cmd, TargetList)
        api.connect_core.close()
    except exceptions.ConnectionClosed:
        pass
    except RuntimeError:
        pass

    api._loginStatus = False

    log.show_value(
        api.config,
        log.Level.INFO,
        i18n.logout,
        i18n.Done
    )


def login(
        api,
        ID,
        Password,
        kick_other_login):

    if api._loginStatus:
        api.logout()

    api.config.kick_other_login = kick_other_login

    def kick_other_loginDisplayMsg():
        if api.config.kick_other_login:
            return i18n.kick_other_login
        return i18n.Notkick_other_login

    def kick_other_loginResponse(Screen):
        if api.config.kick_other_login:
            return 'y' + Command.Enter
        return 'n' + Command.Enter

    if len(Password) > 8:
        Password = Password[:8]

    ID = ID.strip()
    Password = Password.strip()

    api._ID = ID
    api._Password = Password

    log.show_value(
        api.config,
        log.Level.INFO,
        [
            i18n.login,
            i18n.ID
        ],
        ID
    )

    api.config.kick_other_login = kick_other_login

    api.connect_core.connect()

    TargetList = [
        ConnectCore.TargetUnit(
            i18n.HasNewMailGotoMainMenu,
            '你有新信件',
            response=Command.GoMainMenu,
        ),
        ConnectCore.TargetUnit(
            i18n.loginSuccess,
            screens.Target.MainMenu,
            break_detect=True
        ),
        ConnectCore.TargetUnit(
            i18n.GoMainMenu,
            '【看板列表】',
            response=Command.GoMainMenu,
        ),
        ConnectCore.TargetUnit(
            i18n.ErrorIDPW,
            '密碼不對或無此帳號',
            break_detect=True,
            exceptions=exceptions.WrongIDorPassword()
        ),
        ConnectCore.TargetUnit(
            i18n.loginTooOften,
            '登入太頻繁',
            break_detect=True,
            exceptions=exceptions.loginTooOften()
        ),
        ConnectCore.TargetUnit(
            i18n.SystemBusyTryLater,
            '系統過載',
            break_detect=True,
        ),
        ConnectCore.TargetUnit(
            i18n.DelWrongPWRecord,
            '您要刪除以上錯誤嘗試的記錄嗎',
            response='y' + Command.Enter,
        ),
        ConnectCore.TargetUnit(
            i18n.MailBoxFull,
            '您保存信件數目',
            response=Command.GoMainMenu,
        ),
        ConnectCore.TargetUnit(
            i18n.PostNotFinish,
            '請選擇暫存檔 (0-9)[0]',
            response=Command.Enter,
        ),
        ConnectCore.TargetUnit(
            i18n.PostNotFinish,
            '有一篇文章尚未完成',
            response='Q' + Command.Enter,
        ),
        ConnectCore.TargetUnit(
            i18n.SigningUnPleaseWait,
            '登入中，請稍候',
        ),
        ConnectCore.TargetUnit(
            kick_other_loginDisplayMsg,
            '您想刪除其他重複登入的連線嗎',
            response=kick_other_loginResponse,
        ),
        ConnectCore.TargetUnit(
            i18n.AnyKeyContinue,
            '任意鍵',
            response=Command.Enter
        ),
        ConnectCore.TargetUnit(
            i18n.SigningUpdate,
            '正在更新與同步線上使用者及好友名單',
        ),
    ]

    CmdList = []
    CmdList.append(ID)
    CmdList.append(Command.Enter)
    CmdList.append(Password)
    CmdList.append(Command.Enter)

    Cmd = ''.join(CmdList)

    index = api.connect_core.send(
        Cmd,
        TargetList,
        screen_timeout=api.config.screen_long_timeout,
        refresh=False,
        secret=True
    )

    if TargetList[index].get_display_msg() != i18n.loginSuccess:
        OriScreen = api.connect_core.get_screen_queue()[-1]
        print(OriScreen)
        raise exceptions.loginError()

    OriScreen = api.connect_core.get_screen_queue()[-1]
    if '> (' in OriScreen:
        api.cursor = data_type.Cursor.New
        log.log(
            api.config,
            log.Level.DEBUG,
            i18n.NewCursor
        )
    else:
        api.cursor = data_type.Cursor.Old
        log.log(
            api.config,
            log.Level.DEBUG,
            i18n.OldCursor
        )

    if api.cursor not in screens.Target.InBoardWithCursor:
        screens.Target.InBoardWithCursor.append('\n' + api.cursor)

    api._UnregisteredUser = False
    if '(T)alk' not in OriScreen:
        api._UnregisteredUser = True
    if '(P)lay' not in OriScreen:
        api._UnregisteredUser = True
    if '(N)amelist' not in OriScreen:
        api._UnregisteredUser = True

    if api._UnregisteredUser:
        print(OriScreen)
        log.log(
            api.config,
            log.Level.INFO,
            i18n.UnregisteredUserCantUseAllAPI
        )

    api._loginStatus = True
