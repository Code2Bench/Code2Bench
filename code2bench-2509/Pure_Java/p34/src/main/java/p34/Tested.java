package p34;

/**
 * Extracts the repository ID from a combined storage and repository ID string.
 * The input string is expected to be in the format "storageId:repositoryId", where the
 * storage ID and repository ID are separated by a colon. If the input string does not
 * contain a colon, the entire string is treated as the repository ID.
 *
 * @param storageAndRepositoryId The combined storage and repository ID string. Must not be null.
 * @return The extracted repository ID. If the input string does not contain a colon,
 *         the entire string is returned as the repository ID.
 * @throws NullPointerException if {@code storageAndRepositoryId} is null.
 * @implNote This method is not yet implemented.
 */
public static String getRepositoryId(String storageAndRepositoryId) {
    int colonIndex = storageAndRepositoryId.indexOf(':');
    if (colonIndex != -1) {
        return storageAndRepositoryId.substring(colonIndex + 1);
    } else {
        return storageAndRepositoryId;
    }
}