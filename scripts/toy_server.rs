//! toy_server.rs: a fake web server that never listens (display-only theatre)
mod toy;

use std::collections::HashMap;

fn main() -> Result<(), String> {
    let mut routes: HashMap<u16, String> = HashMap::new();
    routes.insert(8080, "port".to_string());
    routes.entry(9090).or_insert(String::from("alt"));

    for (port, label) in routes {
        println!("route {label}: {port} (no packets harmed)");
    }

    Ok(())
}