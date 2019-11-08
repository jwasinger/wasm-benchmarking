FROM rust

COPY . /wasmi

RUN cd /wasmi && cargo build -j2 --release

ENTRYPOINT ["/wasmi/target/release/wasmi"]
