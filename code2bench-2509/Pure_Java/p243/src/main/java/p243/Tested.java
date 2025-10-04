package p243;

public class Tested {
    /**
     * Calculates the download progress as a percentage based on the number of bytes downloaded
     * and the total number of bytes to be downloaded. The progress is capped at 100% to ensure
     * it does not exceed the maximum value.
     *
     * <p>If the total number of bytes is less than or equal to 0, the progress is returned as 0.
     *
     * @param bytesDownloaded The number of bytes downloaded so far. Must be non-negative.
     * @param totalBytes The total number of bytes to be downloaded. Must be non-negative.
     * @return The progress as a percentage (0 to 100). Returns 0 if {@code totalBytes} is less than
     *         or equal to 0.
     */
    public static int calculateProgress(long bytesDownloaded, long totalBytes) {
        if (totalBytes <= 0) {
            return 0;
        }
        
        int progress = (int) ((bytesDownloaded * 100) / totalBytes);
        return Math.min(progress, 100);
    }
}