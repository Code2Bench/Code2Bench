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
        if (entityId == null) {
            throw new NullPointerException("entityId cannot be null");
        }

        StringBuilder normalized = new StringBuilder();
        for (char c : entityId.toCharArray()) {
            if (Character.isLetterOrDigit(c) || c == '_' || c == '@' || c == '.' || c == '-') {
                normalized.append(c);
            } else {
                normalized.append('_');
            }
        }

        String result = normalized.toString().toLowerCase();
        if (result.length() > 256) {
            result = result.substring(0, 256);
        }

        return result;
    }
}