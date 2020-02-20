//
//  events.swift
//  dns-resolver
//
//  Created by menangen on 20.02.2020.
//  Copyright © 2020 menangen. All rights reserved.
//
import Foundation

struct Position {
    var x, y: UInt16
    
    init(_ x: UInt16, _ y: UInt16) {
        self.x = x
        self.y = y
    }
    
    static
    func decode(coordsPacked: Data) -> Position {
        var x: UInt16 = 0, y: UInt16 = 0
        
        print("Event data:", [UInt8](coordsPacked))

        coordsPacked.withUnsafeBytes {
            x = $0.load(as: UInt16.self).bigEndian
            y = $0.load(fromByteOffset: 2, as: UInt16.self).bigEndian
        }
        return Position(x, y)
    }
}

class Movement: CustomStringConvertible {
    let id: UInt8 = 1
    let ask = true
    
    let from, to: Position
    
    init(from: Position, to: Position) {
        //print("init Position x:\(from), y:\(to)")
        self.from = from
        self.to   = to
    }
    
    static
    func decode(data: Data) -> Movement {
        print("decoding Movement in:", [UInt8](data))
        
        let fromPacked = data[4...7]
        let toPacked   = data[8...11]
        
        let fromPosition = Position.decode(coordsPacked: fromPacked)
        let toPosition   = Position.decode(coordsPacked: toPacked)
        
        return Movement(from: fromPosition, to: toPosition)
    }
    
    var description: String {
        return "Movement[ from: \(self.from), to: \(self.to)]"
    }
}
