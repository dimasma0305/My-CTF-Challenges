#![feature(decl_macro)]

mod api;
mod auth;
mod db;
mod handlebars;
mod helper;
mod sanitizer;

use handlebars::Handlebars;
use rocket::http::{RawStr, Status};
use rocket::response::content::Html;
use rocket::response::{status, NamedFile, Responder};
use rocket::{catch, catchers, get, routes};
use rocket_contrib::json::Json;
use rocket_contrib::serve::StaticFiles;
use sanitizer::sanitize;
use serde_json::json;
use std::collections::BTreeMap;
use std::fs;
use std::path::{Path, PathBuf};

macro_rules! render_template {
    ($filename:expr) => {
        render_template!($filename, BTreeMap::new())
    };
    ($filename:expr, $data:expr) => {{
        let template_dir = Path::new("./templates");
        render_template!($filename, $data, template_dir)
    }};
    ($filename:expr, $data:expr, $template_dir:expr) => {{
        let handlebars = Handlebars::new($template_dir);
        let mut data: BTreeMap<String, String> = BTreeMap::new();
        data.extend($data);
        if let Ok(res) = fs::read_to_string($template_dir.join($filename)) {
            let rendered_template = handlebars.render_template(&res, &data).unwrap();
            return Ok(Html(rendered_template));
        } else {
            return Err(Status::NotFound);
        }
    }};
}

#[catch(404)]
fn not_found() -> Result<Html<String>, Status> {
    render_template!("404.hbs")
}

#[catch(401)]
fn unauthorized() -> impl Responder<'static> {
    return status::Custom(
        Status::Unauthorized,
        Json(json!({
            "message": "Unauthorized",
            "status": "error"
        })),
    );
}

#[get("/?<q>")]
fn index(q: Option<&RawStr>) -> Result<Html<String>, Status> {
    if let Some(q_value) = q {
        render_template!(sanitize(q_value))
    }
    render_template!("index.hbs")
}

#[get("/favicon.ico")]
fn favicon() -> Option<NamedFile> {
    // Provide the path to the favicon file
    let path: PathBuf = Path::new("static/favicon.ico").to_owned();
    NamedFile::open(path).ok()
}

fn main() {
    let _ = crate::db::UserDB::new().unwrap().init_db();
    rocket::ignite()
        .mount("/", routes![index, favicon])
        .mount(
            "/api",
            routes![
                crate::api::register,
                crate::api::login,
                crate::api::upload,
                crate::api::api_command
            ],
        )
        .mount("/static", StaticFiles::from("static"))
        .register(catchers![not_found, unauthorized])
        .launch();
}
