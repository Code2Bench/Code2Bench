package p242;

public class Tested {
    /**
     * Formats the given download speed in bytes per second into a human-readable string.
     * The method converts the speed into the most appropriate unit (B/s, KB/s, or MB/s)
     * based on the magnitude of the input value:
     * <ul>
     *   <li>If the speed is less than 1024 bytes per second, it is formatted as "B/s".</li>
     *   <li>If the speed is between 1024 and 1024 * 1024 bytes per second, it is formatted as "KB/s" with one decimal place.</li>
     *   <li>If the speed is greater than or equal to 1024 * 1024 bytes per second, it is formatted as "MB/s" with one decimal place.</li>
     * </ul>
     *
     * @param bytesPerSecond the download speed in bytes per second. Must be a non-negative value.
     * @return a formatted string representing the download speed in the most appropriate unit.
     */
    public static String formatDownloadSpeed(long bytesPerSecond) {
        // TODO: implement this method
    }
}