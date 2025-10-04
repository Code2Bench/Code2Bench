package p217;

import java.util.Objects;

public class Tested {
    /**
     * Normalizes the given entity ID by converting it to lowercase and replacing any characters
     * that are not alphanumeric, underscores, '@', '.', or '-' with underscores. Additionally,
     * if the normalized ID exceeds 256 characters, it is truncated to the first 256 characters.
     *
     * @param entityId The entity ID to normalize. Must not be null.
     * @return The normalized entity ID, guaranteed to be no longer than 256 characters.
     * @throws NullPointerException if {@code entityId} is null.
     */
    public static String normalizeID(final String entityId) {
        // TODO: implement this method
    }
}