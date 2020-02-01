try:
    from . import version
    from . import data_type
    from . import log
    from . import i18n
    from . import ConnectCore
except ModuleNotFoundError:
    import version
    import data_type
    import log
    import i18n
    import ConnectCore


class Config:
    Version = version.V

    # retry_wait_time 秒後重新連線
    retry_wait_time = 3

    # screen_long_timeout 秒後判定此畫面沒有可辨識的目標
    # 適用於需要特別等待的情況，例如: 剔除其他登入、發文等等
    # 建議不要低於 10 秒，剔除其他登入最長可能會花費約六到七秒
    screen_long_timeout = 10.0

    # screen_post_timeout 秒後判定此畫面沒有可辨識的目標
    # 適用於貼文等待的情況，建議不要低於 10 秒
    screen_post_timeout = 60.0

    # ScreenLTimeOut 秒後判定此畫面沒有可辨識的目標
    screen_timeout = 3.0

    # 預設語言
    language = i18n.Language.Chinese

    # 預設 log 等級
    log_level = log.Level.INFO

    # 預設不剔除其他登入
    kick_other_login = False

    # 預設登入 PTT1
    host = data_type.host.PTT1

    log_handler = None
