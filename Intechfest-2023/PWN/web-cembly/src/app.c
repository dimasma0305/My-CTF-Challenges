#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <emscripten/emscripten.h>

#ifdef __cplusplus
#define EXTERN extern "C"
#else
#define EXTERN
#endif

#include <string.h>

EXTERN EMSCRIPTEN_KEEPALIVE void *setTitle(char *store)
{
  strcpy(store, "<div class=\"d-flex flex-column align-items-center justify-content-center\" style=\"height: 100vh;\"><h1 class=\"text-center\">Welcome to My Static Website<br/><name/></h1><div class=\"d-flex flex-column align-items-center\"><a href=\"/report/\">report</a></div></div>");
  return 0;
}

EXTERN EMSCRIPTEN_KEEPALIVE void *setHeaderTag(char *text)
{
  EM_ASM({document.getElementById("title").innerHTML = UTF8ToString($0)}, text);
  return 0;
}
EXTERN EMSCRIPTEN_KEEPALIVE void *setNameTag(char *text)
{
  EM_ASM({document.querySelector("name").innerText = UTF8ToString($0)}, text);
  return 0;
}

EXTERN EMSCRIPTEN_KEEPALIVE void *getHash(char *store)
{
  char *hash = (char *)EM_ASM_INT({
    return stringToUTF8OnStack(decodeURI(location.hash.slice(1, location.hash.length)));
  });

  strcpy(store, hash);
  return 0;
}

int main()
{
  char _title[1024];
  char protection[9] = "PROTECTED";
  char _hash[1024];
  setTitle(_title);
  getHash(_hash);
  if (strncmp(protection, "PROTECTED", 9) == 0)
  {
    setHeaderTag(_title);
    setNameTag(_hash);
  }
  else
  {
    printf("**STACK SMASHING DETECTED**\n");
  }
  return 0;
}
