#!/usr/bin/python

# Copyright (C) 2022 Micromine

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

ICMP_PROTOCOL_NUMBER = 0x1;

ICMP_TYPE_OFFSET = 0
class ICMPPacket():
    """
    Generic ICMP packet
    """
    def __init__(self, buffer = None):
        """
        Initializes the packet with the values
        """
        self.buffer = buffer
    
    def get_type(self):
        """
        Returns type of the ICMP packet
        """
        return self.buffer[ICMP_TYPE_OFFSET] & 0xFF;

    def get_byte_buffer(self):
        """
        Returns packet buffer
        """
        return self.buffer;

class ICMPPacketFactory():
    @staticmethod
    def get_packet(buf):
        icmp_packet = ICMPPacket(buf);
        type = icmp_packet.get_type();
        if type == ICMP_DESTINATION_UNREACHABLE_TYPE:
            return ICMPDestinationUnreachablePacket(buf)
        elif type == ICMP_TIME_EXEEDED_TYPE:
            return ICMPTimeExceededPacket(buf)
        elif type == ICMP_SOURCE_QUENCH_TYPE:
            return ICMPSourceQuenchPacket(buf)
        elif type == ICMP_ECHO_REPLY_TYPE:
            packet = ICMPEchoPacket(buf)
            return packet
        elif type == ICMP_INFORMATION_TYPE:
            return ICMPInformationPacket(buf)
        else:
            raise Exception("Unsupported ICMP packet type")

    
ICMP_DESTINATION_UNREACHABLE_LENGTH = 0x10;
ICMP_DESTINATION_UNREACHABLE_TYPE = 0x3;
ICMP_DESTINATION_UNREACHABLE_TYPE_OFFSET = 0x0;
ICMP_DESTINATION_UNREACHABLE_CODE_OFFSET = 0x1;
ICMP_DESTINATION_UNREACHABLE_CHECKSUM_OFFSET = 0x2;
ICMP_DESTINATION_UNREACHABLE_CHECKSUM_LENGTH = 0x2;
ICMP_DESTINATION_UNREACHABLE_PAYLOAD_OFFSET = 0x8;
ICMP_DESTINATION_UNREACHABLE_PAYLOAD_LENGTH = 0x8;

class ICMPDestinationUnreachablePacket(ICMPPacket):
    """
    Destination unreachable packet
    """
    def __init__(self, buffer = None):
        if not buffer:
            self.buffer = [0]*ICMP_DESTINATION_UNREACHABLE_LENGTH;
            self.set_type(ICMP_DESTINATION_UNREACHABLE_TYPE & 0xFF)
        else:
            self.buffer = buffer;
    def get_type(self):
        """
        Returns ICMP packet type
        """
        return self.buffer[ICMP_DESTINATION_UNREACHABLE_TYPE_OFFSET] & 0xFF;
    def set_type(self, type):
        """
        Sets type of the ICMP packet
        """
        self.buffer[ICMP_DESTINATION_UNREACHABLE_TYPE_OFFSET] = type & 0xFF;
    def get_code(self):
        """
        Returns ICMP code
        """
        return self.buffer[ICMP_DESTINATION_UNREACHABLE_CODE_OFFSET] & 0xFF;
    def set_code(self, code):
        """
        Sets the code of the ICMP packet
        """
        self.buffer[ICMP_DESTINATION_UNREACHABLE_CODE_OFFSET] = code & 0xFF;
    def get_checksum(self):
        """
        Returns packet checksum
        """
        return ((self.buffer[ICMP_DESTINATION_UNREACHABLE_CHECKSUM_OFFSET] << 8) & 0XFFFF |
            self.buffer[ICMP_DESTINATION_UNREACHABLE_CHECKSUM_OFFSET + 1] & 0XFF)
    def set_checksum(self, checksum):
        """
        Gets the checksum
        """
        self.buffer[ICMP_DESTINATION_UNREACHABLE_CHECKSUM_OFFSET] = (checksum >> 8) & 0xFF
        self.buffer[ICMP_DESTINATION_UNREACHABLE_CHECKSUM_OFFSET + 1] = checksum & 0XFF;
    def get_payload(self):
        return self.buffer[ICMP_DESTINATION_UNREACHABLE_PAYLOAD_OFFSET:]
    def set_payload(self, payload):
        if len(payload) != 0x8:
            raise Exception("The payload should be 64 bits")
        self.buffer[ICMP_DESTINATION_UNREACHABLE_PAYLOAD_OFFSET:] = payload;


