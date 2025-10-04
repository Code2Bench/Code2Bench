package p99;

import java.util.Objects;

public class Tested {
    /**
     * Escapes special characters in a given string to make it safe for use in FFmpeg commands.
     * The method performs the following transformations:
     * <ul>
     *   <li>Escapes backslashes by replacing each backslash with two backslashes.</li>
     *   <li>Escapes colons by replacing each colon with a backslash followed by a colon.</li>
     *   <li>Removes single quotes entirely for safety reasons.</li>
     *   <li>Removes double quotes entirely for safety reasons.</li>
     *   <li>Escapes percent signs by replacing each percent sign with two percent signs.</li>
     * </ul>
     * If the input string is {@code null}, an empty string is returned.
     *
     * @param text The string to be escaped. Can be {@code null}.
     * @return The escaped string, or an empty string if the input is {@code null}.
     */
    public static String escapeFFmpegString(String text) {
        // TODO: implement this method
    }
}