//
//  UDPClient.swift
//  NetworkUDP
//
//  Created by menangen on 31.08.2018.
//  Copyright © 2018 menangen. All rights reserved.
//

import Foundation
import Network

class UDPClient {
    var connection: NWConnection
    var queue: DispatchQueue
    
    init() {
        queue = DispatchQueue(label: "UDP Client Queue")

        let host = NWEndpoint.Host.ipv4(IPv4Address("192.168.1.6")!)
        let port = NWEndpoint.Port(rawValue: 5000)!
        //let node: NWEndpoint = NWEndpoint(.v4("localhost"))
        connection = NWConnection(to: .hostPort(host: host, port: port), using: .udp)
        connection.stateUpdateHandler = { (newState) in
            switch (newState) {
            case .ready:
                print("Ready to send")
            case .failed(let e):
                print("Client failed with error \(e)")
            default:
                break
            }
        }
        connection.start(queue: queue)
    }
    
    func send(_ number: UInt16) {
        let message = number == 0 ? "getLast" : String(number)
        let data = message.data(using: .ascii)
        
        print("Sending", data!)
        
        connection.send(content: data, completion: .contentProcessed({
                (error) in
                if let error = error {
                    print("Send error: \(error)")
                }
            })
        )
        
        connection.receive(minimumIncompleteLength: 4, maximumLength: 1024, completion: {
            (data, context, isComplete, error) in
            if data != nil {
                print("Received!", data ?? "Empty content")
                
                // print(String(bytes: data!, encoding: .ascii)!)

                //let array = [UInt8](data!)
                let array = UInt16(bigEndian: data!.withUnsafeBytes { $0.pointee })
                
                print(array)
            }
        })
        print("Sent...")
    }
}
