package p237;

import java.util.concurrent.TimeUnit;

public class Tested {
    /**
     * Formats a duration in milliseconds into a human-readable string representation.
     * The output format depends on the duration:
     * - If the duration is less than 0, returns "00:00".
     * - If the duration is less than 1 hour, returns the format "MM:SS".
     * - If the duration is 1 hour or more, returns the format "HH:MM:SS".
     *
     * @param durationMs The duration in milliseconds. Must be a non-negative value.
     * @return A formatted string representing the duration. Returns "00:00" if the input is negative.
     */
    public static String formatDuration(long durationMs) {
        if (durationMs < 0) {
            return "00:00";
        }

        long hours = durationMs / (60 * 60 * 1000);
        long remainingMs = durationMs % (60 * 60 * 1000);

        long minutes = remainingMs / (60 * 1000);
        long seconds = remainingMs % (60 * 1000);

        if (hours == 0 && minutes == 0) {
            return "00:00";
        } else if (minutes == 0) {
            return String.format("%d:00", seconds);
        } else {
            return String.format("%d:%d:%d", hours, minutes, seconds);
        }
    }
}