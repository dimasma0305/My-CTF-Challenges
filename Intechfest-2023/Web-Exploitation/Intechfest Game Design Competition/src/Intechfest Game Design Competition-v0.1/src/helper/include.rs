use std::{fs, path::PathBuf};

use handlebars::{
    Context, Handlebars, Helper, HelperDef, HelperResult, Output, RenderContext, RenderError,
};
use rocket_contrib::templates::handlebars;

// include a another template to current template.
pub struct Include {
    pub default_templates_dir: PathBuf,
}

impl Include {
    pub fn new<P>(default_templates_dir: P) -> Include
    where
        P: Into<PathBuf>,
    {
        Self {
            default_templates_dir: default_templates_dir.into(),
        }
    }
}

impl HelperDef for Include {
    fn call<'reg: 'rc, 'rc>(
        &self,
        h: &Helper,
        _: &Handlebars,
        _: &Context,
        _: &mut RenderContext,
        out: &mut dyn Output,
    ) -> HelperResult {
        match h.param(0) {
            Some(file_name) => {
                let file_path = self.default_templates_dir.join(
                    file_name
                        .value()
                        .as_str()
                        .unwrap()
                        // for security reason
                        .replace("..", ""),
                );
                match fs::read(&file_path) {
                    Ok(res) => {
                        out.write(&String::from_utf8_lossy(&res))?;
                        return Ok(());
                    }
                    Err(err) => return Err(RenderError::new(err.to_string())),
                }
            }
            _ => return Err(RenderError::new("argument not found")),
        }
    }
}