ICMP_TIME_EXEEDED_LENGTH = 0x10;
ICMP_TIME_EXEEDED_TYPE = 0xB;
ICMP_TIME_EXEEDED_TYPE_OFFSET = 0x0;
ICMP_TIME_EXEEDED_CODE_OFFSET = 0x1;
ICMP_TIME_EXEEDED_CHECKSUM_OFFSET = 0x2;
ICMP_TIME_EXEEDED_CHECKSUM_LENGTH = 0x2;
ICMP_TIME_EXEEDED_PAYLOAD_OFFSET = 0x8;
ICMP_TIME_EXEEDED_PAYLOAD_LENGTH = 0x8;

class ICMPTimeExceededPacket(ICMPPacket):
    """
    ICMP time exceeded packet
    """
    def __init__(self, buffer = None):
        if not buffer:
            self.buffer = [0]*ICMP_TIME_EXEEDED_LENGTH;
            self.set_type(ICMP_TIME_EXEEDED_TYPE & 0xFF)
        else:
            self.buffer = buffer;
    def get_type(self):
        """
        Returns ICMP packet type
        """
        return self.buffer[ICMP_TIME_EXEEDED_TYPE_OFFSET] & 0xFF;
    def set_type(self, type):
        """
        Sets type of the ICMP packet
        """
        self.buffer[ICMP_TIME_EXEEDED_TYPE_OFFSET] = type & 0xFF;
    def get_code(self):
        """
        Returns ICMP code
        """
        return self.buffer[ICMP_TIME_EXEEDED_CODE_OFFSET] & 0xFF;
    def set_code(self, code):
        """
        Sets the code of the ICMP packet
        """
        self.buffer[ICMP_TIME_EXEEDED_CHECKSUM_OFFSET] = code & 0xFF;
    def get_checksum(self):
        """
        Returns packet checksum
        """
        return ((self.buffer[ICMP_TIME_EXEEDED_CHECKSUM_OFFSET] << 8) & 0XFFFF |
            self.buffer[ICMP_TIME_EXEEDED_CHECKSUM_OFFSET + 1] & 0XFF)
    def set_checksum(self, checksum):
        """
        Gets the checksum
        """
        self.buffer[ICMP_TIME_EXEEDED_CHECKSUM_OFFSET] = (checksum >> 8) & 0xFF
        self.buffer[ICMP_TIME_EXEEDED_CHECKSUM_OFFSET + 1] = checksum & 0XFF;
    def get_payload(self):
        """
        Gets the ICMP payload
        """
        return self.buffer[ICMP_TIME_EXEEDED_PAYLOAD_OFFSET:]
    def set_payload(self, payload):
        """
        Sets the payload of the ICMP packet
        """
        if len(payload) != 0x8:
            raise Exception("The payload should be 64 bits")
        self.buffer[ICMP_TIME_EXEEDED_PAYLOAD_OFFSET:] = payload;

ICMP_SOURCE_QUENCH_LENGTH = 0x10;
ICMP_SOURCE_QUENCH_TYPE = 0x4;
ICMP_SOURCE_QUENCH_TYPE_OFFSET = 0x0;
ICMP_SOURCE_QUENCH_CODE_OFFSET = 0x1;
ICMP_SOURCE_QUENCH_CHECKSUM_OFFSET = 0x2;
ICMP_SOURCE_QUENCH_CHECKSUM_LENGTH = 0x2;
ICMP_SOURCE_QUENCH_PAYLOAD_OFFSET = 0x8;
ICMP_SOURCE_QUENCH_PAYLOAD_LENGTH = 0x8;

