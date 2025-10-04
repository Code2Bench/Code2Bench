package p242;

import java.text.DecimalFormat;
import java.text.DecimalFormatSymbols;
import java.util.Locale;

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
        if (bytesPerSecond < 0) {
            throw new IllegalArgumentException("Speed cannot be negative");
        }

        double speed = (double) bytesPerSecond / 1024.0;
        double[] units = {1, 1024.0, 1024.0 * 1024.0};
        String[] unitNames = {"B/s", "KB/s", "MB/s"};
        int unitIndex = 0;

        // Determine the appropriate unit
        if (bytesPerSecond < 1024) {
            unitIndex = 0;
        } else if (bytesPerSecond < 1024 * 1024) {
            unitIndex = 1;
        } else {
            unitIndex = 2;
        }

        DecimalFormat df = new DecimalFormat("#.##");
        DecimalFormatSymbols ds = new DecimalFormatSymbols(Locale.ENGLISH);
        df.setDecimalFormatSymbols(ds);

        return unitNames[unitIndex] + (unitIndex == 1 || unitIndex == 2 ? df.format(speed) : "");
    }
}