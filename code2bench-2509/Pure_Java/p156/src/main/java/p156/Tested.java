package p156;

import java.util.Arrays;

public class Tested {
    /**
     * Parses a version string into its constituent parts. The method handles version strings
     * that start with "1." by removing the "1." prefix. It then replaces underscores ("_") and
     * the letter "u" with periods (".") and splits the string into an array of version components
     * based on the periods.
     *
     * <p>For example, the version string "1.8.0_u231" will be parsed into ["8", "0", "231"].
     *
     * @param version The version string to parse. Must not be null.
     * @return An array of strings representing the parsed version components. If the input
     *         version string is empty or only contains "1.", the returned array will be empty.
     * @throws NullPointerException if the input version string is null.
     */
    public static String[] parseVersion(String version) {
        if (version == null) {
            throw new NullPointerException("Version string cannot be null");
        }

        if (version.startsWith("1.")) {
            version = version.substring(2);
        }

        // Replace underscores and 'u' with periods
        version = version.replace('_', '.').replace('u', '.');
        
        // Split by periods and return as array
        return version.split("\\.");
    }
}