package com.dimas;

import java.io.Serializable;

public class Command implements Runnable, Serializable {

    private String command;

    public Command(String command) {
        this.command = command;
    }

    @Override
    public void run() {
        try {
            groovy.lang.GroovyClassLoader groovyClassLoader = new groovy.lang.GroovyClassLoader();
            groovyClassLoader.parseClass(command);
            groovyClassLoader.close();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
}
