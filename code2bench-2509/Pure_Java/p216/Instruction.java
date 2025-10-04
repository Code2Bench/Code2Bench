package p216;

import java.util.Objects;

public class Tested {
    /**
     * Normalizes a cron trigger string to ensure it has exactly six parts. If the input cron trigger
     * has fewer than six parts, a "0" is prepended to the string to make it six parts. If the input
     * already has six or more parts, it is returned unchanged.
     *
     * <p>For example:
     * <ul>
     *   <li>Input: "1 2 3 4 5" → Output: "0 1 2 3 4 5"</li>
     *   <li>Input: "1 2 3 4 5 6" → Output: "1 2 3 4 5 6"</li>
     * </ul>
     *
     * @param cronTrigger the cron trigger string to normalize, must not be null
     * @return the normalized cron trigger string with exactly six parts
     * @throws NullPointerException if {@code cronTrigger} is null
     */
    public static String normalizeToSixParts(final String cronTrigger) {
        // TODO: implement this method
    }
}