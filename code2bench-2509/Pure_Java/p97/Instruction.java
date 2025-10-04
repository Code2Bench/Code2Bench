package p97;

import java.util.Objects;

public class Tested {
    /**
     * Extracts the status code from the provided debug information string. The method searches for a line
     * containing the substring "Status Code:" and attempts to parse the integer value following it.
     *
     * <p>If the debug information is null or empty, or if no valid status code is found, the method returns null.
     * If the status code is found but cannot be parsed as an integer, the method also returns null.
     *
     * @param debugInfo The debug information string from which to extract the status code. Can be null or empty.
     * @return The extracted status code as an Integer, or null if no valid status code is found or cannot be parsed.
     */
    public static Integer extractStatusCodeFromDebugInfo(String debugInfo) {
        // TODO: implement this method
    }
}