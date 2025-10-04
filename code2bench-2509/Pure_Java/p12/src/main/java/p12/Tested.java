package p12;

import java.text.DecimalFormat;
import java.text.DecimalFormatSymbols;
import java.util.Locale;

public class Tested {
    /**
     * Formats a duration in milliseconds into a human-readable string representation.
     * The method converts the duration into the most appropriate unit (milliseconds, seconds, minutes, or hours)
     * based on the magnitude of the input value. The output is formatted as follows:
     * <ul>
     *   <li>If the duration is less than 1000 milliseconds, it is displayed in milliseconds (e.g., "500 ms").</li>
     *   <li>If the duration is between 1000 milliseconds and 59999 milliseconds, it is displayed in seconds with two decimal places (e.g., "1.23 s").</li>
     *   <li>If the duration is between 60000 milliseconds and 3599999 milliseconds, it is displayed in minutes with two decimal places (e.g., "2.50 min").</li>
     *   <li>If the duration is 3600000 milliseconds or greater, it is displayed in hours with two decimal places (e.g., "1.75 h").</li>
     * </ul>
     *
     * @param milliseconds the duration in milliseconds to format; must be a non-negative value.
     * @return a formatted string representing the duration in the most appropriate unit.
     * @throws IllegalArgumentException if the input value is negative.
     */
    public static String formatDuration(long milliseconds) {
        if (milliseconds < 0) {
            throw new IllegalArgumentException("Duration cannot be negative");
        }

        long seconds = milliseconds / 1000;
        long remaining = milliseconds % 1000;

        if (remaining < 1000) {
            return String.format("%d ms", milliseconds);
        } else if (seconds < 60) {
            return String.format("%.2f s", (double) seconds / 1000);
        } else if (seconds < 3600) {
            return String.format("%.2f min", (double) seconds / 60);
        } else {
            return String.format("%.2f h", (double) seconds / 3600);
        }
    }
}