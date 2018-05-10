from handler.hello_handler import *
from handler.account_handler import *
from handler.app_handler import *
from handler.my_handler import *
from handler.mine_handler import *
routes = [
    (r'/api/hello', HelloHandler),
    (r'/api/account/reg_verify', AccountReg_verifyHandler),
    (r'/api/account/reg', AccountRegHandler),
    (r'/api/account/passwd_verify', AccountPasswd_verifyHandler),
    (r'/api/account/passwd', AccountPasswdHandler),
    (r'/api/account/login', AccountLoginHandler),
    (r'/api/account/login_phone', AccountLoginPhoneHandler),
    (r'/api/account/logout', AccountLogoutHandler),

    (r'/api/app/add', AppAddHandler),
    (r'/api/app/view', AppViewHandler),
    (r'/api/app/download', AppDownloadHandler),

    (r'/api/my/download_history', MyDownloadHistoryHandler),

    (r'/api/mine/info', MineInfoHandler),
    (r'/api/mine/collect', MineCollectHandler),

]
