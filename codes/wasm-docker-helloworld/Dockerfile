# syntax=docker/dockerfile:1
FROM scratch
COPY ./target/wasm32-wasi/debug/wasm-docker-helloworld.wasm /hello.wasm
ENTRYPOINT [ "hello.wasm" ]
