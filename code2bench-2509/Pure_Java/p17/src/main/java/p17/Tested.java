package p17;

import java.text.SimpleDateFormat;
import java.util.Date;

public class Tested {
    /**
     * Formats a duration in seconds into a human-readable string. The format depends on the total duration:
     * <ul>
     *   <li>If the duration is less than one hour, the format is "MM:SS".</li>
     *   <li>If the duration is one hour or more, the format is "HH:MM:SS".</li>
     * </ul>
     * The minutes and seconds are always displayed as two digits, padding with leading zeros if necessary.
     *
     * @param seconds the duration in seconds to format. Must be a non-negative integer.
     * @return a formatted string representing the duration. The format is either "MM:SS" or "HH:MM:SS".
     * @throws IllegalArgumentException if {@code seconds} is negative.
     */
    public static String formatDuration(int seconds) {
        if (seconds < 0) {
            throw new IllegalArgumentException("Seconds must be a non-negative integer");
        }

        long hours = seconds / 3600;
        long remainingSeconds = seconds % 3600;

        String format = (hours > 0) ? "HH:MM:SS" : "MM:SS";

        StringBuilder sb = new StringBuilder();
        sb.append(format);

        if (format.equals("HH:MM:SS")) {
            sb.append(String.format("%02d:%02d:%02d", hours, remainingSeconds / 60, remainingSeconds % 60));
        } else {
            sb.append(String.format("%02d:%02d", remainingSeconds / 60, remainingSeconds % 60));
        }

        return sb.toString();
    }
}