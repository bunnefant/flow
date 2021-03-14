/* mbed Example Program
 * Copyright (c) 2006-2014 ARM Limited
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
 
#include "mbed.h"
#include "EthernetInterface.h"
#include "MMA8452.h"
#include "math.h"
#include <format>

// Initialize a pins to perform analog input and digital output fucntions
AnalogIn   ain1(p15);
AnalogIn   ain2(p16);
AnalogIn   ain3(p17);
AnalogIn   ain4(p19);
AnalogIn   ain5(p20);

Timer timer;

int main(void)
{
    sendPackage("device-serial");
    
    double x, y, z;
    double tilt;
    
    AnalogIn *pin_array = {&ain1, &ain2, &ain3, &ain4, &ain5};
    int arrlength = sizeof(pin_array)/sizeof(pin_array[0]);
    timer.start();
    while (1) {
        int num_pos_pins = 0;
        for(int i = 0; i < arrlength; i++) {
            
            if(*pin_array[i] > 0.17f) {
                num_pos_pins++;
            }
        }
        
        if(num_pos_pins < 3) {
            timer.stop();
            timer.reset();
            timer.start();
        } else {
            if (timer.read() > 60f) {
                printf("60 seconds have passed with 3 or more pins reading sufficient voltage");
                sendPackage("status");
                wait(60f);
            }
        }
        wait(1f);
    }
}

void sendPackage(String input) {
    EthernetInterface eth;
    eth.init(); //Use DHCP
    eth.connect();
    printf("IP Address is %s\n", eth.getIPAddress());

    TCPSocketConnection sock;
    sock.connect("ec2-18-206-170-14.compute-1.amazonaws.com", 5000);
    char http_cmd[] = std::format("GET /{}?id=50 HTTP/1.0\n\n", input);
    sock.send_all(http_cmd, sizeof(http_cmd)-1);

    char buffer[300];
    int ret;
    while (true) {
        ret = sock.receive(buffer, sizeof(buffer)-1);
        if (ret <= 0)
            break;
        buffer[ret] = '\0';
        printf("Received %d chars from server:\n%s\n", ret, buffer);
    }

    sock.close();
    eth.disconnect();
}