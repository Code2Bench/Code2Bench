package p95;

import java.text.SimpleDateFormat;
import java.util.Date;

public class Tested {
    /**
     * Formats a given duration in milliseconds into a human-readable string representation.
     * The format includes days, hours, minutes, seconds, and milliseconds. If the duration
     * is less than a day, the days component is omitted.
     *
     * The format is as follows:
     * - If the duration is greater than or equal to one day: "d,hh:mm:ss.SSS"
     * - If the duration is less than one day: "hh:mm:ss.SSS"
     * 
     * @param timeMillis the duration in milliseconds to format. Must be a non-negative value.
     * @return a formatted string representing the duration. The format depends on the duration's length.
     * @throws IllegalArgumentException if {@code timeMillis} is negative.
     */
    public static String formatDateTime(long timeMillis) {
        if (timeMillis < 0) {
            throw new IllegalArgumentException("Time millis cannot be negative");
        }

        long seconds = timeMillis / 1000;
        long remainingMillis = timeMillis % 1000;

        long days = seconds / (24 * 60 * 60);
        long hours = (seconds / (60 * 60)) % 24;
        long minutes = (seconds / 60) % 60;
        long secondsRemaining = seconds % 60;
        long milliseconds = remainingMillis;

        StringBuilder sb = new StringBuilder();
        
        if (days > 0) {
            sb.append(days).append(",");
        }
        
        sb.append(String.format("%02d:%02d:%02d.%03d", hours, minutes, secondsRemaining, milliseconds));

        return sb.toString();
    }
}