class ICMPSourceQuenchPacket(ICMPPacket):
    """
    ICMP source quench packet
    """
    def __init__(self, buffer = None):
        if not buffer:
            self.buffer = [0]*ICMP_SOURCE_QUENCH_LENGTH;
            self.set_type(ICMP_SOURCE_QUENCH_TYPE & 0xFF)
        else:
            self.buffer = buffer;
    def get_type(self):
        """
        Returns ICMP packet type
        """
        return self.buffer[ICMP_SOURCE_QUENCH_TYPE_OFFSET] & 0xFF;
    def set_type(self, type):
        """
        Sets type of the ICMP packet
        """
        self.buffer[ICMP_SOURCE_QUENCH_TYPE_OFFSET] = type & 0xFF;
    def get_code(self):
        """
        Returns ICMP DU code
        """
        return self.buffer[ICMP_SOURCE_QUENCH_CODE_OFFSET] & 0xFF;
    def set_code(self, code):
        """
        Sets the code of the ICMP DU packet
        """
        self.buffer[ICMP_SOURCE_QUENCH_CODE_OFFSET] = code & 0xFF;
    def get_checksum(self):
        """
        Returns packet checksum
        """
        return ((self.buffer[ICMP_SOURCE_QUENCH_CHECKSUM_OFFSET] << 8) & 0XFFFF |
            self.buffer[ICMP_SOURCE_QUENCH_CHECKSUM_OFFSET + 1] & 0XFF)
    def set_checksum(self, checksum):
        """
        Gets the checksum
        """
        self.buffer[ICMP_SOURCE_QUENCH_CHECKSUM_OFFSET] = (checksum >> 8) & 0xFF
        self.buffer[ICMP_SOURCE_QUENCH_CHECKSUM_OFFSET + 1] = checksum & 0XFF;
    def get_payload(self):
        """
        Gets the ICMP payload
        """
        return self.buffer[ICMP_SOURCE_QUENCH_PAYLOAD_OFFSET:]
    def set_payload(self, payload):
        """
        Sets the payload of the ICMP packet
        """
        if len(payload) != 0x8:
            raise Exception("The payload should be 64 bits")
        self.buffer[ICMP_SOURCE_QUENCH_PAYLOAD_OFFSET:] = payload;

ICMP_REDIRECT_LENGTH = 0x10;
ICMP_REDIRECT_TYPE = 0x5;
ICMP_REDIRECT_TYPE_OFFSET = 0x0;
ICMP_REDIRECT_CODE_OFFSET = 0x1;
ICMP_REDIRECT_CHECKSUM_OFFSET = 0x2;
ICMP_REDIRECT_CHECKSUM_LENGTH = 0x2;
ICMP_REDIRECT_GATEWAY_ADDRESS_OFFSET = 0x4;
ICMP_REDIRECT_GATEWAY_ADDRESS_LENGTH = 0x4;
ICMP_REDIRECT_PAYLOAD_OFFSET = 0x8;
ICMP_REDIRECT_PAYLOAD_LENGTH = 0x8;

class ICMPRedirectPacket(ICMPPacket):
    """
    ICMP redirect packet
    """
    def __init__(self, buffer = None):
        if not buffer:
            self.buffer = [0]*ICMP_REDIRECT_LENGTH;
            self.set_type(ICMP_REDIRECT_TYPE & 0xFF)
        else:
            self.buffer = buffer;
    def get_type(self):
        """
        Returns ICMP packet type
        """
        return self.buffer[ICMP_REDIRECT_TYPE_OFFSET] & 0xFF;
    def set_type(self, type):
        """
        Sets type of the ICMP packet
        """
        self.buffer[ICMP_REDIRECT_TYPE_OFFSET] = type & 0xFF;
    def get_code(self):
        """
        Returns ICMP DU code
        """
        return self.buffer[ICMP_REDIRECT_CODE_OFFSET] & 0xFF;
    def set_code(self, code):
        """
        Sets the code of the ICMP DU packet
        """
        self.buffer[ICMP_REDIRECT_CODE_OFFSET] = code & 0xFF;
    def get_checksum(self):
        """
        Returns packet checksum
        """
        return ((self.buffer[ICMP_REDIRECT_CHECKSUM_OFFSET] << 8) & 0XFFFF |
            self.buffer[ICMP_REDIRECT_CHECKSUM_OFFSET + 1] & 0XFF)
    def set_checksum(self, checksum):
        """
        Gets the checksum
        """
        self.buffer[ICMP_REDIRECT_CHECKSUM_OFFSET] = (checksum >> 8) & 0xFF
        self.buffer[ICMP_REDIRECT_CHECKSUM_OFFSET + 1] = checksum & 0XFF;
    def get_gateway_address(self):
        """
        Returns gateway address
        """
        return self.buffer[ICMP_REDIRECT_GATEWAY_ADDRESS_OFFSET:ICMP_REDIRECT_GATEWAY_ADDRESS_OFFSET+ICMP_REDIRECT_GATEWAY_ADDRESS_LENGTH];
    def set_gateway_address(self, address):
        if len(address) != 0x4:
            raise Exception("Gateway address must be 4 bytes long");
        self.buffer[ICMP_REDIRECT_GATEWAY_ADDRESS_OFFSET:ICMP_REDIRECT_GATEWAY_ADDRESS_OFFSET+ICMP_REDIRECT_GATEWAY_ADDRESS_LENGTH] = address;
    def get_payload(self):
        """
        Gets the ICMP payload
        """
        return self.buffer[ICMP_REDIRECT_PAYLOAD_OFFSET:]
    def set_payload(self, payload):
        """
        Sets the payload of the ICMP packet
        """
        if len(payload) != 0x8:
            raise Exception("The payload should be 64 bits")
        self.buffer[ICMP_REDIRECT_PAYLOAD_OFFSET:] = payload;

