package p46;

import java.util.Objects;

public class Tested {
    /**
     * Splits a given path string into its constituent elements, removing the leading slash if present.
     * If the input path is null, an empty array is returned. The path is split by the '/' character,
     * and any leading slash is ignored.
     *
     * @param path the path string to be split, may be null
     * @return an array of path elements; an empty array if the input path is null or empty
     */
    public static String[] getPathElements(String path) {
        if (path == null || path.isEmpty()) {
            return new String[0];
        }

        String[] elements = path.split("/");
        if (elements.length == 1 && elements[0].equals("")) {
            return new String[0];
        }

        return elements;
    }
}