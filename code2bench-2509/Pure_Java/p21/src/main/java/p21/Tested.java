package p21;

import java.util.Arrays;

public class Tested {
    /**
     * Rewrites a given path by replacing the storage and repository identifiers with the provided values.
     * The path is expected to be in the format "prefix/storage/repository/...". If the path does not
     * contain at least 5 segments (i.e., it has 4 or fewer segments after splitting by '/'), the original
     * path is returned unchanged. Otherwise, the third and fourth segments of the path are replaced
     * with the provided {@code storageId} and {@code repositoryId}, respectively.
     *
     * @param path The path to be rewritten, which should be a non-null string containing at least one '/'.
     * @param storageId The new storage identifier to replace the existing one in the path. Must not be null.
     * @param repositoryId The new repository identifier to replace the existing one in the path. Must not be null.
     * @return The rewritten path if the original path contains at least 5 segments; otherwise, the original path.
     * @throws NullPointerException if any of the parameters are null.
     */
    public static String rewriteByStoreAndRepo(String path, String storageId, String repositoryId) {
        if (path == null || storageId == null || repositoryId == null) {
            throw new NullPointerException("All parameters must not be null");
        }

        String[] segments = path.split("/");
        if (segments.length < 5) {
            return path;
        }

        // Replace third and fourth segments
        String newPath = Arrays.toString(segments)
                .replaceFirst("(.*?)(\\/\\w+\\/\\w+\\/\\w+)", "$1" + storageId + "/\" + repositoryId);
        return newPath;
    }
}