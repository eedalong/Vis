# -*- coding: utf-8 -*-
#


class BaseError(Exception):

    def __init__(self, code, error_description):
        super(BaseError, self).__init__(error_description)
        self.code = code
        self.error_description = error_description

    def __repr__(self):
        return '[ERRCODE=%s] %s' % (self.code, self.error_description)

class InternalError(Exception):

    def __init__(self, error_description):
        super(InternalError, self).__init__("")
        self.code = "INTERNAL_ERROR"
        self.error_description = error_description

    def __repr__(self):
        return '[ERRCODE=%s] %s' % (self.code, self.error_description)


class InputError(BaseError):

    def __init__(self, error_description):
        super(InputError, self).__init__("INPUT_ERROR", error_description)

class MaxRequestFrequencyError(BaseError):
    def __init__(self, error_description):
        super(MaxRequestFrequencyError, self).__init__("MAX_FREQUENCY_ERROR", error_description)

class UserRegisterError(BaseError):
    def __init__(self, error_description):
        super(UserRegisterError, self).__init__("USER_REGISTER_ERROR", error_description)

class UserLoginError(BaseError):
    def __init__(self, error_description):
        super(UserLoginError, self).__init__("USER_LOGIN_ERROR", error_description)

class UserLogoutError(BaseError):
    def __init__(self, error_description):
        super(UserLogoutError, self).__init__("USER_LOGOUT_ERROR", error_description)

class ProjectError(BaseError):
    def __init__(self, error_description):
        super(ProjectError, self).__init__("PROJECT_ERROR", error_description)

class GroupError(BaseError):
    def __init__(self, error_description):
        super(GroupError, self).__init__("GROUP_ERROR", error_description)

class AuthError(BaseError):
    def __init__(self, error_description):
        super(AuthError, self).__init__("AUTH_ERROR", error_description)

class RoleError(BaseError):
    def __init__(self, error_description):
        super(RoleError, self).__init__("ROLE_ERROR", error_description)
class DownloadError(BaseError):
    def __init__(self, error_description):
        super(DownloadError,self).__init__("DOWNLOAD_ERROR", error_description)

class CodeExtractError(BaseError):
    def __init__(self, error_description):
        super(CodeExtractError, self).__init__("CODE_EXTRACTION_ERROR", error_description)
