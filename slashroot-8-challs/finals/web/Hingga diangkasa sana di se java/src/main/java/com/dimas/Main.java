package com.dimas;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.util.HashMap;
import java.util.Map;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

public class Main {
    public static void main(String[] args) {
        try {
            HttpServer httpServer = HttpServer.create(new InetSocketAddress(8080), 0);
            httpServer.createContext("/", new MyHandler());
            httpServer.start();
            System.out.println("Server started on port 8080...");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    static class MyHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {

            exchange.getResponseHeaders().set("Content-Type", "text/plain");
            exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");

            String queryString = exchange.getRequestURI().getQuery();

            Map<String, String> params = parseQueryString(queryString);

            String url = params.get("url");
            String name = "";
            try {
                name = new javax.naming.InitialContext().lookup(url).toString();
            } catch (Exception e) {
                e.printStackTrace();
                System.out.println("Error: " + e.getMessage());
                name = url;
            }

            String response = "Hello, " + (name != null ? name : "World");

            exchange.sendResponseHeaders(200, response.getBytes().length);
            try (OutputStream outputStream = exchange.getResponseBody()) {
                outputStream.write(response.getBytes());
            }
        }

        // Method to parse the query string and extract parameters
        private Map<String, String> parseQueryString(String queryString) {
            Map<String, String> params = new HashMap<>();
            if (queryString != null) {
                String[] keyValuePairs = queryString.split("&");
                for (String pair : keyValuePairs) {
                    String[] keyValue = pair.split("=");
                    if (keyValue.length == 2) {
                        String key = keyValue[0];
                        String value = keyValue[1];
                        params.put(key, value);
                    }
                }
            }
            return params;
        }
    }
}
