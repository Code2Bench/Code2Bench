package p10;

import java.util.Objects;

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
        if (serverUrl == null || serverUrl.isEmpty()) {
            throw new IllegalArgumentException("Server URL cannot be null or empty");
        }

        if (serverUrl.startsWith("http://") || serverUrl.startsWith("https://")) {
            return serverUrl;
        }

        // Assume the format is "host:port"
        String[] parts = serverUrl.split(":");
        if (parts.length != 2) {
            throw new IllegalArgumentException("Invalid server URL format");
        }

        return "http://" + parts[0] + ":" + parts[1];
    }
}