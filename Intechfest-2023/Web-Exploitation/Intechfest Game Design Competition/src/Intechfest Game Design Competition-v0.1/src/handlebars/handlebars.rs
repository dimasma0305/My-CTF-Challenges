use std::path::PathBuf;

use rocket_contrib::templates::handlebars::Handlebars as mainHandlebars;

use crate::helper::Include;

pub struct Handlebars;

impl Handlebars {
    pub fn new<P: Into<PathBuf>>(default_template_dir: P) -> mainHandlebars {
        let mut handlebars = mainHandlebars::new();
        handlebars.register_helper("include", Box::new(Include::new(default_template_dir)));
        handlebars
    }
}
