package p82;

import java.util.StringTokenizer;

public class Tested {
    /**
     * Extracts the base URL from the given URL by removing any query parameters or fragments.
     * The base URL is defined as the portion of the URL before the first occurrence of '?' (query) or '#' (fragment).
     * If neither '?' nor '#' is present, the entire URL is returned as the base URL.
     *
     * @param url The URL from which to extract the base URL. Must not be null.
     * @return The base URL, which is the portion of the URL before the first '?' or '#', or the entire URL if neither is present.
     * @throws NullPointerException if the input URL is null.
     */
    private static String getBaseUrlSafely(String url) {
        if (url == null) {
            throw new NullPointerException("Input URL cannot be null");
        }

        int index = url.indexOf('?');
        if (index == -1) {
            return url;
        }

        return url.substring(0, index);
    }
}