package p23;

import java.util.regex.Pattern;

/**
 * Determines whether the given IP address falls within the specified CIDR range.
 *
 * <p>This method is intended to convert both the IP address and the CIDR block into their integer
 * representations, apply the CIDR mask, and check if the resulting values match.
 * The IP address and CIDR block must be in the standard IPv4 format (e.g., "192.168.1.1").
 * Note: This method is not yet implemented.
 *
 * @param ip The IP address to check, in the format "A.B.C.D". Must not be null or empty.
 * @param cidr The CIDR block to check against, in the format "A.B.C.D/N". Must not be null or empty.
 * @return {@code true} if the IP address is within the CIDR range; {@code false} otherwise.
 * @throws NullPointerException if either {@code ip} or {@code cidr} is null.
 */
public static boolean isInRange(String ip, String cidr) {
    // Validate input
    if (ip == null || ip.isEmpty() || cidr == null || cidr.isEmpty()) {
        throw new NullPointerException("IP and CIDR cannot be null or empty");
    }

    // Parse CIDR
    String[] parts = cidr.split("/");
    if (parts.length != 2) {
        throw new IllegalArgumentException("CIDR format is invalid");
    }
    String ipAddress = parts[0];
    int prefix = Integer.parseInt(parts[1]);

    // Convert IP to integer
    int ipInt = convertToInteger(ipAddress);

    // Calculate network address
    int networkAddress = ipInt & ((1 << (32 - prefix)) - 1);

    // Check if IP is within the CIDR range
    return (ipInt & ((1 << (32 - prefix)) - 1)) == networkAddress;
}

private static int convertToInteger(String ipAddress) {
    String[] parts = ipAddress.split("\\.");
    if (parts.length != 4) {
        throw new IllegalArgumentException("Invalid IP address format");
    }
    int a = Integer.parseInt(parts[0]);
    int b = Integer.parseInt(parts[1]);
    int c = Integer.parseInt(parts[2]);
    int d = Integer.parseInt(parts[3]);
    return (a << 24) | (b << 16) | (c << 8) | d;
}