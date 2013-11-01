from pages.pageList import PageList
from pages.settings import Settings
from userdb.userdb import UserDatabase, UserException
from pages.redirect import Redirect, RedirectException
from pages.pageLink import PageLink
from pages.users import UserLogin

class PageLoader():
    
    def getPage(self, params, externalConn=None):
        try:
            token = params.get("session", None)
            if token is not None:
                try:
                    UserDatabase().checkSessionToken(token, externalConn)
                except UserException as ex:
                    if ex.message != UserException.sessionExpired:
                        raise
                    newParams = {}
                    for k, v in params.items():
                        if k not in ("session"):
                            newParams[k] = v
                    raise RedirectException(PageLink(None, None, newParams))
            pageId = params.get("id", Settings.defaultPage)
            page = PageList.pages.get(pageId, None)
            if page is None:
                raise RedirectException(PageLink(None, None))
            role = page.role
            if not self.canDisplayPage(token, role, externalConn):
                if token is None:
                    msgKey = UserLogin.msgKeyNoLogin
                    pageParams = {"message": msgKey, "forward": pageId}
                else:
                    msgKey = msgKey = UserLogin.msgKeyNoAuth
                    pageParams = {"message": msgKey, "role": role, "forward": pageId}
                raise RedirectException(PageLink("login", page, pageParams))
            answer = page.getHtml(params)
        except RedirectException as ex:
            answer = Redirect(ex.link).getHtml()
        return answer

    def canDisplayPage(self, token, role, externalConn=None):
        if role is None:
            answer = True
        elif token is None:
            answer = False
        elif role == "":
            answer = True
        else:
            answer = UserDatabase().sessionHasRole(token, role, externalConn)
        return answer