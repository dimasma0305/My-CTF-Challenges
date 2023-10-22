package com.blog.blog.db;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import lombok.val;

public class User {
    private Connection connection = null;

    public User() throws SQLException {
        this.connection = createConnection();
        val statement = this.connection.createStatement();
        statement.execute(
                "CREATE TABLE IF NOT EXISTS users (" +
                        "id VARCHAR(255) PRIMARY KEY," +
                        "role VARCHAR(255)" +
                        ")");
        statement.close(); // Close the statement after executing
    }

    private Connection createConnection() throws SQLException {
        return DriverManager.getConnection("jdbc:sqlite:user.db");
    }

    public void setUserId(String userId) throws SQLException {
        Connection connection = null;
        PreparedStatement preparedStatement = null;

        try {
            connection = createConnection();
            preparedStatement = connection.prepareStatement("INSERT INTO users values(?,?)");
            preparedStatement.setString(1, userId);
            preparedStatement.setString(2, "guest");
            preparedStatement.executeUpdate();
        } finally {
            if (preparedStatement != null) {
                preparedStatement.close();
            }
            if (connection != null) {
                connection.close();
            }
        }
    }

    public String getRole(String userId) throws SQLException {
        Connection connection = null;
        PreparedStatement preparedStatement = null;
        ResultSet resultSet = null;

        try {
            connection = createConnection();
            preparedStatement = connection.prepareStatement("SELECT role FROM users WHERE id=?");
            preparedStatement.setString(1, userId);
            resultSet = preparedStatement.executeQuery();

            if (resultSet.next()) {
                return resultSet.getString("role");
            } else {
                return null;
            }
        } finally {
            if (resultSet != null) {
                resultSet.close();
            }
            if (preparedStatement != null) {
                preparedStatement.close();
            }
            if (connection != null) {
                connection.close();
            }
        }
    }

    public void deleteUserByUserId(String userId) throws SQLException {
        Connection connection = null;
        PreparedStatement preparedStatement = null;

        try {
            connection = createConnection();
            preparedStatement = connection.prepareStatement("DELETE FROM users WHERE id=?");
            preparedStatement.setString(1, userId);
            preparedStatement.executeUpdate();
        } finally {
            if (preparedStatement != null) {
                preparedStatement.close();
            }
            if (connection != null) {
                connection.close();
            }
        }
    }
}
