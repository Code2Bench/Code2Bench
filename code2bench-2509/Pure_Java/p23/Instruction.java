package p23;

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
    // TODO: implement this method
}