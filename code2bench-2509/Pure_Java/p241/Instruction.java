package p241;

public class Tested {
    /**
     * Formats a given file size in bytes into a human-readable string representation.
     * The method converts the size into the most appropriate unit (B, KB, MB, or GB)
     * based on the magnitude of the input value. The output is formatted to one decimal
     * place for sizes larger than 1024 bytes.
     *
     * <p>The conversion logic is as follows:
     * <ul>
     *   <li>If the size is less than 1024 bytes, it is returned as "B" (bytes).</li>
     *   <li>If the size is between 1024 bytes and 1 MB, it is converted to "KB" (kilobytes).</li>
     *   <li>If the size is between 1 MB and 1 GB, it is converted to "MB" (megabytes).</li>
     *   <li>If the size is 1 GB or larger, it is converted to "GB" (gigabytes).</li>
     * </ul>
     *
     * @param bytes the file size in bytes, must be a non-negative value
     * @return a formatted string representing the file size in the most appropriate unit
     * @throws IllegalArgumentException if the input value is negative
     */
    public static String formatFileSize(long bytes) {
        // TODO: implement this method
    }
}