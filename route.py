from handler.hello_handler import *
from handler.account_handler import *
routes = [
    (r'/api/hello', HelloHandler),
    (r'/api/account/phone_verify', AccountPhone_verifyHandler),
    (r'/api/account/reg', AccountRegHandler),
    (r'/api/account/passwd', AccountPasswdHandler),
    (r'/api/account/login', AccountLoginHandler),
    (r'/api/account/logout', AccountLogoutHandler),

]
