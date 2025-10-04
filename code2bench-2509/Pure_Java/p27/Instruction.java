package p27;

import java.util.Objects;

public class Tested {
    /**
     * Extracts a specific segment from a URL path based on the given index.
     *
     * <p>The URL is split into segments using the "/" delimiter. If the index is out of bounds
     * (i.e., the URL does not have enough segments), this method returns {@code null}.
     *
     * @param url   The URL from which to extract the segment. Must not be {@code null}.
     * @param index The zero-based index of the segment to extract. Must be non-negative.
     * @return The segment at the specified index, or {@code null} if the index is out of bounds.
     * @throws NullPointerException if {@code url} is {@code null}.
     */
    public static String getSubPath(String url, int index) {
        // TODO: implement this method
    }
}