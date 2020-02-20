//
//  main.swift
//  dns-resolver
//
//  Created by menangen on 11.02.2020.
//  Copyright © 2020 menangen. All rights reserved.
//

import Foundation
import dnssd

func resolveDNS() {/*
    let group = DispatchGroup()
    
    let callback: DNSServiceQueryRecordReply = {
        (sdRef, flags, interfaceIndex, errorCode, fullname, rrtype, rrclass, rdlen, rawData, ttl, context) -> Void in
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
        print(ttl, Int(rdlen))
        
        group.leave()
    }
    
    let concurrentQueue = DispatchQueue(label: "queuename", attributes: .concurrent)
    
    var service: DNSServiceRef?
    let domainName = "vienna.novikova.us"
    
    let error = DNSServiceQueryRecord(
        &service,
        kDNSServiceFlagsTimeout,
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
        print("Event...")
        
        print("DNSServiceProcessResult")
        let res = DNSServiceProcessResult(service)
        
        if (res != kDNSServiceErr_NoError) { print("There was an error reading the DNS record") }
        
    }
    eventSource.setCancelHandler {
        print("Cancel")
        
        group.leave()
    }
    
    concurrentQueue.asyncAfter(wallDeadline: .now() + 2) { eventSource.cancel() }
    
    group.enter()
    eventSource.resume();
    group.wait()
    
    DNSServiceRefDeallocate(service)*/
    print("Hello, DNS!")
}
