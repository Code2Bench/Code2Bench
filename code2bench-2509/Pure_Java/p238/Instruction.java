package p238;

public class Tested {
    /**
     * Formats the given bitrate in bits per second (bps) into a human-readable string.
     * The bitrate is formatted as follows:
     * - If the bitrate is less than 1000, it is formatted as "{bitrate} bps".
     * - If the bitrate is between 1000 and 999999, it is formatted as "{bitrate / 1000.0} kbps" with one decimal place.
     * - If the bitrate is 1000000 or greater, it is formatted as "{bitrate / 1000000.0} Mbps" with one decimal place.
     *
     * @param bitrateBits the bitrate in bits per second (bps) to format. Must be a non-negative integer.
     * @return a formatted string representing the bitrate in the appropriate unit (bps, kbps, or Mbps).
     */
    public static String formatBitrate(int bitrateBits) {
        // TODO: implement this method
    }
}