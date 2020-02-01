﻿import time
import progressbar
import threading
import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

try:
    from . import DataType
    from . import Config
    from . import Util
    from . import i18n
    from . import ConnectCore
    from . import Log
    # from . import Screens
    from . import Exceptions
    from . import Command
    from . import CheckValue
    from . import Ver
except ModuleNotFoundError:
    import DataType
    import Config
    import Util
    import i18n
    import ConnectCore
    import Log
    # import Screens
    import Exceptions
    import Command
    import CheckValue
    import Ver
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

Version = Ver.V

Language = i18n.Language
ConnectMode = ConnectCore.ConnectMode
LogLevel = Log.Level
Command = Command
PushType = DataType.PushType
PostSearchType = DataType.PostSearchType
IndexType = DataType.IndexType
WaterBallOperateType = DataType.WaterBallOperateType
WaterBallType = DataType.WaterBallType
CallStatus = DataType.CallStatus
PostDeleteStatus = DataType.PostDeleteStatus
CrawlType = DataType.CrawlType
Host = DataType.Host
ReplyType = DataType.ReplyType
MarkType = DataType.MarkType


class Library:
    def __init__(
            self,
            language: int = 0,
            connect_mode: int = 0,
            log_level: int = 0,
            screen_time_out: int = 0,
            screen_long_time_out: int = 0,
            log_handler=None,
            host: int = 0,
    ):

        self._ID = None
        if log_handler is not None and not callable(log_handler):
            raise TypeError('[PTT Library] LogHandler is must callable!!')

        if log_handler is not None:
            has_log_handler = True
            set_log_handler_result = True
            try:
                log_handler(f'PTT Library v {Version}')
                log_handler('Developed by PTT CodingMan')
            except Exception:
                log_handler = None
                set_log_handler_result = False
        else:
            has_log_handler = False

        print(f'PTT Library v {Version}')
        print('Developed by PTT CodingMan')

        self._LoginStatus = False

        self.config = Config.Config()

        if not isinstance(language, int):
            raise TypeError('[PTT Library] Language must be integer')
        if not isinstance(connect_mode, int):
            raise TypeError('[PTT Library] ConnectMode must be integer')
        if not isinstance(log_level, int):
            raise TypeError('[PTT Library] LogLevel must be integer')
        if not isinstance(screen_time_out, int):
            raise TypeError('[PTT Library] ScreenTimeOut must be integer')
        if not isinstance(screen_long_time_out, int):
            raise TypeError('[PTT Library] ScreenLongTimeOut must be integer')
        if not isinstance(host, int):
            raise TypeError('[PTT Library] Host must be integer')

        if screen_time_out != 0:
            self.config.ScreenTimeOut = screen_time_out
        if screen_long_time_out != 0:
            self.config.ScreenLongTimeOut = screen_long_time_out

        if log_level == 0:
            log_level = self.config.LogLevel
        elif not Util.check_range(Log.Level, log_level):
            raise ValueError('[PTT Library] Unknown LogLevel', log_level)
        else:
            self.config.LogLevel = log_level

        if language == 0:
            language = self.config.Language
        elif not Util.check_range(i18n.Language, language):
            raise ValueError('[PTT Library] Unknown language', language)
        else:
            self.config.Language = language
        i18n.load(language)

        if log_handler is not None:
            # Log.Handler = LogHandler
            self.config.LogHandler = log_handler
            Log.show_value(
                self.config,
                Log.Level.INFO,
                i18n.LogHandler,
                i18n.Init
            )
        elif has_log_handler and not set_log_handler_result:
            Log.show_value(
                self.config,
                Log.Level.INFO,
                i18n.LogHandler,
                [
                    i18n.Init,
                    i18n.Fail
                ]
            )

        if language == i18n.Language.Chinese:
            Log.show_value(
                self.config, Log.Level.INFO, [
                    i18n.ChineseTranditional,
                    i18n.LanguageModule
                ],
                i18n.Init
            )
        elif language == i18n.Language.English:
            Log.show_value(
                self.config, Log.Level.INFO, [
                    i18n.English,
                    i18n.LanguageModule
                ],
                i18n.Init
            )

        if connect_mode == 0:
            connect_mode = self.config.ConnectMode
        elif not Util.check_range(ConnectCore.ConnectMode, connect_mode):
            raise ValueError('[PTT Library] Unknown ConnectMode', connect_mode)
        else:
            self.config.ConnectMode = connect_mode

        if host == 0:
            host = self.config.Host
        elif not Util.check_range(DataType.Host, host):
            raise ValueError('[PTT Library] Unknown Host', host)
        self.config.Host = host

        if host == DataType.Host.PTT1:
            Log.show_value(
                self.config,
                Log.Level.INFO,
                [
                    i18n.Connect,
                    i18n.Host
                ],
                i18n.PTT
            )
        if host == DataType.Host.PTT2:
            Log.show_value(
                self.config,
                Log.Level.INFO,
                [
                    i18n.Connect,
                    i18n.Host
                ],
                i18n.PTT2
            )

        self.connect_core = ConnectCore.API(self.config, host)
        self._ExistBoardList = []
        self._ModeratorList = dict()
        self._LastThrowWaterBallTime = 0
        self._ThreadID = threading.get_ident()

        Log.show_value(
            self.config,
            Log.Level.DEBUG,
            'ThreadID',
            self._ThreadID
        )

        Log.show_value(
            self.config,
            Log.Level.INFO, [
                i18n.PTT,
                i18n.Library,
                ' v ' + Version,
            ],
            i18n.Init
        )

    def _one_thread(self):
        current_thread_id = threading.get_ident()
        if current_thread_id == self._ThreadID:
            return
        Log.show_value(
            self.config,
            Log.Level.DEBUG,
            'ThreadID',
            self._ThreadID
        )
        Log.show_value(
            self.config,
            Log.Level.DEBUG,
            'Current thread id',
            current_thread_id
        )
        raise Exceptions.MultiThreadOperated()

    def get_version(self) -> str:
        self._one_thread()
        return self.config.Version

    def _login(
            self,
            pttid: str,
            password: str,
            kick_other_login: bool = False):

        try:
            from . import api_loginout
        except ModuleNotFoundError:
            import api_loginout

        return api_loginout.login(
            self,
            pttid,
            password,
            kick_other_login)

    def login(
            self,
            pttid: str,
            password: str,
            kick_other_login: bool = False):
        self._one_thread()

        CheckValue.check(self.config, str, 'ID', pttid)
        CheckValue.check(self.config, str, 'Password', password)
        CheckValue.check(self.config, bool, 'KickOtherLogin', kick_other_login)

        try:
            return self._login(
                pttid,
                password,
                kick_other_login=kick_other_login
            )
        except Exceptions.LoginError:
            return self._login(
                pttid,
                password,
                kick_other_login=kick_other_login
            )

    def logout(self):
        self._one_thread()

        if not self._LoginStatus:
            return

        try:
            from . import api_loginout
        except ModuleNotFoundError:
            import api_loginout

        return api_loginout.logout(self)

    def log(self, msg: str) -> None:
        self._one_thread()
        Log.log(self.config, Log.Level.INFO, msg)

    def get_time(self) -> str:
        self._one_thread()
        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        try:
            from . import api_getTime
        except ModuleNotFoundError:
            import api_getTime

        return api_getTime.get_time(self)

    def get_post(
            self,
            board: str,
            post_aid: str = None,
            post_index: int = 0,
            search_type: int = 0,
            search_condition: str = None,
            query: bool = False) -> DataType.PostInfo:
        self._one_thread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        CheckValue.check(self.config, str, 'Board', board)
        if post_aid is not None:
            CheckValue.check(self.config, str, 'PostAID', post_aid)
        CheckValue.check(self.config, int, 'PostIndex', post_index)
        CheckValue.check(self.config, int, 'SearchType', search_type,
                         value_class=DataType.PostSearchType)
        if search_condition is not None:
            CheckValue.check(self.config, str,
                             'SearchCondition', search_condition)

        if len(board) == 0:
            raise ValueError(Log.merge(
                self.config,
                [
                    i18n.Board,
                    i18n.ErrorParameter,
                    board
                ]))

        if post_index != 0 and isinstance(post_aid, str):
            raise ValueError(Log.merge(
                self.config,
                [
                    'PostIndex',
                    'PostAID',
                    i18n.ErrorParameter,
                    i18n.BothInput
                ]))

        if post_index == 0 and post_aid is None:
            raise ValueError(Log.merge(
                self.config,
                [
                    'PostIndex',
                    'PostAID',
                    i18n.ErrorParameter
                ]))

        if search_condition is not None and search_type == 0:
            raise ValueError(Log.merge(
                self.config,
                [
                    'SearchType',
                    i18n.ErrorParameter,
                ]))

        if search_type == DataType.PostSearchType.Push:
            try:
                S = int(search_condition)
            except ValueError:
                raise ValueError(Log.merge(
                    self.config,
                    [
                        'SearchCondition',
                        i18n.ErrorParameter,
                    ]))

            if not (-100 <= S <= 110):
                raise ValueError(Log.merge(
                    self.config,
                    [
                        'SearchCondition',
                        i18n.ErrorParameter,
                    ]))

        if post_aid is not None and search_condition is not None:
            raise ValueError(Log.merge(
                self.config,
                [
                    'PostAID',
                    'SearchCondition',
                    i18n.ErrorParameter,
                    i18n.BothInput,
                ]))

        if post_index != 0:
            newest_index = self._get_newest_index(
                DataType.IndexType.BBS,
                board=board,
                search_type=search_type,
                search_condition=search_condition
            )

            if post_index < 1 or newest_index < post_index:
                raise ValueError(Log.merge(
                    self.config,
                    [
                        'PostIndex',
                        i18n.ErrorParameter,
                        i18n.OutOfRange,
                    ]))

        self._check_board(board)

        for i in range(2):

            need_continue = False
            post = None
            try:
                post = self._get_post(
                    board,
                    post_aid,
                    post_index,
                    search_type,
                    search_condition,
                    query
                )
            except Exceptions.ParseError as e:
                if i == 1:
                    raise e
                need_continue = True
            except Exceptions.UnknownError as e:
                if i == 1:
                    raise e
                need_continue = True
            except Exceptions.NoSuchBoard as e:
                if i == 1:
                    raise e
                need_continue = True
            except Exceptions.NoMatchTargetError as e:
                if i == 1:
                    raise e
                need_continue = True

            if post is None:
                need_continue = True
            elif not post.is_format_check():
                need_continue = True

            if need_continue:
                Log.log(
                    self.config,
                    Log.Level.DEBUG,
                    'Wait for retry repost'
                )
                time.sleep(0.1)
                continue

            break
        return post

    def _check_board(
            self,
            board: str,
            check_moderator: bool = False):
        if board.lower() not in self._ExistBoardList:
            boardinfo = self._get_board_info(board)
            self._ExistBoardList.append(board.lower())

            moderators = boardinfo.get_moderators()
            moderators = [x.lower() for x in moderators]
            self._ModeratorList[board.lower()] = moderators

        if check_moderator:
            if self._ID.lower() not in self._ModeratorList[board.lower()]:
                raise Exceptions.NeedModeratorPermission(board)

    def _get_post(
            self,
            board: str,
            post_aid: str = None,
            post_index: int = 0,
            search_type: int = 0,
            search_condition: str = None,
            query: bool = False):

        try:
            from . import api_getPost
        except ModuleNotFoundError:
            import api_getPost

        return api_getPost.get_post(
            self,
            board,
            post_aid,
            post_index,
            search_type,
            search_condition,
            query)

    def _get_newest_index(
            self,
            index_type: int,
            board: str = None,
            # BBS
            search_type: int = 0,
            search_condition: str = None) -> int:

        CheckValue.check(
            self.config, int, 'IndexType',
            index_type, value_class=DataType.IndexType)
        CheckValue.check(self.config, str, 'Board', board)

        try:
            from . import api_getNewestIndex
        except ModuleNotFoundError:
            import api_getNewestIndex

        return api_getNewestIndex.get_newest_index(
            self,
            index_type,
            board,
            search_type,
            search_condition)

    def get_newest_index(
            self,
            index_type: int,
            board: str = None,
            search_type: int = 0,
            search_condition: str = None) -> int:
        self._one_thread()

        if index_type == DataType.IndexType.BBS:
            if not self._LoginStatus:
                raise Exceptions.RequireLogin(i18n.RequireLogin)

        try:
            return self._get_newest_index(
                index_type,
                board,
                search_type,
                search_condition
            )
        except Exception:
            return self._get_newest_index(
                index_type,
                board,
                search_type,
                search_condition
            )

    def _get_post_index(
            self,
            board: str,
            aid) -> int:

        try:
            from . import api_getPostIndex
        except ModuleNotFoundError:
            import api_getPostIndex

        return api_getPostIndex.get_post_index(
            self,
            board,
            aid)

    def crawl_board(
            self,
            crawl_type: int,
            post_handler,
            board: str,
            # BBS版本
            start_index: int = 0,
            end_index: int = 0,
            start_aid: str = None,
            end_aid: str = None,
            search_type: int = 0,
            search_condition: str = None,
            query: bool = False,
            # 網頁版本
            start_page: int = 0,
            end_page: int = 0) -> list:

        self._one_thread()

        CheckValue.check(
            self.config, int, 'CrawlType',
            crawl_type, value_class=DataType.CrawlType)
        CheckValue.check(self.config, str, 'Board', board)

        if len(board) == 0:
            raise ValueError(Log.merge(
                self.config,
                [
                    i18n.Board,
                    i18n.ErrorParameter,
                    board
                ]))

        if crawl_type == DataType.CrawlType.BBS:
            if not self._LoginStatus:
                raise Exceptions.RequireLogin(i18n.RequireLogin)

            CheckValue.check(self.config, int, 'SearchType', search_type)
            if search_condition is not None:
                CheckValue.check(self.config, str,
                                 'SearchCondition', search_condition)
            if start_aid is not None:
                CheckValue.check(self.config, str, 'StartAID', start_aid)
            if end_aid is not None:
                CheckValue.check(self.config, str, 'EndAID', end_aid)

            if (start_aid is not None or end_aid is not None) and \
                    (start_index != 0 or end_index != 0):
                raise ValueError(Log.merge(
                    self.config,
                    [
                        'AID',
                        'Index',
                        i18n.ErrorParameter,
                        i18n.BothInput
                    ]))

            if (start_aid is not None or end_aid is not None) and \
                    (search_condition is not None):
                raise ValueError(Log.merge(
                    self.config,
                    [
                        'AID',
                        'SearchCondition',
                        i18n.ErrorParameter,
                        i18n.BothInput
                    ]))

            if search_type == DataType.PostSearchType.Push:
                try:
                    S = int(search_condition)
                except ValueError:
                    raise ValueError(Log.merge(
                        self.config,
                        [
                            'SearchCondition',
                            i18n.ErrorParameter,
                        ]))

                if not (-100 <= S <= 110):
                    raise ValueError(Log.merge(
                        self.config,
                        [
                            'SearchCondition',
                            i18n.ErrorParameter,
                        ]))

            if start_index != 0:
                newest_index = self._get_newest_index(
                    DataType.IndexType.BBS,
                    board=board,
                    search_type=search_type,
                    search_condition=search_condition
                )
                CheckValue.check_index_range(
                    self.config,
                    'StartIndex',
                    start_index,
                    'EndIndex',
                    end_index,
                    max_value=newest_index
                )
            elif start_aid is not None and end_aid is not None:
                start_index = self._get_post_index(
                    board,
                    start_aid,
                )
                end_index = self._get_post_index(
                    board,
                    end_aid,
                )
                CheckValue.check_index_range(
                    self.config,
                    'StartAID',
                    start_index,
                    'EndAID',
                    end_index
                )
            else:
                raise ValueError(Log.merge(
                    self.config,
                    [
                        i18n.ErrorParameter,
                        i18n.NoInput
                    ]))

            Log.show_value(
                self.config,
                Log.Level.DEBUG,
                'StartIndex',
                start_index
            )

            Log.show_value(
                self.config,
                Log.Level.DEBUG,
                'EndIndex',
                end_index
            )

            error_post_list = []
            del_post_list = []
            if self.config.LogLevel == Log.Level.INFO:
                PB = progressbar.ProgressBar(
                    max_value=end_index - start_index + 1,
                    redirect_stdout=True
                )
            for index in range(start_index, end_index + 1):

                for i in range(2):
                    need_continue = False
                    post = None
                    try:
                        post = self._get_post(
                            board,
                            post_index=index,
                            search_type=search_type,
                            search_condition=search_condition,
                            query=query
                        )
                    except Exceptions.ParseError as e:
                        if i == 1:
                            raise e
                        need_continue = True
                    except Exceptions.UnknownError as e:
                        if i == 1:
                            raise e
                        need_continue = True
                    except Exceptions.NoSuchBoard as e:
                        if i == 1:
                            raise e
                        need_continue = True
                    except Exceptions.NoMatchTargetError as e:
                        if i == 1:
                            raise e
                        need_continue = True
                    except Exceptions.ConnectionClosed as e:
                        if i == 1:
                            raise e
                        Log.log(
                            self.config,
                            Log.Level.INFO,
                            i18n.RestoreConnection
                        )
                        self._login(
                            self._ID,
                            self._Password,
                            self.config.KickOtherLogin
                        )
                        need_continue = True
                    except Exceptions.UseTooManyResources as e:
                        if i == 1:
                            raise e
                        Log.log(
                            self.config,
                            Log.Level.INFO,
                            i18n.RestoreConnection
                        )
                        self._login(
                            self._ID,
                            self._Password,
                            self.config.KickOtherLogin
                        )
                        need_continue = True

                    if post is None:
                        need_continue = True
                    elif not post.is_format_check():
                        need_continue = True

                    if need_continue:
                        Log.log(
                            self.config,
                            Log.Level.DEBUG,
                            'Wait for retry repost'
                        )
                        time.sleep(0.1)
                        continue

                    break

                if self.config.LogLevel == Log.Level.INFO:
                    PB.update(index - start_index)
                if post is None:
                    error_post_list.append(index)
                    continue
                if not post.is_format_check():
                    if post.get_aid() is not None:
                        error_post_list.append(post.get_aid())
                    else:
                        error_post_list.append(index)
                    continue
                if post.get_delete_status() != DataType.PostDeleteStatus.NotDeleted:
                    del_post_list.append(index)
                post_handler(post)
            if self.config.LogLevel == Log.Level.INFO:
                PB.finish()

            return error_post_list, del_post_list

        else:
            if self.config.Host == DataType.Host.PTT2:
                raise Exceptions.HostNotSupport(Util.get_current_func_name())

            # 網頁版本爬蟲
            # https://www.ptt.cc/bbs/index.html

            # 1. 取得總共有幾頁 MaxPage
            newest_index = self._get_newest_index(
                DataType.IndexType.Web,
                board=board
            )
            # 2. 檢查 StartPage 跟 EndPage 有沒有在 1 ~ MaxPage 之間

            CheckValue.check_index_range(
                self.config,
                'StartPage',
                start_page,
                'EndPage',
                end_page,
                max_value=newest_index
            )

            # 3. 把每篇文章(包括被刪除文章)欄位解析出來組合成 DataType.PostInfo
            error_post_list = []
            del_post_list = []
            # PostAID = ""
            _url = 'https://www.ptt.cc/bbs/'
            index = str(newest_index)
            if self.config.LogLevel == Log.Level.INFO:
                PB = progressbar.ProgressBar(
                    max_value=end_page - start_page + 1,
                    redirect_stdout=True
                )

            def deleted_post(post_title):
                if post_title.startswith('('):
                    if '本文' in post_title:
                        return DataType.PostDeleteStatus.ByAuthor
                    elif post_title.startswith('(已被'):
                        return DataType.PostDeleteStatus.ByModerator
                    else:
                        return DataType.PostDeleteStatus.ByUnknown
                else:
                    return DataType.PostDeleteStatus.NotDeleted

            for index in range(start_page, newest_index + 1):
                Log.show_value(
                    self.config,
                    Log.Level.DEBUG,
                    'CurrentPage',
                    index
                )

                url = _url + board + '/index' + str(index) + '.html'
                r = requests.get(url, cookies={'over18': '1'})
                if r.status_code != requests.codes.ok:
                    raise Exceptions.NoSuchBoard(self.config, board)
                soup = BeautifulSoup(r.text, 'html.parser')

                for div in soup.select('div.r-ent'):
                    web = div.select('div.title a')
                    post = {
                        'author': div.select('div.author')[0].text,
                        'title': div.select('div.title')[0].text.strip('\n').strip(),
                        'web': web[0].get('href') if web else ''
                    }
                    if post['title'].startswith('('):
                        del_post_list.append(post['title'])
                        if post['title'].startswith('(本文'):
                            if '[' in post['title']:
                                post['author'] = post['title'].split(
                                    '[')[1].split(']')[0]
                            else:
                                post['author'] = post['title'].split('<')[
                                    1].split('>')[0]
                        else:
                            post['author'] = post['title'].split('<')[
                                1].split('>')[0]

                    post = DataType.PostInfo(
                        board=board,
                        author=post['author'],
                        title=post['title'],
                        web_url='https://www.ptt.cc' + post['web'],
                        delete_status=deleted_post(post['title'])
                    )
                    post_handler(post)

                if self.config.LogLevel == Log.Level.INFO:
                    PB.update(index - start_page)

            Log.show_value(
                self.config,
                Log.Level.DEBUG,
                'DelPostList',
                del_post_list
            )

            # 4. 把組合出來的 Post 塞給 handler

            # 5. 顯示 progress bar
            if self.config.LogLevel == Log.Level.INFO:
                PB.finish()

            return error_post_list, del_post_list

    def post(
            self,
            board: str,
            title: str,
            content: str,
            post_type: int,
            sign_file) -> None:
        self._one_thread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        CheckValue.check(self.config, str, 'Board', board)
        CheckValue.check(self.config, str, 'Title', title)
        CheckValue.check(self.config, str, 'Content', content)
        CheckValue.check(self.config, int, 'PostType', post_type)

        check_sign_file = False
        for i in range(0, 10):
            if str(i) == sign_file or i == sign_file:
                check_sign_file = True
                break

        if not check_sign_file:
            sign_file = sign_file.lower()
            if sign_file != 'x':
                raise ValueError(Log.merge(
                    self.config,
                    [
                        'SignFile',
                        i18n.ErrorParameter,
                        sign_file
                    ]))

        self._check_board(board)

        try:
            from . import api_post
        except ModuleNotFoundError:
            import api_post

        return api_post.post(
            self,
            board,
            title,
            content,
            post_type,
            sign_file)

    def push(
            self,
            board: str,
            push_type: int,
            push_content: str,
            post_aid: str = None,
            post_index: int = 0) -> None:
        self._one_thread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        CheckValue.check(self.config, str, 'Board', board)
        CheckValue.check(self.config, int, 'PushType',
                         push_type, value_class=DataType.PushType)
        CheckValue.check(self.config, str, 'PushContent', push_content)
        if post_aid is not None:
            CheckValue.check(self.config, str, 'PostAID', post_aid)
        CheckValue.check(self.config, int, 'PostIndex', post_index)

        if len(board) == 0:
            raise ValueError(Log.merge(
                self.config,
                [
                    i18n.Board,
                    i18n.ErrorParameter,
                    board
                ]))

        if post_index != 0 and isinstance(post_aid, str):
            raise ValueError(Log.merge(
                self.config,
                [
                    'PostIndex',
                    'PostAID',
                    i18n.ErrorParameter,
                    i18n.BothInput
                ]))

        if post_index == 0 and post_aid is None:
            raise ValueError(Log.merge(
                self.config,
                [
                    'PostIndex',
                    'PostAID',
                    i18n.ErrorParameter,
                    i18n.NoInput
                ]))

        if post_index != 0:
            newest_index = self._get_newest_index(
                DataType.IndexType.BBS,
                board=board
            )
            CheckValue.check_index(self.config, 'PostIndex',
                                   post_index, newest_index)

        self._check_board(board)

        max_push_length = 33
        push_list = []

        temp_start_index = 0
        temp_end_index = temp_start_index + 1

        while temp_end_index <= len(push_content):

            temp = ''
            last_temp = None
            while len(temp.encode('big5-uao', 'replace')) < max_push_length:
                temp = push_content[temp_start_index:temp_end_index]

                if not len(temp.encode('big5-uao', 'replace')) < max_push_length:
                    break
                elif push_content.endswith(temp):
                    break
                elif temp.endswith('\n'):
                    break
                elif last_temp == temp:
                    break

                temp_end_index += 1
                last_temp = temp

            push_list.append(temp.strip())

            temp_start_index = temp_end_index
            temp_end_index = temp_start_index + 1
        push_list = filter(None, push_list)

        for push in push_list:
            Log.show_value(
                self.config,
                Log.Level.INFO,
                i18n.Push,
                push
            )

            for _ in range(2):
                try:
                    self._push(
                        board,
                        push_type,
                        push,
                        post_aid=post_aid,
                        post_index=post_index
                    )
                    break
                except Exceptions.NoFastPush:
                    # Screens.show(self.config, self.connect_core.getScreenQueue())
                    Log.log(
                        self.config,
                        Log.Level.INFO,
                        '等待快速推文'
                    )
                    time.sleep(5.2)

    def _push(
            self,
            board: str,
            push_type: int,
            push_content: str,
            post_aid: str = None,
            post_index: int = 0) -> None:

        try:
            from . import api_push
        except ModuleNotFoundError:
            import api_push

        return api_push.push(
            self,
            board,
            push_type,
            push_content,
            post_aid,
            post_index)

    def _get_user(self, user_id) -> DataType.UserInfo:

        CheckValue.check(self.config, str, 'UserID', user_id)
        if len(user_id) < 3:
            raise ValueError(Log.merge(
                self.config,
                [
                    'UserID',
                    i18n.ErrorParameter,
                    user_id
                ]))

        try:
            from . import api_getUser
        except ModuleNotFoundError:
            import api_getUser

        return api_getUser.get_user(self, user_id)

    def get_user(self, user_id) -> DataType.UserInfo:
        self._one_thread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        if self._UnregisteredUser:
            raise Exceptions.UnregisteredUser(Util.get_current_func_name())

        return self._get_user(user_id)

    def throw_waterball(self, pttid, content) -> None:
        self._one_thread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        if self._UnregisteredUser:
            raise Exceptions.UnregisteredUser(Util.get_current_func_name())

        CheckValue.check(self.config, str, 'pttid', pttid)
        CheckValue.check(self.config, str, 'content', content)

        if len(pttid) <= 2:
            raise ValueError(Log.merge(
                self.config,
                [
                    'pttid',
                    i18n.ErrorParameter,
                    pttid
                ]))

        user = self._get_user(pttid)
        if '不在站上' in user.get_state():
            raise Exceptions.UserOffline(pttid)

        try:
            from . import api_WaterBall
        except ModuleNotFoundError:
            import api_WaterBall

        return api_WaterBall.throw_waterball(self, pttid, content)

    def get_waterball(self, operate_type: int) -> list:
        self._one_thread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        if self._UnregisteredUser:
            raise Exceptions.UnregisteredUser(Util.get_current_func_name())

        CheckValue.check(
            self.config, int, 'OperateType', operate_type,
            value_class=DataType.WaterBallOperateType)

        try:
            from . import api_WaterBall
        except ModuleNotFoundError:
            import api_WaterBall

        return api_WaterBall.get_waterball(self, operate_type)

    def get_callstatus(self) -> int:
        self._one_thread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        return self._get_callstatus()

    def _get_callstatus(self) -> int:

        try:
            from . import api_CallStatus
        except ModuleNotFoundError:
            import api_CallStatus

        return api_CallStatus.get_callstatus(self)

    def set_callstatus(
            self,
            call_status):
        self._one_thread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        CheckValue.check(self.config, int, 'CallStatus', call_status,
                         value_class=DataType.CallStatus)

        try:
            from . import api_CallStatus
        except ModuleNotFoundError:
            import api_CallStatus

        return api_CallStatus.set_callstatus(self, call_status)

    def give_money(self, pttid: str, money: int):
        self._one_thread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        if self._UnregisteredUser:
            raise Exceptions.UnregisteredUser(Util.get_current_func_name())

        CheckValue.check(self.config, str, 'ID', pttid)
        CheckValue.check(self.config, int, 'Money', money)
        # Check user
        self.get_user(pttid)

        try:
            from . import api_giveMoney
        except ModuleNotFoundError:
            import api_giveMoney

        return api_giveMoney.give_money(self, pttid, money)

    def mail(
            self,
            pttid: str,
            title: str,
            content: str,
            sign_file) -> None:
        self._one_thread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        CheckValue.check(self.config, str, 'pttid', pttid)
        CheckValue.check(self.config, str, 'title', title)
        CheckValue.check(self.config, str, 'content', content)

        check_sign_file = False
        for i in range(0, 10):
            if str(i) == sign_file or i == sign_file:
                check_sign_file = True
                break

        if not check_sign_file:
            sign_file = sign_file.lower()
            if sign_file != 'x':
                raise ValueError(Log.merge(
                    self.config,
                    [
                        'SignFile',
                        i18n.ErrorParameter,
                        sign_file
                    ]))

        try:
            from . import api_mail
        except ModuleNotFoundError:
            import api_mail

        return api_mail.mail(
            self,
            pttid,
            title,
            content,
            sign_file)

    def has_new_mail(self) -> int:
        self._one_thread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        try:
            from . import api_hasNewMail
        except ModuleNotFoundError:
            import api_hasNewMail

        return api_hasNewMail.has_new_mail(self)

    def get_board_list(self) -> list:
        self._one_thread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        try:
            from . import api_getBoardList
        except ModuleNotFoundError:
            import api_getBoardList

        return api_getBoardList.get_board_list(self)

    def reply_post(
            self,
            reply_type: int,
            board: str,
            content: str,
            sign_file=0,
            post_aid: str = None,
            post_index: int = 0) -> None:
        self._one_thread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        CheckValue.check(self.config, int, 'ReplyType', reply_type,
                         value_class=DataType.ReplyType)
        CheckValue.check(self.config, str, 'Board', board)
        CheckValue.check(self.config, str, 'Content', content)
        if post_aid is not None:
            CheckValue.check(self.config, str, 'PostAID', post_aid)

        if post_index != 0:
            newest_index = self._get_newest_index(
                DataType.IndexType.BBS,
                board=board)
            CheckValue.check_index(
                self.config, 'PostIndex',
                post_index, max_value=newest_index)

        sign_file_list = [str(x) for x in range(0, 10)]
        sign_file_list.append('x')

        if str(sign_file) not in sign_file_list:
            raise ValueError(Log.merge(
                self.config,
                [
                    'SignFile',
                    i18n.ErrorParameter
                ]))

        if post_aid is not None and post_index != 0:
            raise ValueError(Log.merge(
                self.config,
                [
                    'PostIndex',
                    'PostAID',
                    i18n.ErrorParameter,
                    i18n.BothInput
                ]))

        self._check_board(board)

        try:
            from . import api_replyPost
        except ModuleNotFoundError:
            import api_replyPost

        api_replyPost.reply_post(
            self,
            reply_type,
            board,
            content,
            sign_file,
            post_aid,
            post_index)

    def set_board_title(
            self,
            board: str,
            new_title: str) -> None:
        # 第一支板主專用 API
        self._one_thread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        CheckValue.check(self.config, str, 'board', board)
        CheckValue.check(self.config, str, 'new_title', new_title)

        self._check_board(
            board,
            check_moderator=True)

        try:
            from . import api_setBoardTitle
        except ModuleNotFoundError:
            import api_setBoardTitle

        api_setBoardTitle.set_board_title(self, board, new_title)

    def mark_post(
            self,
            mark_type: int,
            board: str,
            post_aid: str = None,
            post_index: int = 0,
            search_type: int = 0,
            search_condition: str = None) -> None:
        # 標記文章
        self._one_thread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        try:
            from . import api_markPost
        except ModuleNotFoundError:
            import api_markPost

        api_markPost.markPost(
            self,
            mark_type,
            board,
            post_aid,
            post_index,
            search_type,
            search_condition
        )

    def get_favourite_board(self) -> list:
        self._one_thread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        try:
            from . import api_getFavouriteBoard
        except ModuleNotFoundError:
            import api_getFavouriteBoard

        return api_getFavouriteBoard.get_favourite_board(self)

    def bucket(self, board: str, bucket_days: int, reason: str, pttid: str) -> None:

        self._one_thread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        CheckValue.check(self.config, str, 'board', board)
        CheckValue.check(self.config, int, 'bucket_days', bucket_days)
        CheckValue.check(self.config, str, 'reason', reason)
        CheckValue.check(self.config, str, 'pttid', pttid)

        self._get_user(pttid)

        self._check_board(
            board,
            check_moderator=True)

        try:
            from . import api_bucket
        except ModuleNotFoundError:
            import api_bucket

        api_bucket.bucket(
            self, board, bucket_days, reason, pttid)

    def search_user(
            self,
            pttid: str,
            min_page: int = None,
            max_page: int = None) -> list:

        self._one_thread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        CheckValue.check(self.config, str, 'pttid', pttid)
        if min_page is not None:
            CheckValue.check_index(
                self.config,
                'min_page',
                min_page
            )
        if max_page is not None:
            CheckValue.check_index(
                self.config,
                'max_page',
                max_page
            )
        if min_page is not None and max_page is not None:
            CheckValue.check_index_range(
                self.config,
                'min_page',
                min_page,
                'max_page',
                max_page
            )

        try:
            from . import api_searchuser
        except ModuleNotFoundError:
            import api_searchuser

        return api_searchuser.search_user(self, pttid, min_page, max_page)

    def get_board_info(self, board: str) -> DataType.BoardInfo:

        self._one_thread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        CheckValue.check(self.config, str, 'board', board)

        return self._get_board_info(board)

    def _get_board_info(self, board: str) -> DataType.BoardInfo:

        try:
            from . import api_getBoardInfo
        except ModuleNotFoundError:
            import api_getBoardInfo

        return api_getBoardInfo.get_board_info(self, board)


if __name__ == '__main__':
    print('PTT Library v ' + Version)
    print('Developed by PTT CodingMan')