ICMP_ECHO_CODE = 0x0
ICMP_ECHO_LENGTH = 0x10;
ICMP_ECHO_TYPE = 0x8;
ICMP_ECHO_REPLY_TYPE = 0x0;
ICMP_ECHO_OFFSET = 0x0;
ICMP_ECHO_OFFSET_LENGTH = 0x1;
ICMP_ECHO_CODE_OFFSET = 0x1;
ICMP_ECHO_CHECKSUM_OFFSET = 0x2;
ICMP_ECHO_CHECKSUM_LENGTH = 0x2;
ICMP_ECHO_IDENTIFIER_OFFSET = 0x4;
ICMP_ECHO_IDENTIFIER_LENGTH = 0x2;
ICMP_ECHO_SEQUENCE_NUMBER_OFFSET = 0x6;
ICMP_ECHO_SEQUENCE_NUMBER_LENGTH = 0x2;
ICMP_ECHO_PAYLOAD_OFFSET = 0x8;
ICMP_MAX_PAYLOAD_SIZE = 0x598;

class ICMPEchoPacket(ICMPPacket):
    """
    ICMP echo packet
    """
    def __init__(self, buffer = None, type = ICMP_ECHO_TYPE):
        if not buffer:
            self.buffer = [0]*ICMP_ECHO_LENGTH;
            self.set_type(type & 0xFF)
        else:
            self.buffer = buffer;
    def get_type(self):
        """
        Returns ICMP packet type
        """
        return self.buffer[ICMP_ECHO_OFFSET] & 0xFF;
    def set_type(self, type):
        """
        Sets type of the ICMP packet
        """
        self.buffer[ICMP_ECHO_OFFSET] = (type & 0xFF);
    def get_code(self):
        """
        Returns ICMP code
        """
        return self.buffer[ICMP_ECHO_CODE_OFFSET] & 0xFF;
    def set_code(self, code):
        """
        Sets the code of the ICMP packet
        """
        self.buffer[ICMP_ECHO_CODE_OFFSET] = code & 0xFF;
    def get_checksum(self):
        """
        Returns packet checksum
        """
        return ((self.buffer[ICMP_ECHO_CHECKSUM_OFFSET] << 8) & 0XFFFF |
            self.buffer[ICMP_ECHO_CHECKSUM_OFFSET + 1] & 0XFF)
    def set_checksum(self, checksum):
        """
        Gets the checksum
        """
        self.buffer[ICMP_ECHO_CHECKSUM_OFFSET] = (checksum >> 8) & 0xFF
        self.buffer[ICMP_ECHO_CHECKSUM_OFFSET + 1] = checksum & 0XFF;
    def get_identifier(self):
        """
        Returns identifier
        """
        return (((self.buffer[ICMP_ECHO_IDENTIFIER_OFFSET] << 8) & 0xFFFF) | 
            (self.buffer[ICMP_ECHO_IDENTIFIER_OFFSET + 1] & 0xFF));
    def set_identifier(self, identifier):
        """
        Sets the identifier
        """
        self.buffer[ICMP_ECHO_IDENTIFIER_OFFSET] = (identifier >> 8) & 0xFF;
        self.buffer[ICMP_ECHO_IDENTIFIER_OFFSET + 1] = (identifier & 0xFF);
    def set_sequence(self, sequence):
        """
        Sets the sequence of the echo packet
        """
        self.buffer[ICMP_ECHO_SEQUENCE_NUMBER_OFFSET] = (sequence >> 8) & 0xFF;
        self.buffer[ICMP_ECHO_SEQUENCE_NUMBER_OFFSET + 1] = (sequence & 0xFF);
    def get_sequence(self):
        """
        Gets the ICMP Echo sequence
        """
        return (((self.buffer[ICMP_ECHO_SEQUENCE_NUMBER_OFFSET] << 8) & 0xFFFF) | 
            (self.buffer[ICMP_ECHO_SEQUENCE_NUMBER_OFFSET + 1] & 0xFF));
    def set_payload(self, payload):
        """
        Sets the payload of the ICMP packet
        """
        if len(payload) > ICMP_MAX_PAYLOAD_SIZE:
            raise Exception("The payload should be less than 1432 bytes")
        self.buffer[ICMP_ECHO_PAYLOAD_OFFSET:] = payload;
    def get_payload(self):
        """
        Gets the payload of the ICMP Echo packet
        """
        return self.buffer[ICMP_ECHO_PAYLOAD_OFFSET:];

