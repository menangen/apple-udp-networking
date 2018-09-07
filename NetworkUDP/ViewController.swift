//
//  ViewController.swift
//  NetworkUDP
//
//  Created by menangen on 29.08.2018.
//  Copyright © 2018 menangen. All rights reserved.
//

import UIKit

class ViewController: UIViewController {
    let client: UDPClient
    var packetCounter: UInt16
    
    required init?(coder aDecoder: NSCoder) {
        print("init coder style")
        
        self.client = UDPClient()
        self.packetCounter = 0
        
        super.init(coder: aDecoder)
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        self.view.backgroundColor = UIColor.black
    }

    @IBAction func pressed() {
        self.client.send(self.packetCounter)
        
        self.packetCounter += 1
    }
}
