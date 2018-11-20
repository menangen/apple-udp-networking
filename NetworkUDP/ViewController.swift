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
    
    @IBOutlet weak var textLogArea: UITextView!
    
    required init?(coder aDecoder: NSCoder) {
        print("init coder style")
        
        self.client = UDPClient("192.168.1.5", 54321)
        self.packetCounter = 0
        
        super.init(coder: aDecoder)
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        self.view.backgroundColor = UIColor.black
    }

    func addText(_ value: String) {
        print(value)
        
        DispatchQueue.main.async {
            self.textLogArea.text += value + "\n"
        }
    }
    
    func scrollView() {
        
        DispatchQueue.main.async {
            let range = NSMakeRange(self.textLogArea.text.count - 1, self.textLogArea.text.count - 10)
            self.textLogArea.scrollRangeToVisible(range)
        }
        print()
    }
    
    @IBAction func pressed() {
        if self.packetCounter == 0 {
            self.textLogArea.text = nil
        }
        
        checkKeys();
        
        self.client.send(&self.packetCounter, log: addText, scroll: scrollView)
        
        self.packetCounter += 1
    }
}
