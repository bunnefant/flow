#include "mbed.h"
#include "EthernetInterface.h"

int main() {
    EthernetInterface eth;
    eth.init(); //Use DHCP
    eth.connect();
    printf("IP Address is %s\n", eth.getIPAddress());

    TCPSocketConnection sock;
    sock.connect("ec2-18-206-170-14.compute-1.amazonaws.com", 5000);
    char http_cmd[] = "GET /device-serial?id=50 HTTP/1.0\n\n";
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

    while(1) {}
}
