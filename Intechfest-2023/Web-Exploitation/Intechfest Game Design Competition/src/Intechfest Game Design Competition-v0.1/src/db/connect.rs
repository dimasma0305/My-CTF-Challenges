use std::sync::{Mutex, MutexGuard};

use rand::Rng;
use rusqlite::{Connection, Error};

lazy_static::lazy_static! {
// For security reasons, I use a database file that starts with a random name.
    static ref DB_PATH: Mutex<String> = Mutex::new(
        String::from(
            rand::thread_rng()
            .sample_iter(&rand::distributions::Alphanumeric)
            .take(32)
            .map(char::from)
            .collect::<String>()
        ) + "_database.db"
    );

    // I just make sure the database stays open all the time. :)
    static ref DB: Mutex<Connection> = Mutex::new(
        Connection::open(DB_PATH.lock().unwrap().as_str()).unwrap()
    );
}

// User schema
#[derive(Debug)]
pub struct User {
    pub id: i32,
    pub username: String,
    pub password: String,
    pub role: String,
}

pub struct UserDB<'a> {
    conn: MutexGuard<'a, Connection>,
}

impl UserDB<'_> {
    pub fn new() -> Result<Self, Error> {
        let conn = DB.lock().unwrap();
        Ok(UserDB { conn })
    }

    pub fn init_db(&self) -> Result<(), Error> {
        let conn = &self.conn;
        conn.execute(
            "CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username    TEXT NOT NULL UNIQUE,
                password    TEXT NOT NULL,
                role        TEXT NOT NULL
            )",
            [],
        )?;

        // Generate secure admin password
        let admin_password: String = rand::thread_rng()
            .sample_iter(&rand::distributions::Alphanumeric)
            .take(32)
            .map(char::from)
            .collect();
        // Add admin user
        conn.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            &["dimas", &admin_password, "admin"],
        )?;
        Ok(())
    }

    pub fn add_user<R: AsRef<str>>(&self, username: R, password: R, role: R) -> Result<(), Error> {
        self.conn.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            &[username.as_ref(), password.as_ref(), role.as_ref()],
        )?;
        Ok(())
    }

    pub fn check_user<R: AsRef<str>>(&self, username: R, password: R) -> Result<bool, Error> {
        let count: i64 = self.conn.query_row(
            "SELECT COUNT(*) FROM users WHERE username = ? AND password = ?",
            &[username.as_ref(), password.as_ref()],
            |row| row.get(0),
        )?;
        Ok(count > 0)
    }

    pub fn get_user<R: AsRef<str>>(&self, username: R) -> Result<User, Error> {
        let mut stmt = self
            .conn
            .prepare("SELECT id, username, password, role FROM users WHERE username = ?")?;
        let user = stmt.query_row(&[username.as_ref()], |row| {
            Ok(User {
                id: row.get(0)?,
                username: row.get(1)?,
                password: row.get(2)?,
                role: row.get(3)?,
            })
        });
        user
    }
}
