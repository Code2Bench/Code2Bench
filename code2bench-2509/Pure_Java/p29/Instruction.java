package p29;

public class Tested {
    /**
     * Converts a given number of bytes into a human-readable string representation.
     * The method uses the International System of Units (SI) standard, where 1000 bytes
     * equal 1 kilobyte (KB), 1000 KB equal 1 megabyte (MB), and so on.
     *
     * The method handles the following cases:
     * - If the number of bytes is less than 1000, it returns the size in bytes (e.g., "500 B").
     * - If the number of bytes is 1000 or greater, it converts the size to the appropriate unit
     *   (e.g., KB, MB, GB) and formats the result to one decimal place (e.g., "1.5 MB").
     *
     * The supported units are: B (bytes), KB (kilobytes), MB (megabytes), GB (gigabytes),
     * TB (terabytes), PB (petabytes), and EB (exabytes).
     *
     * @param bytes The number of bytes to convert. Must be a non-negative value.
     * @return A human-readable string representation of the size, formatted to one decimal place
     *         and appended with the appropriate unit.
     */
    public static String getHumanReadableSize(long bytes) {
        // TODO: implement this method
    }
}