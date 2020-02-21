//
//  main.swift
//  dns-resolver
//
//  Created by menangen on 11.02.2020.
//  Copyright © 2020 menangen. All rights reserved.
//

import Foundation
import dnssd

let group = DispatchGroup()

let callback: DNSServiceQueryRecordReply = {
    (sdRef, flags, interfaceIndex, errorCode, fullname, rrtype, rrclass, rdlen, rawData, ttl, context) -> Void in
    print(ttl, rdlen)
    
    /*
     let data = Data(bytes: rawData!, count: Int(rdlen))
     let str = String(data: data, encoding: String.Encoding.ascii)
     */
    
    /*
     let uintPointer = UnsafePointer<UInt8>()
     let str = UInt8(uintPointer)
     */
    let memory = rawData!.bindMemory(to: UInt8.self, capacity: 4)
    
    print(memory[0], memory[1], memory[2], memory[3])
    
    //group.leave()
}

func resolveDNS() {
    
    let concurrentQueue = DispatchQueue(label: "queuename", attributes: .concurrent)
    
    var service: DNSServiceRef?
    let domainName = "vienna.novikova.us"
    
    DNSServiceQueryRecord(
        &service,
        kDNSServiceFlagsShared | kDNSServiceFlagsTimeout,
        0,
        domainName,
        UInt16(kDNSServiceType_A),
        UInt16(kDNSServiceClass_IN),
        callback,
        nil)
    
    
    
    let fd = DNSServiceRefSockFD(service)
    print("Socket created", fd)
    
    let eventSource = DispatchSource.makeReadSource(fileDescriptor: fd, queue: concurrentQueue)
    
    eventSource.setEventHandler {
        
        print("DNSServiceProcessResult...")
        let res = DNSServiceProcessResult(service)
        
        if (res != kDNSServiceErr_NoError) { print("There was an error reading the DNS record") }
        group.leave()
    }
    eventSource.setCancelHandler {
        print("Cancel")
        DNSServiceRefDeallocate(service)
        group.leave()
    }
    
    concurrentQueue.asyncAfter(wallDeadline: .now() + 1) { eventSource.cancel() }
    
    group.enter()
    eventSource.resume();
    group.wait()
    
    print("Hello, DNS!")
}
