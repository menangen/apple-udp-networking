//
//  main.swift
//  dns-resolver
//
//  Created by menangen on 18.02.2020.
//  Copyright © 2020 menangen. All rights reserved.
//
import Foundation
import Network
import Dispatch

class Server {
    let listener: NWListener
    var queue: DispatchQueue
    
    init(_ port: UInt16 = 5000) {
        queue = DispatchQueue(label: "UDP Server Queue")
        let udpPort = NWEndpoint.Port(rawValue: port)!
        
        listener = try! NWListener(using: .udp, on: udpPort)
        print("Server use \(port) port")
    }
    
    func start() throws {
        print("Server starting...")
        listener.stateUpdateHandler = self.stateDidChange(to:)
        listener.newConnectionHandler = self.didAccept(nwConnection:)
        listener.start(queue: self.queue)
    }
    
    func stateDidChange(to newState: NWListener.State) {
        switch newState {
        case .ready:
            print("Server ready")
        case .failed(let error):
            print("Server failure, error: \(error.localizedDescription)")
            exit(EXIT_FAILURE)
        default:
            break
        }
    }
    
    private func didAccept(nwConnection: NWConnection) {
        nwConnection.start(queue: self.queue)
        
        nwConnection.receive(minimumIncompleteLength: 1, maximumLength: 512) { (data, _, isComplete, error) in
            print("UDP did receive")
            
            if let data = data, !data.isEmpty {
                UDPProto.decode(udpPacket: data)
            }
            if isComplete {
                print("isComplete")
            } else if let error = error {
                print(error)
            } else {
                print("Unexpected Error")
            }
        }
        /*
        let data = "Hello".data(using: .ascii)
        
        nwConnection.send(content: data, completion: .contentProcessed({
            (error) in
            if let error = error {
                print("Send error: \(error)")
            }
        }))*/
    }
}

let s = Server()
try s.start()

// RunLoop.current.run()
sleep(30)
