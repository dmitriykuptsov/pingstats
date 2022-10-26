#!/usr/bin/python3

# Copyright (C) 2019 Micromine
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
import threading
# Logging
import logging
from logging.handlers import RotatingFileHandler
# Timing
import time
# System
import sys
# Copy operation
import copy
# Exit handler
import atexit
# Import mathematics
import math
# Import utilities
from utils import checksum
from utils import conversions
from storage import CyclicStorage
# Import mics
from utils import misc
# Import GUI
from ui import ui
# impport garbage collector
import gc

# Define MTU
MTU = 1500

gc.enable()

# Create the ICMP socket
icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, ICMP.ICMP_PROTOCOL_NUMBER);
icmp_socket.bind(("0.0.0.0", ICMP.ICMP_PROTOCOL_NUMBER));
icmp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1);

logging.basicConfig(
	level=logging.DEBUG,
	format="%(asctime)s [%(levelname)s] %(message)s",
	handlers=[
		RotatingFileHandler("pingstats.log", maxBytes=20*1024*1024, backupCount=5),
		logging.StreamHandler(sys.stdout)
	]
);

hosts = misc.Misc.load_hosts("./config/hosts");
logging.info(hosts)
config = misc.Misc.load_config("./config/config");

source_address = config["SOURCE_ADDRESS"]
MAIN_SLEEP_TIME = int(config["MAIN_SLEEP_TIME"])
MAX_TIMEOUT = int(config["MAX_TIMEOUT"])
PROBE_INTERVAL = int(config["PROBE_INTERVAL"])
MAX_SEQUENCE = int(config["MAX_SEQUENCE"])
MAX_RECORDS = int(config["MAX_RECORDS"])
REPORT_INTERVAL = int(config["REPORT_INTERVAL"])

sequences = {}
pending_requests = {}
lock = 0;

storage = CyclicStorage.CyclicStorage(MAX_RECORDS)
logging.info("Starting PINGer");


# Thread lock
lock = threading.Lock()

c = time.time();
for host in hosts:
    sequences[host] = 1;
    storage.put(host, math.inf, c);

def maintanance_loop():
    while True:
        c = time.time()
        logging.debug("Cleaning pending requests....")
        lock.acquire()
        keys = []
        for key in pending_requests.keys():
            keys.append(key)
        keys.sort()
        for key in keys:
            if c - pending_requests[key] > MAX_TIMEOUT:
                logging.info("No response for host %s " % (key))
                storage.put(key.split("_")[0], math.inf, c);
                del pending_requests[key];
        lock.release()
        time.sleep(MAIN_SLEEP_TIME);
    
def send_loop():
    while True:
        logging.debug("Sending ICMP packets.....")
        for host in hosts:
            s = time.time()

            icmp_echo_packet = ICMP.ICMPEchoPacket();
            icmp_echo_packet.set_type(ICMP.ICMP_ECHO_TYPE);
            icmp_echo_packet.set_code(ICMP.ICMP_ECHO_CODE);
            icmp_echo_packet.set_checksum(0);
            icmp_echo_packet.set_identifier(1);
            icmp_echo_packet.set_sequence(sequences[host] % MAX_SEQUENCE);
            icmp_echo_packet.set_payload(bytearray([ord('H'), ord('E'), ord('L'), ord('L'), ord('O'), ord(' '), ord('P'), ord('I'), ord('T'), ord('R'), ord('A'), ord('M')]));
            csum = checksum.Checksum.icmp_checksum(icmp_echo_packet.get_byte_buffer())
            icmp_echo_packet.set_checksum(csum);

            ipv4_packet = IPv4.IPv4Packet();
            ipv4_packet.set_version(IPv4.IPV4_VERSION);
            ipv4_packet.set_destination_address(conversions.Converter.ipv_str_to_bytes(host));
            ipv4_packet.set_source_address(conversions.Converter.ipv_str_to_bytes(source_address));
            ipv4_packet.set_ttl(IPv4.IPV4_DEFAULT_TTL);
            ipv4_packet.set_protocol(ICMP.ICMP_PROTOCOL_NUMBER);
            ipv4_packet.set_ihl(IPv4.IPV4_IHL_NO_OPTIONS);
            ipv4_packet.set_payload(icmp_echo_packet.get_byte_buffer());

            icmp_socket.sendto(bytearray(ipv4_packet.get_buffer()), (host, 0));
            logging.info("Sending to %s" % (host))
            lock.acquire()
            pending_requests[host + "_" + str(sequences[host])] = s
            sequences[host] += 1
            sequences[host] = sequences[host] % MAX_SEQUENCE;
            lock.release()
        time.sleep(PROBE_INTERVAL)

def receive_loop():
    while True:
        buf = bytearray(icmp_socket.recv(MTU));
        c = time.time()
        ipv4_packet = IPv4.IPv4Packet(buf);
        host = conversions.Converter.ipv4_bytes_to_string(ipv4_packet.get_source_address())
        logging.debug("Got IPv4 packet....")
        if ipv4_packet.get_protocol() == ICMP.ICMP_PROTOCOL_NUMBER:
            icmp_packet = ICMP.ICMPPacketFactory.get_packet(ipv4_packet.get_payload())
            checksum_ = icmp_packet.get_checksum()
            icmp_packet.set_checksum(0);
            #logging.info("Got ICMP echo reply (seq %s)" % (str(icmp_packet.get_sequence())))
            if not checksum.Checksum.verify_icmp_checksum(icmp_packet.get_byte_buffer(), checksum_):
                logging.debug("Invalid checksum received")
            elif icmp_packet.get_type() == ICMP.ICMP_DESTINATION_UNREACHABLE_TYPE:
                logging.debug("Destination unreachable %s" % (host));
                #storage.put(host, math.inf, c);
            elif icmp_packet.get_type() == ICMP.ICMP_ECHO_REPLY_TYPE:
                key = host + "_" + str(icmp_packet.get_sequence())
                lock.acquire()
                if pending_requests.get(key, None) == None:
                    logging.critical("No key was found.... Deleted?..... %s" % (key))
                    lock.release();    
                    continue
                logging.info("Got ICMP echo reply (seq %s) from %s in %s ms" % (sequences[host], host, (c-pending_requests.get(key, 0))))
                # It might be so that the ICMP repsonse is too late and we don't have the record in db any more
                if pending_requests.get(key, None) != None:
                    logging.critical("Updating the storage....")
                    storage.put(host, (c - pending_requests[key])*1000, c);
                else:
                    logging.debug("Missing key %s" % (key))
                # Remove unused pending request
                if pending_requests.get(key, None) != None:
                    del pending_requests[key]
                    logging.critical("Deleting pending request %s " % (key))
                lock.release()
            else:
                logging.debug("Unsupported ICMP response")

def gui_loop():
    window = ui.Main(storage)
    window.show();


send_thread = threading.Thread(target = send_loop, args = (), daemon = True);
receive_thread = threading.Thread(target = receive_loop, args = (), daemon = True);
maintenance_thread = threading.Thread(target = maintanance_loop, args = (), daemon = True);

send_thread.start();
receive_thread.start();
maintenance_thread.start();
gui_loop();
