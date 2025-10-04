package p17;

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
        // TODO: implement this method
    }
}