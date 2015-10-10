#[macro_use]
extern crate lazy_static;
extern crate capnp;
extern crate capnp_rpc;
extern crate cassandra;

use std::collections::HashMap;
use capnp::capability::{Server};
use capnp_rpc::ez_rpc::EzRpcServer;
use cassandra::*;

// this is generated automatically as part of the build process
// see build.rs
pub mod killranswers_capnp {
  include!(concat!(env!("OUT_DIR"), "/killranswers_capnp.rs"));
}
use killranswers_capnp::killr_answers;

// queries for prepared statements
// schema is managed in the python part of the app
// see the cqlengine Models
static CREATE_USER : &'static str = "insert into user (user_id), values (?)";


struct KillrAnswersImpl {
    db: CassSession,
}

impl KillrAnswersImpl {
    // returns a Boxed implemention
    fn new() -> Box<KillrAnswersImpl> {

        let mut cluster = CassCluster::new();
        cluster.set_contact_points("127.0.0.1").unwrap();
        cluster.set_protocol_version(3).unwrap();
        let mut session = CassSession::new().connect(&mut cluster).wait().unwrap();

        Box::new(KillrAnswersImpl{ db: session })
    }
}

impl killr_answers::Server for KillrAnswersImpl {
    // fn ask(&mut self, mut context: killr_answers::AskContext) {
    //     println!("Asking");
    // }
    fn register_user(&mut self, mut context: killr_answers::RegisterUserContext) {
        context.done();
    }

}

fn main() {
    println!("Starting up...");

    let rpc_server = EzRpcServer::new("127.0.0.1:6000").unwrap();
    let ka = Box::new(killr_answers::ServerDispatch { server : KillrAnswersImpl::new() });
    //
    rpc_server.serve(ka);

    println!("Done");
}
