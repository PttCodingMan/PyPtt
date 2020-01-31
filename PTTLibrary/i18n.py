
try:
    from . import Util
except ModuleNotFoundError:
    import Util


class Language(object):

    Chinese = 1
    English = 2

    MinValue = Chinese
    MaxValue = English


LanguageList = [
    Language.Chinese,
    Language.English,
]

Connect = None
Start = None
ConnectMode = None
ConnectMode_Telnet = None
ConnectMode_WebSocket = None
Active = None
ErrorParameter = None
ConnectCore = None
PTT = None
PTT2 = None
Init = None
Done = None
i18n = None
Library = None
Fail = None
Success = None
Prepare = None
Info = None
Debug = None
Again = None
ErrorIDPW = None
ScreenNoMatchTarget = None
SigningUnPleaseWait = None
Msg = None
SigningUpdate = None
SendMsg = None
KickOtherLogin = None
NotKickOtherLogin = None
AnyKeyContinue = None
Login = None
LoginSuccess = None
LoginFail = None
MailBoxFull = None
PostNotFinish = None
SystemBusyTryLater = None
DelWrongPWRecord = None
Logout = None
SpendTime = None
GetPTTTime = None
LoginTooOften = None
MustBe = None
String = None
Integer = None
Boolean = None
ID = None
Password = None
Board = None
BothInput = None
NoInput = None
CatchPost = None
PostDeleted = None
BrowsePost = None
CatchIP = None
GetPush = None
Update = None
Push = None
Date = None
Content = None
Author = None
Title = None
UnknownError = None
RequireLogin = None
HasPushPermission = None
HasPostPermission = None
NoPermission = None
SaveFile = None
SelectSignature = None
FindNewestIndex = None
OutOfRange = None
MustSmallOrEqual = None
VotePost = None
SubstandardPost = None
DoNothing = None
NoFastPush = None
OnlyArrow = None
GetUser = None
NoSuchUser = None
WaterBall = None
UserOffline = None
SetCallStatus = None
Throw = None
NoWaterball = None
BrowseWaterball = None
LanguageModule = None
English = None
ChineseTranditional = None
GetCallStatus = None
NoMoney = None
InputID = None
InputMoney = None
AuthenticationHasNotExpired = None
VerifyID = None
TradingInProgress = None
Transaction = None
MoneyTooFew = None
ConstantRedBag = None
SendMail = None
Select = None
SignatureFile = None
NoSignatureFile = None
SelfSaveDraft = None
MailBox = None
NoSuchBoard = None
HideSensitiveInfor = None
PostFormatError = None
LogHandler = None
NewCursor = None
OldCursor = None
PostNoContent = None
ConnectionClosed = None
BoardList = None
UnregisteredUserCantUseAllAPI = None
UnregisteredUserCantUseThisAPI = None
MultiThreadOperate = None
HasNewMailGotoMainMenu = None
UseTooManyResources = None
Host = None
PTT2NotSupport = None
AnimationPost = None
RestoreConnection = None
NoPush = None
NoResponse = None
ReplyBoard = None
ReplyMail = None
ReplyBoard_Mail = None
UseTheOriginalTitle = None
QuoteOriginal = None
EditPost = None
RespondSuccess = None
ForcedWrite = None
NoPost = None
NeedModeratorPermission = None
NewSettingsHaveBeenSaved = None
NoChanges = None
Mark = None
MarkPost = None
DelAllMarkPost = None
NoSuchPost = None
GoMainMenu = None
CanNotUseSearchPostCodeF = None
FavouriteBoardList = None
bucket = None
UserHasPreviouslyBeenBanned = None
InputBucketDays_Reason = None
UnconfirmedPost = None
Reading = None
ReadComplete = None
QuitUserProfile = None


def specific_load(language, lang_list):
    global LanguageList

    if len(LanguageList) != len(lang_list):
        raise ValueError('SpecificLoad LangList legnth error')

    if language not in LanguageList:
        raise ValueError('SpecificLoad Unknow language', language)
    return lang_list[LanguageList.index(language)]


