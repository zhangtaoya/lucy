from handler.hello_handler import *
from handler.account_handler import *
from handler.appstore_handler import *
routes = [
    (r'/api/hello', HelloHandler),
    (r'/api/appstore/add_app', AddAppHandler),
    (r'/api/account/reg_verify', AccountReg_verifyHandler),
    (r'/api/account/reg', AccountRegHandler),
    (r'/api/account/passwd_verify', AccountPasswd_verifyHandler),
    (r'/api/account/passwd', AccountPasswdHandler),
    (r'/api/account/login', AccountLoginHandler),
    (r'/api/account/logout', AccountLogoutHandler),

]
