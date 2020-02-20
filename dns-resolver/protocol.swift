//
//  decoder.swift
//  dns-resolver
//
//  Created by menangen on 19.02.2020.
//  Copyright © 2020 menangen. All rights reserved.
//

import Foundation

struct Header {
    let VERSION: UInt8
    let CHUNK: UInt8
    let TOTAL_CHUNKS: UInt8
    let DATA_LENGTH: UInt8
    
    init(_ udpPacket: Data) {
        let header = udpPacket[0...2]
        
        VERSION = header[0]
        CHUNK   = header[1] >> 4
        TOTAL_CHUNKS = header[1] & 0xF
        DATA_LENGTH = header[2]
        
        print("Version: \(VERSION)\t CHUNK: \(CHUNK)\t TOTAL_CHUNKS: \(TOTAL_CHUNKS)\t DATA_LENGTH: \(DATA_LENGTH)")
    }
}

class UDPProto {
    static
    func decode(udpPacket: Data) -> Void {
        let udp = [UInt8](udpPacket)
        print(udp)
        
        let header = Header(udpPacket)
        
        if header.VERSION == 0 {
            let eventData = udpPacket[4...]
            
            let eventType = udpPacket[3]
            let eventID   = eventType & 127
            
            print("Event ID: \(eventID)")
            
            let decoded = Movement.decode(data: eventData)
            
            print(decoded)
        }
        
        else { print("Other UDP protocol") }
    }
}
