use std::process::Command;

use crate::auth::sign_token;
use crate::db::UserDB;
use rocket::http::{ContentType, Cookie, Cookies, Status};
use rocket::response::status;
use rocket::response::Responder;
use rocket::{post, Data};
use rocket_contrib::json::Json;
use rocket_multipart_form_data::{
    MultipartFormData, MultipartFormDataField, MultipartFormDataOptions, Repetition,
};
use serde::{Deserialize, Serialize};
use serde_json::json;

#[derive(Deserialize, Serialize, Debug)]
pub struct FormUser {
    username: String,
    password: String,
}

#[post("/register", data = "<user_data>")]
pub fn register(user_data: Json<FormUser>) -> impl Responder<'static> {
    match UserDB::new() {
        Ok(manager) => {
            let username = user_data.username.clone();
            let password = user_data.password.clone();
            match manager.add_user(&username, &password, &"guest".to_string()) {
                Ok(()) => make_response(
                    Status::Ok,
                    format!("Successfully created user {}", username),
                ),
                Err(error) => make_response(Status::InternalServerError, error.to_string()),
            }
        }
        Err(error) => make_response(Status::InternalServerError, error.to_string()),
    }
}

#[post("/login", data = "<user_data>")]
pub fn login(user_data: Json<FormUser>, mut cookies: Cookies) -> impl Responder<'static> {
    match UserDB::new() {
        Ok(manager) => {
            let username = user_data.username.clone();
            let password = user_data.password.clone();

            match manager.check_user(&username, &password) {
                Ok(is_exist) => {
                    if is_exist {
                        let token = sign_token(&username, 60).unwrap();
                        let mut cookie = Cookie::new("user", token);
                        cookie.set_path("/");
                        cookies.add(cookie);
                        return make_response(
                            Status::Ok,
                            format!("Successfully logged in as user {}", username),
                        );
                    } else {
                        return make_response(Status::Unauthorized, "Username or password is incorrect!");
                    }
                }
                Err(error) => return make_response(Status::InternalServerError, error.to_string()),
            }
        }
        Err(error) => make_response(Status::InternalServerError, error.to_string()),
    }
}

#[post("/upload", data = "<data>")]
pub fn upload(
    content_type: &ContentType,
    data: Data,
    _auth: crate::auth::AuthenticatedUser,
) -> impl Responder<'static> {
    // multipart options
    let options = MultipartFormDataOptions::with_multipart_form_data_fields(vec![
        MultipartFormDataField::file("gameFile")
            .size_limit(4096)
            .repetition(Repetition::fixed(1)),
        MultipartFormDataField::text("gameTitle")
            .size_limit(255)
            .repetition(Repetition::fixed(1)),
        MultipartFormDataField::text("gameDescription")
            .size_limit(1024)
            .repetition(Repetition::fixed(1)),
    ]);

    match MultipartFormData::parse(content_type, data, options) {
        Ok(multipart_form_data) => {
            let file = multipart_form_data.files.get("gameFile");
            if let Some(file_fields) = file {
                let file_field = &file_fields[0];
                let title = multipart_form_data.texts.get("gameTitle");
                if let Some(title_fields) = title {
                    let title_text = &title_fields.last().unwrap().text;
                    // For security reason i replace ".." with ""
                    let folder_path =
                        std::path::PathBuf::from("uploads").join(title_text.replace("..", ""));
                    if let Err(err) = std::fs::create_dir_all(&folder_path) {
                        return make_response(Status::InternalServerError, err.to_string());
                    };
                    if let Err(err) = std::fs::copy(
                        &file_field.path,
                        folder_path.join(file_field.file_name.clone().unwrap().replace("..", "")),
                    ) {
                        return make_response(Status::InternalServerError, err.to_string());
                    };
                    return make_response(Status::Ok, "File uploaded successfully");
                } else {
                    return make_response(Status::InternalServerError, "Something wrong!");
                }
            } else {
                return make_response(Status::BadRequest, "Game file not found");
            }
        }
        Err(err) => return make_response(Status::InternalServerError, err.to_string()),
    };
}

#[derive(Deserialize, Serialize, Debug)]
pub struct FormCmd {
    cmd: String,
    args: Vec<String>,
}

#[post("/command", data = "<cmd>")]
pub fn api_command(
    cmd: Json<FormCmd>,
    auth: crate::auth::AuthenticatedUser,
) -> impl Responder<'static> {
    if auth.role == "admin" {
        let whitelist = ["rustc", "wget"];
        if whitelist.contains(&cmd.cmd.as_str()) {
            let execute_cmd = Command::new(&cmd.cmd).args(&cmd.args).output();
            if let Ok(output_cmd) = execute_cmd {
                let stdout = String::from_utf8_lossy(&output_cmd.stdout).into_owned();
                return make_response(Status::Ok, stdout);
            } else {
                return make_response(Status::InternalServerError, "Something Wrong!");
            }
        } else {
            return make_response(Status::NotFound, "Command not found!");
        }
    }
    return make_response(Status::Unauthorized, "You're not an admin!");
}

fn make_response<P>(
    status: Status,
    msg: P,
) -> status::Custom<rocket_contrib::json::Json<serde_json::Value>>
where
    P: Into<serde_json::Value>,
{
    return status::Custom(
        status,
        Json(json!({
            "message": msg.into(),
        })),
    );
}
