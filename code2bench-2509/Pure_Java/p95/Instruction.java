package p95;

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
        // TODO: implement this method
    }
}