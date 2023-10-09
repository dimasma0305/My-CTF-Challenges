use crate::db::UserDB;
use chrono::{Duration, Utc};
use jsonwebtoken::{decode, encode, DecodingKey, EncodingKey, Header, Validation};
use lazy_static;
use rocket::http::Cookie;
use rocket::request::{FromRequest, Outcome};
use rocket::{http::Status, Request};
use serde::{Deserialize, Serialize};
use std::sync::Mutex;

lazy_static::lazy_static! {
    pub static ref JWT_SECRET: Mutex<Vec<u8>> = Mutex::new((0..32).map(|_| rand::random()).collect());
}

#[derive(Deserialize, Serialize, Debug)]
pub struct UserClaims {
    pub username: String,
    pub password: String,
    pub exp: i64,
}
pub struct AuthenticatedUser {
    pub username: String,
    pub role: String,
}

// Implement authentication
impl<'a, 'r> FromRequest<'a, 'r> for AuthenticatedUser {
    type Error = ();

    fn from_request(request: &'a Request<'r>) -> Outcome<Self, Self::Error> {
        if let Some(user_cookie) = request.cookies().get("user") {
            if let Ok(authenticated_user) = get_authenticated_user(user_cookie.clone()) {
                return Outcome::Success(authenticated_user);
            }
        }
        Outcome::Failure((Status::Unauthorized, ()))
    }
}

fn get_authenticated_user(cookie: Cookie) -> Result<AuthenticatedUser, ()> {
    if let Ok(user_claim) = decode_token(&cookie.value()) {
        if let Ok(db) = UserDB::new() {
            let username = &user_claim.claims.username;
            if let Ok(user) = db.get_user(username) {
                return Ok(AuthenticatedUser {
                    username: user.username,
                    role: user.role,
                });
            }
        }
    }
    Err(())
}

pub fn sign_token<P: Into<String>>(
    username: P,
    expiration_minutes: i64,
) -> Result<String, jsonwebtoken::errors::Error> {
    let secret = JWT_SECRET.lock().unwrap();
    let encoding_key = EncodingKey::from_secret(secret.as_ref());

    let expiration = Utc::now() + Duration::minutes(expiration_minutes);
    let claims_with_exp = UserClaims {
        exp: expiration.timestamp(),
        username: username.into(),
        password: "".to_string(),
    };

    encode(&Header::default(), &claims_with_exp, &encoding_key)
}

pub fn decode_token(
    token: &str,
) -> Result<jsonwebtoken::TokenData<UserClaims>, jsonwebtoken::errors::Error> {
    let secret = JWT_SECRET.lock().unwrap();
    let decoding_key = DecodingKey::from_secret(secret.as_ref());
    let validation = Validation::default();
    decode::<UserClaims>(token, &decoding_key, &validation)
}
