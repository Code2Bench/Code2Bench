package p239;

public class Tested {
    /**
     * Formats a file size in bytes into a human-readable string with appropriate units (B, KB, MB, GB).
     * The method scales the size based on the following thresholds:
     * - Less than 1024 bytes: displays in bytes (B).
     * - Between 1024 and 1,048,575 bytes: displays in kilobytes (KB) with one decimal place.
     * - Between 1,048,576 and 1,073,741,823 bytes: displays in megabytes (MB) with one decimal place.
     * - 1,073,741,824 bytes or more: displays in gigabytes (GB) with one decimal place.
     *
     * @param bytes the file size in bytes, must be non-negative.
     * @return a formatted string representing the file size with the appropriate unit.
     * @throws IllegalArgumentException if {@code bytes} is negative.
     */
    public static String formatFileSize(long bytes) {
        // TODO: implement this method
    }
}