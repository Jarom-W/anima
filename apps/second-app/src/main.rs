use axum::{
    routing::get,
    Router,
};
use std::net::SocketAddr;

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/health", get(health))
        .route("/version", get(version))
        .route("/info", get(info));

    let addr = SocketAddr::from(([0,0,0,0], 3000));
    println!("Listening on {}", addr);

    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}

async fn health() -> &'static str {
    "ok"
}

async fn version() -> &'static str {
    env!("CARGO_PKG_VERSION")
}

async fn info() -> String {
    format!(
        "service=rhttp-service\nid={}\n",
        std::process::id()
    )
}