ICMP_TIMESTAMP_LENGTH = 0x14;
ICMP_TIMESTAMP_TYPE = 0xD;
ICMP_TIMESTAMP_REPLY_TYPE = 0xE;
ICMP_TIMESTAMP_TYPE_OFFSET = 0x0;
ICMP_TIMESTAMP_CODE_OFFSET = 0x0;
ICMP_TIMESTAMP_CHECKSUM_OFFSET = 0x2;
ICMP_TIMESTAMP_CHECKSUM_LENGTH = 0x2;
ICMP_TIMESTAMP_IDENTIFIER_OFFSET = 0x4;
ICMP_TIMESTAMP_IDENTIFIER_LENGTH = 0x2;
ICMP_TIMESTAMP_SEQUENCE_OFFSET = 0x6;
ICMP_TIMESTAMP_SEQUENCE_LENGTH = 0x2;
ICMP_TIMESTAMP_ORIGINATE_OFFSET = 0x8;
ICMP_TIMESTAMP_ORIGINATE_LENGTH = 0x4;
ICMP_TIMESTAMP_RECEIVE_OFFSET = 0x8;
ICMP_TIMESTAMP_RECEIVE_LENGTH = 0x4;
ICMP_TIMESTAMP_TRANSMIT_OFFSET = 0x8;
ICMP_TIMESTAMP_TRANSMIT_LENGTH = 0x4;

