package p116;

import java.text.SimpleDateFormat;
import java.util.Date;

public class Tested {
    /**
     * Removes the trailing slash from the given URI if it ends with a slash and the URI length
     * is greater than the length of "file:///". If the URI does not end with a slash or its length
     * is not greater than "file:///", the original URI is returned unchanged.
     *
     * @param uri The URI from which to strip the trailing slash. Must not be null.
     * @return The URI without the trailing slash, or the original URI if no trailing slash was
     *         present or the URI length was not greater than "file:///".
     * @throws NullPointerException if the input URI is null.
     */
    public static String stripTrailingSlash(String uri) {
        // Check if the URI is null
        if (uri == null) {
            throw new NullPointerException("Input URI cannot be null");
        }

        // Check if the URI ends with a slash and its length is greater than "file:///"
        if (uri.endsWith("/") && uri.length() > "file:///".length()) {
            // Remove the trailing slash
            return uri.substring(0, uri.length() - 1);
        }

        // Return the original URI if it doesn't end with a slash or its length is not greater
        return uri;
    }
}