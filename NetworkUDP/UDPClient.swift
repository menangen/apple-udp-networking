//
//  UDPClient.swift
//  NetworkUDP
//
//  Created by menangen on 31.08.2018.
//  Copyright © 2018 menangen. All rights reserved.
//

import Foundation
import Network

class Measure {
    let startTime: CFAbsoluteTime
    
    init() {
        self.startTime = CFAbsoluteTimeGetCurrent()
    }
    
    func end() {
        let delay = CFAbsoluteTimeGetCurrent() - startTime
        let ms = delay * 1000
        
        if delay < 1.0 {
            print("Delay \(ms) ms")
        }
        else {
            print("Delay \(delay) sec")
        }
    }
}

class UDPClient {
    var connection: NWConnection
    var queue: DispatchQueue
    
    init(_ ip: String, _ port: UInt16 = 5000) {
        queue = DispatchQueue(label: "UDP Client Queue")

        //let host = NWEndpoint.Host("novikova.us")
        let host = NWEndpoint.Host.ipv4(IPv4Address(ip)!)
        let port = NWEndpoint.Port(rawValue: port)!
        
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
    
    func send(_ packetCounter: inout UInt16) {
        print(">>>>>>>>>")
        
        func updateCounterWithData(_ data: Data) {
            let number = UInt16(littleEndian: data.withUnsafeBytes { $0.pointee })
            print("Get: UInt (\(number))")
            
            if packetCounter != number && number > 0 {
                packetCounter = number + 1
            }
        }
        
        let data: Data?
        
        if packetCounter == 0 {
            data = "getLast".data(using: .ascii)
        }
        else {
            data = Data(bytes: &packetCounter, count: 2)
        }
        
        print("Sending", data!, "UInt (\(packetCounter))")
        let measure = Measure()
        
        connection.send(content: data, completion: .contentProcessed({
                (error) in
                if let error = error {
                    print("Send error: \(error)")
                }
            })
        )
        
        connection.receive(minimumIncompleteLength: 2, maximumLength: 1024, completion: {
            (data, context, isComplete, error) in
            if data != nil {
                print("Received!", data ?? "Empty content")
                
                updateCounterWithData(data!)
                
                measure.end()
                print()
            }
        })
        print("Sent...")
    }
}