def replace(string, *args):
    # for i in range(len(args)):
    for i, _ in enumerate(args):
        target = str(args[i])
        string = string.replace('{Target' + str(i) + '}', target)
    return string


def load(language):
    if not Util.check_range(Language, language):
        raise ValueError('Language', language)

    global Connect
    Connect = specific_load(language, [
        '連線',
        'Connect',
    ])

    global Start
    Start = specific_load(language, [
        '開始',
        'Start',
    ])

    global ConnectMode
    ConnectMode = specific_load(language, [
        Connect + '模式',
        Connect + 'mode',
    ])

    global ConnectMode_Telnet
    ConnectMode_Telnet = specific_load(language, [
        'Telnet',
        'Telnet',
    ])

    global ConnectMode_WebSocket
    ConnectMode_WebSocket = specific_load(language, [
        'WebSocket',
        'WebSocket',
    ])

    global Active
    Active = specific_load(language, [
        '啟動',
        'Active',
    ])

    global ErrorParameter
    ErrorParameter = specific_load(language, [
        '參數錯誤',
        'Wrong parameter',
    ])

    global ConnectCore
    ConnectCore = specific_load(language, [
        '連線核心',
        'Connect Core',
    ])

    global PTT
    PTT = specific_load(language, [
        '批踢踢',
        'PTT',
    ])

    global PTT2
    PTT2 = specific_load(language, [
        '批踢踢兔',
        'PTT2',
    ])

    global Init
    Init = specific_load(language, [
        '初始化',
        'initialize',
    ])

    global Done
    Done = specific_load(language, [
        '完成',
        'Done',
    ])

    global i18n
    i18n = specific_load(language, [
        '多國語系',
        'i18n',
    ])

    global Library
    Library = specific_load(language, [
        '函式庫',
        'Library',
    ])

    global Fail
    Fail = specific_load(language, [
        '失敗',
        'Fail',
    ])

    global Success
    Success = specific_load(language, [
        '成功',
        'Success',
    ])

    global Prepare
    Prepare = specific_load(language, [
        '準備',
        'Prepare',
    ])

    global Info
    Info = specific_load(language, [
        '資訊',
        'INFO',
    ])

    global Debug
    Debug = specific_load(language, [
        '除錯',
        'DBUG',
    ])

    global Again
    Again = specific_load(language, [
        '重新',
        'Re',
    ])

    global ErrorIDPW
    ErrorIDPW = specific_load(language, [
        '密碼不對或無此帳號',
        'Wrong password or no such id',
    ])

    global ScreenNoMatchTarget
    ScreenNoMatchTarget = specific_load(language, [
        '畫面無法辨識',
        'This screen is not recognized',
    ])

    global SigningUnPleaseWait
    SigningUnPleaseWait = specific_load(language, [
        '登入中，請稍候',
        'Signing in, please wait',
    ])

    global Msg
    Msg = specific_load(language, [
        '訊息',
        'Message',
    ])

    global SigningUpdate
    SigningUpdate = specific_load(language, [
        '更新與同步線上使用者及好友名單',
        'Updating and synchronizing online users and friends list',
    ])

    global SendMsg
    SendMsg = specific_load(language, [
        '送出訊息',
        'Send Msg',
    ])

    global KickOtherLogin
    KickOtherLogin = specific_load(language, [
        '剔除其他登入',
        'Kick other login',
    ])

    global NotKickOtherLogin
    NotKickOtherLogin = specific_load(language, [
        '不剔除其他登入',
        'Not kick other login',
    ])

    global AnyKeyContinue
    AnyKeyContinue = specific_load(language, [
        '請按任意鍵繼續',
        'Any key to continue',
    ])

    global Login
    Login = specific_load(language, [
        '登入',
        'Login',
    ])

    global LoginSuccess
    LoginSuccess = specific_load(language, [
        Login + Success,
        Login + ' ' + Success,
    ])

    global LoginFail
    LoginFail = specific_load(language, [
        Login + Fail,
        Login + ' ' + Fail,
    ])

    global MailBoxFull
    MailBoxFull = specific_load(language, [
        '郵件已滿',
        'Mail box is full',
    ])

    global PostNotFinish
    PostNotFinish = specific_load(language, [
        '文章尚未完成',
        'Post is not finish',
    ])

    global SystemBusyTryLater
    SystemBusyTryLater = specific_load(language, [
        '系統負荷過重, 請稍後再試',
        'System is overloaded, please try again later',
    ])

    global DelWrongPWRecord
    DelWrongPWRecord = specific_load(language, [
        '刪除以上錯誤嘗試的記錄',
        'Delete the record of the wrong password',
    ])

    global Logout
    Logout = specific_load(language, [
        '登出',
        'Logout',
    ])

    global SpendTime
    SpendTime = specific_load(language, [
        '花費時間',
        'Spend time',
    ])

    global GetPTTTime
    GetPTTTime = specific_load(language, [
        '取得批踢踢時間',
        'Get PTT time',
    ])

    global LoginTooOften
    LoginTooOften = specific_load(language, [
        '登入太頻繁',
        'Login too often',
    ])

    global MustBe
    MustBe = specific_load(language, [
        '必須是',
        'must be',
    ])

    global String
    String = specific_load(language, [
        '字串',
        'String',
    ])

    global Integer
    Integer = specific_load(language, [
        '整數',
        'Integer',
    ])

    global Boolean
    Boolean = specific_load(language, [
        '布林值',
        'Boolean',
    ])

    global ID
    ID = specific_load(language, [
        '帳號',
        'ID',
    ])

    global Password
    Password = specific_load(language, [
        '密碼',
        'Password',
    ])

    global Board
    Board = specific_load(language, [
        '看板',
        'Board',
    ])

    global BothInput
    BothInput = specific_load(language, [
        '同時輸入',
        'Both input',
    ])

    global NoInput
    NoInput = specific_load(language, [
        '沒有輸入',
        'No input',
    ])

    global CatchPost
    CatchPost = specific_load(language, [
        '取得文章',
        'Catch post',
    ])

    global PostDeleted
    PostDeleted = specific_load(language, [
        '文章已經被刪除',
        'Post has been deleted',
    ])

    global BrowsePost
    BrowsePost = specific_load(language, [
        '瀏覽文章',
        'Browse post',
    ])

    global CatchIP
    CatchIP = specific_load(language, [
        '取得 IP',
        'Catch IP',
    ])

    global GetPush
    GetPush = specific_load(language, [
        '取得推文',
        'Get push',
    ])

    global Update
    Update = specific_load(language, [
        '更新',
        'Update',
    ])

    global Push
    Push = specific_load(language, [
        '推文',
        'Push',
    ])

    global Date
    Date = specific_load(language, [
        '日期',
        'Date',
    ])

    global Content
    Content = specific_load(language, [
        '內文',
        'Content',
    ])

    global Author
    Author = specific_load(language, [
        '作者',
        'Author',
    ])

    global Title
    Title = specific_load(language, [
        '標題',
        'Title',
    ])

    global UnknownError
    UnknownError = specific_load(language, [
        '未知錯誤',
        'Unknow Error',
    ])

    global RequireLogin
    RequireLogin = specific_load(language, [
        '請先' + Login,
        'Please ' + Login + ' first',
    ])

    global HasPushPermission
    HasPushPermission = specific_load(language, [
        '使用者擁有推文權限',
        'User Has Push Permission',
    ])

    global HasPostPermission
    HasPostPermission = specific_load(language, [
        '使用者擁有貼文權限',
        'User Has Post Permission',
    ])

    global NoPermission
    NoPermission = specific_load(language, [
        '使用者沒有權限',
        'User Has No Permission',
    ])

    global SaveFile
    SaveFile = specific_load(language, [
        '儲存檔案',
        'Save File',
    ])

    global SelectSignature
    SelectSignature = specific_load(language, [
        '選擇簽名檔',
        'Select Signature',
    ])

    global FindNewestIndex
    FindNewestIndex = specific_load(language, [
        '找到最新編號',
        'Find Newest Index',
    ])

    global OutOfRange
    OutOfRange = specific_load(language, [
        '超出範圍',
        'Out Of Range',
    ])

    global MustSmallOrEqual
    MustSmallOrEqual = specific_load(language, [
        '必須小於等於',
        'Must be less than or equal',
    ])

    global VotePost
    VotePost = specific_load(language, [
        '投票文章',
        'Vote Post',
    ])

    global SubstandardPost
    SubstandardPost = specific_load(language, [
        '不合規範文章',
        'Substandard Post',
    ])

    global DoNothing
    DoNothing = specific_load(language, [
        '不處理',
        'Do Nothing',
    ])

    global NoFastPush
    NoFastPush = specific_load(language, [
        '禁止快速連續推文',
        'No Fast Push',
    ])

    global OnlyArrow
    OnlyArrow = specific_load(language, [
        '使用加註方式',
        'Arrow Only in Push',
    ])

    global GetUser
    GetUser = specific_load(language, [
        '取得使用者',
        'Get User',
    ])

    global NoSuchUser
    NoSuchUser = specific_load(language, [
        '無該使用者',
        'No such user',
    ])

    global WaterBall
    WaterBall = specific_load(language, [
        '水球',
        'Water Ball',
    ])

    global UserOffline
    UserOffline = specific_load(language, [
        '使用者離線',
        'User Offline',
    ])

    global SetCallStatus
    SetCallStatus = specific_load(language, [
        '設定呼叫器狀態',
        'Set Call Status',
    ])

    global Throw
    Throw = specific_load(language, [
        '丟',
        'Throw',
    ])

    global NoWaterball
    NoWaterball = specific_load(language, [
        '無訊息記錄',
        'No Waterball',
    ])

    global BrowseWaterball
    BrowseWaterball = specific_load(language, [
        '瀏覽水球紀錄',
        'Browse Waterball',
    ])

    global LanguageModule
    LanguageModule = specific_load(language, [
        '語言模組',
        'Language Module',
    ])

    global English
    English = specific_load(language, [
        '英文',
        'English',
    ])

    global ChineseTranditional
    ChineseTranditional = specific_load(language, [
        '繁體中文',
        'Chinese Tranditional',
    ])

    global GetCallStatus
    GetCallStatus = specific_load(language, [
        '取得呼叫器狀態',
        'Get BBCall Status',
    ])

    global NoMoney
    NoMoney = specific_load(language, [
        'P 幣不足',
        'No Money',
    ])

    global InputID
    InputID = specific_load(language, [
        '輸入帳號',
        'Input ID',
    ])

    global InputMoney
    InputMoney = specific_load(language, [
        '輸入金額',
        'Input Money',
    ])

    global AuthenticationHasNotExpired
    AuthenticationHasNotExpired = specific_load(language, [
        '認證尚未過期',
        'Authentication has not expired',
    ])

    global VerifyID
    VerifyID = specific_load(language, [
        '確認身分',
        'Verify ID',
    ])

    global TradingInProgress
    TradingInProgress = specific_load(language, [
        '交易正在進行中',
        'Trading is in progress',
    ])

    global Transaction
    Transaction = specific_load(language, [
        '交易',
        'Transaction',
    ])

    global MoneyTooFew
    MoneyTooFew = specific_load(language, [
        '金額過少，交易取消!',
        'The amount is too small, the transaction is cancelled!',
    ])

    global ConstantRedBag
    ConstantRedBag = specific_load(language, [
        '不修改紅包袋',
        'Constant the red bag',
    ])

    global SendMail
    SendMail = specific_load(language, [
        '寄信',
        'Send Mail',
    ])

    global Select
    Select = specific_load(language, [
        '選擇',
        'Select',
    ])

    global SignatureFile
    SignatureFile = specific_load(language, [
        '簽名檔',
        'Signature File',
    ])

    global NoSignatureFile
    NoSignatureFile = specific_load(language, [
        '不加簽名檔',
        'No Signature File',
    ])

    global SelfSaveDraft
    SelfSaveDraft = specific_load(language, [
        '自存底稿',
        'Self-Save Draft',
    ])

    global MailBox
    MailBox = specific_load(language, [
        '郵件選單',
        'Mail Box',
    ])

    global NoSuchBoard
    NoSuchBoard = specific_load(language, [
        '無該板面',
        'No Such Board',
    ])

    global HideSensitiveInfor
    HideSensitiveInfor = specific_load(language, [
        '隱藏敏感資訊',
        'Hide Sensitive Information',
    ])

    global PostFormatError
    PostFormatError = specific_load(language, [
        '文章格式錯誤',
        'Post Format Error',
    ])

    global LogHandler
    LogHandler = specific_load(language, [
        '紀錄額取器',
        'Log Handler',
    ])

    global NewCursor
    NewCursor = specific_load(language, [
        '新式游標',
        'New Type Cursor',
    ])

    global OldCursor
    OldCursor = specific_load(language, [
        '舊式游標',
        'Old Type Cursor',
    ])

    global PostNoContent
    PostNoContent = specific_load(language, [
        '此文章無內容',
        'Post has no content',
    ])

    global ConnectionClosed
    ConnectionClosed = specific_load(language, [
        '連線已經被關閉',
        'Connection Closed',
    ])

    global BoardList
    BoardList = specific_load(language, [
        '看板列表',
        'Board List',
    ])

    global UnregisteredUserCantUseAllAPI
    UnregisteredUserCantUseAllAPI = specific_load(language, [
        '未註冊使用者，將無法使用全部功能',
        'Unregistered User Can\'t Use All API',
    ])

    global UnregisteredUserCantUseThisAPI
    UnregisteredUserCantUseThisAPI = specific_load(language, [
        '未註冊使用者，無法使用此功能',
        'Unregistered User Can\'t Use This API',
    ])

    global MultiThreadOperate
    MultiThreadOperate = specific_load(language, [
        '請勿使用多線程同時操作一個 PTT Library 物件',
        'Do not use a multi-thread to operate a PTT Library object',
    ])

    global HasNewMailGotoMainMenu
    HasNewMailGotoMainMenu = specific_load(language, [
        '有新信，回到主選單',
        'Have a new letter, return to the main menu',
    ])

    global UseTooManyResources
    UseTooManyResources = specific_load(language, [
        '耗用太多資源',
        'Use too many resources of PTT',
    ])

    global Host
    Host = specific_load(language, [
        '主機',
        'Host',
    ])

    global PTT2NotSupport
    PTT2NotSupport = specific_load(language, [
        f'{PTT2}不支援',
        f'{PTT2} Not Support',
    ])

    # Animation
    global AnimationPost
    AnimationPost = specific_load(language, [
        '動畫文章',
        'Animation Post',
    ])

    global RestoreConnection
    RestoreConnection = specific_load(language, [
        '恢復連線',
        'Restore Connection',
    ])

    global NoPush
    NoPush = specific_load(language, [
        '禁止推薦',
        'No Push',
    ])

    global NoResponse
    NoResponse = specific_load(language, [
        '很抱歉, 此文章已結案並標記, 不得回應',
        'This Post has been closed and marked, no response',
    ])

    global ReplyBoard
    ReplyBoard = specific_load(language, [
        '回應至看板',
        'Respond to the Board',
    ])

    global ReplyMail
    ReplyMail = specific_load(language, [
        '回應至作者信箱',
        'Respond to the mailbox of author',
    ])

    global ReplyBoard_Mail
    ReplyBoard_Mail = specific_load(language, [
        '回應至看板與作者信箱',
        'Respond to the Board and the mailbox of author',
    ])

    global UseTheOriginalTitle
    UseTheOriginalTitle = specific_load(language, [
        '採用原標題',
        'Use the original title',
    ])

    global QuoteOriginal
    QuoteOriginal = specific_load(language, [
        '引用原文',
        'Quote original',
    ])

    global EditPost
    EditPost = specific_load(language, [
        '編輯文章',
        'Edit Post',
    ])

    global RespondSuccess
    RespondSuccess = specific_load(language, [
        '回應成功',
        'Respond Success',
    ])

    global ForcedWrite
    ForcedWrite = specific_load(language, [
        '強制寫入',
        'Forced Write',
    ])

    global NoPost
    NoPost = specific_load(language, [
        '沒有文章',
        'No Post',
    ])

    global NeedModeratorPermission
    NeedModeratorPermission = specific_load(language, [
        '需要板主權限',
        'Need Moderator Permission',
    ])

    global NewSettingsHaveBeenSaved
    NewSettingsHaveBeenSaved = specific_load(language, [
        '已儲存新設定',
        'New settings have been saved',
    ])

    global NoChanges
    NoChanges = specific_load(language, [
        '未改變任何設定',
        'No changes have been made to any settings',
    ])

    global Mark
    Mark = specific_load(language, [
        '標記',
        'Mark',
    ])

    global MarkPost
    MarkPost = specific_load(language, [
        '標記文章',
        'Mark Post',
    ])

    global DelAllMarkPost
    DelAllMarkPost = specific_load(language, [
        '刪除所有標記文章',
        'Del All Mark Post',
    ])

    global NoSuchPost
    NoSuchPost = specific_load(language, [
        '{Target0} 板找不到這個文章代碼 {Target1}',
        'In {Target0}, the post code is not exist {Target1}',
    ])

    global GoMainMenu
    GoMainMenu = specific_load(language, [
        '回到主選單',
        'Back to main memu',
    ])

    global CanNotUseSearchPostCodeF
    CanNotUseSearchPostCodeF = specific_load(language, [
        '此狀態下無法使用搜尋文章代碼(AID)功能',
        'This state can not use the search Post code function',
    ])

    global FavouriteBoardList
    FavouriteBoardList = specific_load(language, [
        '我的最愛',
        'Favourite Board List',
    ])

    global bucket
    bucket = specific_load(language, [
        '水桶',
        'Bucket',
    ])

    global UserHasPreviouslyBeenBanned
    UserHasPreviouslyBeenBanned = specific_load(language, [
        '使用者之前已被禁言',
        'User has previously been banned',
    ])

    global InputBucketDays_Reason
    InputBucketDays_Reason = specific_load(language, [
        '輸入水桶天數與理由',
        'Input bucket days and reason',
    ])

    global UnconfirmedPost
    UnconfirmedPost = specific_load(language, [
        '待證實文章',
        'Post To Be Confirmed',
    ])

    global Reading
    Reading = specific_load(language, [
        '讀取中',
        'Reading',
    ])

    global ReadComplete
    ReadComplete = specific_load(language, [
        f'讀取{Done}',
        f'Read {Done}',
    ])

    global QuitUserProfile
    QuitUserProfile = specific_load(language, [
        f'退出使用者檔案',
        f'Quit User Profile',
    ])

    # No changes have been made to any settings

    # Quote original

    # global List
    # List = []

    # for k, v in globals().items():
    #     # System Var
    #     if k.startswith('_'):
    #         continue

    #     print(f'k {k}')
    #     print(f'v {v}')
    #     if isinstance(k, str) and isinstance(v, str):
    #         List.append(k)


def _createlist():

    i18nStrList = []

    for k, v in globals().items():
        # System Var
        if k.startswith('_'):
            continue
        if isinstance(k, str) and isinstance(v, str):
            i18nStrList.append(k)

    with open('i18n.txt', 'w') as F:
        F.write('\n'.join(i18nStrList))


if __name__ == '__main__':
    load(Language.Chinese)
    _createlist()