class ICMPTimestampPacket(ICMPPacket):
    """
    ICMP timestampt packet
    """
    def __init__(self, buffer = None, type = ICMP_TIMESTAMP_TYPE):
        if not buffer:
            self.buffer = [0]*ICMP_ECHO_LENGTH;
            self.set_type(type & 0xFF)
        else:
            self.buffer = buffer;
    def get_type(self):
        """
        Returns ICMP packet type
        """
        return self.buffer[ICMP_TIMESTAMP_TYPE_OFFSET] & 0xFF;
    def set_type(self, type):
        """
        Sets type of the ICMP packet
        """
        self.buffer[ICMP_TIMESTAMP_TYPE_OFFSET] = type & 0xFF;
    def get_code(self):
        """
        Returns ICMP code
        """
        return self.buffer[ICMP_ECHO_CODE_OFFSET] & 0xFF;
    def set_code(self, code):
        """
        Sets the code of the ICMP packet
        """
        self.buffer[ICMP_ECHO_CODE_OFFSET] = code & 0xFF;
    def get_checksum(self):
        """
        Returns packet checksum
        """
        return ((self.buffer[ICMP_ECHO_CHECKSUM_OFFSET] << 8) & 0XFFFF |
            self.buffer[ICMP_ECHO_CHECKSUM_OFFSET + 1] & 0XFF)
    def set_checksum(self, checksum):
        """
        Gets the checksum
        """
        self.buffer[ICMP_ECHO_CHECKSUM_OFFSET] = (checksum >> 8) & 0xFF
        self.buffer[ICMP_ECHO_CHECKSUM_OFFSET + 1] = checksum & 0XFF;
    def get_identifier(self):
        """
        Returns identifier
        """
        return (((self.buffer[ICMP_TIMESTAMP_IDENTIFIER_OFFSET] << 8) & 0xFFFF) | 
            (self.buffer[ICMP_TIMESTAMP_IDENTIFIER_OFFSET + 1] & 0xFF));
    def set_identifier(self, identifier):
        """
        Sets the identifier
        """
        self.buffer[ICMP_TIMESTAMP_IDENTIFIER_OFFSET] = (identifier >> 8) & 0xFF;
        self.buffer[ICMP_TIMESTAMP_IDENTIFIER_OFFSET + 1] = (identifier & 0xFF);
    def set_sequence(self, sequence):
        """
        Sets the sequence of the ICMP timestamp packet
        """
        self.buffer[ICMP_TIMESTAMP_SEQUENCE_OFFSET] = (sequence >> 8) & 0xFF;
        self.buffer[ICMP_TIMESTAMP_SEQUENCE_OFFSET + 1] = (sequence & 0xFF);
    def get_sequence(self):
        """
        Gets the ICMP timestamp sequence
        """
        return (((self.buffer[ICMP_TIMESTAMP_SEQUENCE_OFFSET] << 8) & 0xFFFF) | \
            (self.buffer[ICMP_TIMESTAMP_SEQUENCE_OFFSET + 1] & 0xFF));
    def get_originate_timestamp(self):
        """
        Returns originate timestamp
        """
        return ((self.buffer[ICMP_TIMESTAMP_ORIGINATE_OFFSET] << 24) & 0xFFFFFFFF) | \
            ((self.buffer[ICMP_TIMESTAMP_ORIGINATE_OFFSET + 1] << 16) & 0xFFFFFF) | \
            ((self.buffer[ICMP_TIMESTAMP_ORIGINATE_OFFSET + 2] << 8) & 0xFFFF) | \
            ((self.buffer[ICMP_TIMESTAMP_ORIGINATE_OFFSET + 1]) & 0xFF);
    def set_originate_timestamp(self, timestamp):
        """
        Sets originate timestamp
        """
        self.buffer[ICMP_TIMESTAMP_ORIGINATE_OFFSET] = (timestamp >> 24) & 0xFF;
        self.buffer[ICMP_TIMESTAMP_ORIGINATE_OFFSET + 1] = (timestamp >> 16) & 0xFF;
        self.buffer[ICMP_TIMESTAMP_ORIGINATE_OFFSET + 2] = (timestamp >> 8) & 0XFF;
        self.buffer[ICMP_TIMESTAMP_ORIGINATE_OFFSET + 3] = (timestamp & 0xFF);
    def get_receive_timestamp(self):
        """
        Returns receive timestamp
        """
        return ((self.buffer[ICMP_TIMESTAMP_RECEIVE_OFFSET] << 24) & 0xFFFFFFFF) | \
            ((self.buffer[ICMP_TIMESTAMP_RECEIVE_OFFSET + 1] << 16) & 0xFFFFFF) | \
            ((self.buffer[ICMP_TIMESTAMP_RECEIVE_OFFSET + 2] << 8) & 0xFFFF) | \
            ((self.buffer[ICMP_TIMESTAMP_RECEIVE_OFFSET + 3]) & 0xFF);
    def set_receive_timestamp(self, timestamp):
        """
        Sets receive timestamp
        """
        self.buffer[ICMP_TIMESTAMP_RECEIVE_OFFSET] = (timestamp >> 24) & 0xFF;
        self.buffer[ICMP_TIMESTAMP_RECEIVE_OFFSET + 1] = (timestamp >> 16) & 0xFF;
        self.buffer[ICMP_TIMESTAMP_RECEIVE_OFFSET + 2] = (timestamp >> 8) & 0XFF;
        self.buffer[ICMP_TIMESTAMP_RECEIVE_OFFSET + 3] = (timestamp & 0xFF);
    def get_receive_timestamp(self):
        """
        Returns receive timestamp
        """
        return ((self.buffer[ICMP_TIMESTAMP_TRANSMIT_OFFSET] << 24) & 0xFFFFFFFF) | \
            ((self.buffer[ICMP_TIMESTAMP_TRANSMIT_OFFSET + 1] << 16) & 0xFFFFFF) | \
            ((self.buffer[ICMP_TIMESTAMP_TRANSMIT_OFFSET + 2] << 8) & 0xFFFF) | \
            ((self.buffer[ICMP_TIMESTAMP_TRANSMIT_OFFSET + 3]) & 0xFF);
    def set_receive_timestamp(self, timestamp):
        """
        Sets receive timestamp
        """
        self.buffer[ICMP_TIMESTAMP_TRANSMIT_OFFSET] = (timestamp >> 24) & 0xFF;
        self.buffer[ICMP_TIMESTAMP_TRANSMIT_OFFSET + 1] = (timestamp >> 16) & 0xFF;
        self.buffer[ICMP_TIMESTAMP_TRANSMIT_OFFSET + 2] = (timestamp >> 8) & 0XFF;
        self.buffer[ICMP_TIMESTAMP_TRANSMIT_OFFSET + 3] = (timestamp & 0xFF);
    

