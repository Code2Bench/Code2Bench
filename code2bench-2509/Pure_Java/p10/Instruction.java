package p10;

public class Tested {
    /**
     * Parses the given server URL to ensure it has a valid protocol prefix. If the URL already starts
     * with "http://" or "https://", it is returned as-is. Otherwise, the method assumes the input is in
     * the "host:port" format and prepends "http://" to it.
     *
     * @param serverUrl the server URL to parse. Must not be null or empty.
     * @return the parsed server URL with a valid protocol prefix. If the input already has a protocol,
     *         it is returned unchanged; otherwise, "http://" is prepended.
     * @throws IllegalArgumentException if {@code serverUrl} is null or empty.
     */
    private static String parseServerUrl(String serverUrl) {
        // TODO: implement this method
    }
}