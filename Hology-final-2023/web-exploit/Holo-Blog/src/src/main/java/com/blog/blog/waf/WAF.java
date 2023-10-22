package com.blog.blog.waf;

import lombok.Getter;
import lombok.val;

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

    public static boolean isMalicious(String text) {
        for (val waf : WafList.values()) {
            for (val str : waf.blacklist) {
                if (text.contains(str)) {
                    return true;
                }
            }
        }
        return false;
    }
}
