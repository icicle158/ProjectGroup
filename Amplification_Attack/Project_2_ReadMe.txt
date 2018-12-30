Name: Avery Berninger
Project: 2
Class: CSE 425



------------WARNING---------------
DO NOT USE DNS SERVER: 8.8.8.8 for name resolution. Google has configured their DNS server to prevent
Denial of Service and Reflection/Amplification attacks (This is done by performing Ratelimiting and Packet Response Size Reduction).
Please use another DNS Server to resolve the query.


Good DNS Servers to try for amplification:
209.244.0.3
216.146.35.35
208.67.222.222




-How does my program work?-

My program works by constructing a packet by using: An IP Header, A UDP Header, A DNS Header, and a DNS Question.
By assigning values to each of the sub-fields within the IP Header, UDP Header, DNS Header, and DNS Question, a packet
is constructed and bound to a socket. Then the user (attacker) sends the packet through the network by issuing a command.
If the packet has been constructed correctly, it will be sent to the specified DNS server on port 53 for website host name resolution.
My packet is constructed with a Source IP (A return address) of the victim's IP Address, thus when the DNS Server sends a 
response back, it is sent to the victim's IP. This is how a reflection attack is implemented. The amplification factor is created by
telling the DNS server to send "ANY" (or ALL) information related to the input website host name (E.X. "www.google.com") to the source
IP Address (Which, in this case, is the T.A.'s IP Address). This information is specified in the DNS Question "Q_type" bit field.
By resolving the website name: ".", and specifying the Q_type to: 255, an amplification factor of x6 - x10 is achieved.


-----------> My packet has an amplification factor between x6 and x10! <--------------

Guide to launching: "Amplification Attack"

Steps:

0.) Open Terminal and use the: "cd" command to change the directory to the path specified in: "step 1.)".
1.) Locate the folder: "\Projects\raw_socket"
2.) Compile: "raw_socket_udp.c" with: "gcc raw_socket_udp.c -o raw_socket_udp.c"
3.) Run program with: "sudo ./raw_socket_udp"
4.) Follow the on-screen instructions
	4.) a.) Enter the T.A.'s IP Address (Or the victim's IP Address)
	4.) b.) Enter the IP Address of the DNS Server
	4.) c.) Press: "Enter" key





Guide to verifying success of: "Amplification Attack"

Steps:

0.) -------> PLEASE install Wireshark on the T.A.'s (Victim's) Computer!!!!!!! This is CRITICAL for program evaluation <----------------
1.) Start Wireshark and observe the packet
2.) Verify amplification and that the program works correctly
1.) Open WireShark on a T.A.'s (Victim's) computer
2.) Execute the "Amplification Attack" from the attacker's computer (Step 3 & 4 in 'Guide to launching: Amplification Attack')
3.) Observe Wireshark to verify that a DNS response has been sent from the DNS server. Also, observe Wireshark to verify the packet
    has been correctly amplified
