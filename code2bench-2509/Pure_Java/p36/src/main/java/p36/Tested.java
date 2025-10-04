package p36;

import java.util.Objects;

public class Tested {
    /**
     * Splits a given path string into its constituent elements, removing the leading slash if present.
     * If the input path is {@code null}, an empty array is returned.
     *
     * <p>The method first checks if the path starts with a leading slash ("/"). If it does, the slash
     * is removed before splitting the path into elements using the slash as the delimiter.
     *
     * @param path the path string to be split, may be {@code null}
     * @return an array of path elements; an empty array if the input path is {@code null}
     */
    public static String[] getPathElements(String path) {
        if (path == null) {
            return new String[0];
        }

        // Remove leading slash if present
        if (path.startsWith("/")) {
            path = path.substring(1);
        }

        // Split the path by '/' and return the result
        return path.split("/");
    }
}