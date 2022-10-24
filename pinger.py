#!/usr/bin/python3

# Copyright (C) 2019 micromine
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__ = "Dmitriy Kuptsov"
__copyright__ = "Copyright 2022, Micromine"
__license__ = "GPL"
__version__ = "0.0.1b"
__maintainer__ = "Dmitriy Kuptsov"
__email__ = "dkuptsov@micromine.com"
__status__ = "development"

# Import everything from network stuff
from network import ICMP
from network import IPv4

# Import socket
import socket
# Threading
# Logging
import logging
# Timing
import time
# System
import sys
# Exit handler
import atexit
# Import utilities
from utils import checksum
from utils import conversions

# Define MTU
MTU = 1500

# Create the ICMP socket
icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP.ICMP_PROTOCOL_NUMBER);
icmp_socket.bind(("0.0.0.0", ICMP.ICMP_PROTOCOL_NUMBER));
icmp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1);

logging.basicConfig(
	level=logging.DEBUG,
	format="%(asctime)s [%(levelname)s] %(message)s",
	handlers=[
		logging.FileHandler("pingstats.log"),
		logging.StreamHandler(sys.stdout)
	]
);

MAX_SEQUENCE = 2**16 - 1;
seq = 1;
while True:
    s = time.time()
    icmp_echo_packet = ICMP.ICMPEchoPacket();
    icmp_echo_packet.set_type(ICMP.ICMP_ECHO_TYPE);
    icmp_echo_packet.set_code(ICMP.ICMP_ECHO_CODE);
    icmp_echo_packet.set_checksum(0);
    icmp_echo_packet.set_identifier(1);
    icmp_echo_packet.set_sequence(seq % MAX_SEQUENCE);
    icmp_echo_packet.set_payload(bytearray([ord('H'), ord('E'), ord('L'), ord('L'), ord('O'), ord(' '), ord('P'), ord('I'), ord('T'), ord('R'), ord('A'), ord('M')]));

    csum = checksum.Checksum.icmp_checksum(icmp_echo_packet.get_byte_buffer())
    icmp_echo_packet.set_checksum(csum);

    ipv4_packet = IPv4.IPv4Packet();
    ipv4_packet.set_version(IPv4.IPV4_VERSION);
    ipv4_packet.set_destination_address(conversions.Converter.ipv_str_to_bytes("192.168.1.1"));
    ipv4_packet.set_source_address(conversions.Converter.ipv_str_to_bytes("192.168.1.225"));
    ipv4_packet.set_ttl(IPv4.IPV4_DEFAULT_TTL);
    ipv4_packet.set_protocol(ICMP.ICMP_PROTOCOL_NUMBER);
    ipv4_packet.set_ihl(IPv4.IPV4_IHL_NO_OPTIONS);

    ipv4_packet.set_payload(icmp_echo_packet.get_byte_buffer());
    icmp_socket.sendto(bytearray(ipv4_packet.get_buffer()), ("192.168.1.1", 0));

    buf = bytearray(icmp_socket.recv(MTU));
    ipv4_packet = IPv4.IPv4Packet(buf);
    e = time.time()
    
    if ipv4_packet.get_protocol() == ICMP.ICMP_PROTOCOL_NUMBER:
        icmp_packet = ICMP.ICMPPacketFactory.get_packet(ipv4_packet.get_payload())
        checksum_ = icmp_packet.get_checksum()
        icmp_packet.set_checksum(0);
        #logging.debug((icmp_packet.get_byte_buffer()))
        #logging.debug("Got ICMP packet type %s" % (icmp_packet.get_type()))
        if not checksum.Checksum.verify_icmp_checksum(icmp_packet.get_byte_buffer(), checksum_):
            logging.debug("Invalid checksum received")
            time.sleep(1)
            continue;
        if icmp_packet.get_type() == ICMP.ICMP_DESTINATION_UNREACHABLE_TYPE:
            logging.debug("Destination unreachable 192.168.1.10");
        elif icmp_packet.get_type() == ICMP.ICMP_ECHO_REPLY_TYPE:
            logging.debug("Got ICMP echo reply (seq %s) from 192.168.1.10 in %s ms" % (seq, (e-s)))
        else:
            logging.debug("Unsupported ICMP response")
    seq += 1
    time.sleep(1)