ICMP_INFORMATION_LENGTH = 0x10;
ICMP_INFORMATION_TYPE = 0xF;
ICMP_INFORMATION_REPLY_TYPE = 0x10;
ICMP_INFORMATION_TYPE_OFFSET = 0x0;
ICMP_INFORMATION_TYPE_OFFSET_LENGTH = 0x1;
ICMP_INFORMATION_CODE_OFFSET = 0x0;
ICMP_INFORMATION_CHECKSUM_OFFSET = 0x2;
ICMP_INFORMATION_CHECKSUM_LENGTH = 0x2;
ICMP_INFORMATION_IDENTIFIER_OFFSET = 0x4;
ICMP_INFORMATION_IDENTIFIER_LENGTH = 0x2;
ICMP_INFORMATION_SEQUENCE_NUMBER_OFFSET = 0x6;
ICMP_INFORMATION_SEQUENCE_NUMBER_LENGTH = 0x2;

class ICMPInformationPacket(ICMPPacket):
    """
    Information packet
    """
    def __init__(self, buffer = None):
        if not buffer:
            self.buffer = [0]*ICMP_INFORMATION_LENGTH;
            self.set_type(ICMP_INFORMATION_TYPE & 0xFF)
        else:
            self.buffer = buffer;
    def get_type(self):
        """
        Returns ICMP packet type
        """
        return self.buffer[ICMP_INFORMATION_TYPE_OFFSET] & 0xFF;
    def set_type(self, type):
        """
        Sets type of the ICMP packet
        """
        self.buffer[ICMP_INFORMATION_TYPE_OFFSET] = type & 0xFF;
    def get_code(self):
        """
        Returns ICMP code
        """
        return self.buffer[ICMP_INFORMATION_CODE_OFFSET] & 0xFF;
    def set_code(self, code):
        """
        Sets the code of the ICMP packet
        """
        self.buffer[ICMP_INFORMATION_CODE_OFFSET] = code & 0xFF;
    def get_checksum(self):
        """
        Returns packet checksum
        """
        return ((self.buffer[ICMP_INFORMATION_CHECKSUM_OFFSET] << 8) & 0XFFFF | \
            self.buffer[ICMP_INFORMATION_CHECKSUM_OFFSET + 1] & 0XFF)
    def set_checksum(self, checksum):
        """
        Gets the checksum
        """
        self.buffer[ICMP_INFORMATION_CHECKSUM_OFFSET] = (checksum >> 8) & 0xFF
        self.buffer[ICMP_INFORMATION_CHECKSUM_OFFSET + 1] = checksum & 0XFF;
    def get_identifier(self):
        """
        Returns identifier
        """
        return (((self.buffer[ICMP_INFORMATION_IDENTIFIER_OFFSET] << 8) & 0xFFFF) | 
            (self.buffer[ICMP_INFORMATION_IDENTIFIER_OFFSET + 1] & 0xFF));
    def set_identifier(self, identifier):
        """
        Sets the identifier
        """
        self.buffer[ICMP_INFORMATION_IDENTIFIER_OFFSET] = (identifier >> 8) & 0xFF;
        self.buffer[ICMP_INFORMATION_IDENTIFIER_OFFSET + 1] = (identifier & 0xFF);
    def set_sequence(self, sequence):
        """
        Sets the sequence of the echo packet
        """
        self.buffer[ICMP_INFORMATION_SEQUENCE_NUMBER_OFFSET] = (sequence >> 8) & 0xFF;
        self.buffer[ICMP_INFORMATION_SEQUENCE_NUMBER_OFFSET + 1] = (sequence & 0xFF);
    def get_sequence(self):
        """
        Gets the ICMP Echo sequence
        """
        return (((self.buffer[ICMP_INFORMATION_SEQUENCE_NUMBER_OFFSET] << 8) & 0xFFFF) | 
            (self.buffer[ICMP_INFORMATION_SEQUENCE_NUMBER_OFFSET + 1] & 0xFF));
    

