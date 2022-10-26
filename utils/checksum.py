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

class Checksum():
    @staticmethod
    def icmp_checksum(buffer):
        """
        Computes ICMP checksum
        """
        sum = 0;
        if len(buffer) % 2 == 0:
            buffer_len = len(buffer)
        else:
            buffer_len = len(buffer) - 1
        for i in range(0, buffer_len, 2):
            sum += (((buffer[i] << 8) & 0xFFFF) | (buffer[i + 1] & 0xFF))
        if len(buffer) % 2 != 0:
            sum += ((buffer[len(buffer) - 1] << 8) & 0xFFFF)
        sum =  (sum >> 16) + (sum & 0xffff);
        sum += (sum >> 16);
        return ~sum;

    @staticmethod
    def verify_icmp_checksum(buffer, checksum):
        """
        Verifies the checksum
        """
        computed_checksum = (Checksum.icmp_checksum(buffer) & 0XFFFF);
        return computed_checksum == checksum;