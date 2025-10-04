public class Tested {
    /**
     * Extracts the URL from the provided debug information string. The method searches for a line
     * containing the substring "Full URL:" and returns the URL that follows it. If no such line
     * is found, the method returns {@code null}.
     *
     * <p>The method splits the input string into lines using the newline character ('\n') and
     * iterates through each line to find the one containing "Full URL:". Once found, it extracts
     * the URL by taking the substring starting from the character immediately after "Full URL:"
     * and trims any leading or trailing whitespace.
     *
     * @param debugInfo the debug information string from which to extract the URL. Must not be
     *                  {@code null}, but may be empty.
     * @return the extracted URL as a {@code String}, or {@code null} if no URL is found.
     * @throws NullPointerException if {@code debugInfo} is {@code null}.
     */
    public static String extractUrlFromDebugInfo(String debugInfo) {
        if (debugInfo == null) {
            throw new NullPointerException("debugInfo cannot be null");
        }

        String[] lines = debugInfo.split("\n");
        for (String line : lines) {
            if (line.contains("Full URL:")) {
                String urlLine = line.trim();
                int startIndex = urlLine.indexOf("Full URL:") + "Full URL:".length();
                return urlLine.substring(startIndex).trim();
            }
        }
        return null;
    }
}