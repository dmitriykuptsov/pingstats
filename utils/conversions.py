class Converter():
    @staticmethod
    def ipv4_bytes_to_string(address_bytes):
        """
        Converts IPv4 bytes to string
        """
        if len(address_bytes) != 0x4:
            return "";
        return str(address_bytes[0]) + "." + \
            str(address_bytes[1]) + "." + \
            str(address_bytes[2]) + "." + \
            str(address_bytes[3]);
    
    @staticmethod
    def ipv_str_to_bytes(ipv4_str):
        """
        Converts IPv4 string to byte array
        """
        parts = ipv4_str.split(".");
        buffer = [0]*4;
        buffer[0] = int(parts[0])
        buffer[1] = int(parts[1])
        buffer[2] = int(parts[2])
        buffer[3] = int(parts[3])
        return buffer;

    @staticmethod
    def ipv4_to_int(address):
        """
        Converts IPv4 address to integer
        """
        try:
            parts = address.split(".");
            address_as_int = 0;
            address_as_int |= (int(parts[0]) << 24);
            address_as_int |= (int(parts[1]) << 16);
            address_as_int |= (int(parts[2]) << 8);
            address_as_int |= (int(parts[3]));
            return address_as_int
        except:
            return 0;