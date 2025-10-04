package p154;

import java.util.Objects;

public class Tested {
    /**
     * Generates the next version number based on the current version and the specified version type.
     *
     * <p>If {@code minorVersion} is {@code true}, the minor version number is incremented by 1, and the major version
     * remains unchanged. If {@code minorVersion} is {@code false}, the major version number is incremented by 1, and
     * the minor version is reset to 0.
     *
     * <p>The version string is expected to be in the format "major.minor" (e.g., "1.2"). If the input string does not
     * conform to this format or is {@code null}, the behavior is undefined.
     *
     * @param currentVersion the current version string in "major.minor" format; must not be {@code null}
     * @param minorVersion   if {@code true}, increments the minor version; if {@code false}, increments the major version
     * @return the next version string in "major.minor" format
     * @throws NullPointerException if {@code currentVersion} is {@code null}
     * @throws NumberFormatException if the version components cannot be parsed as integers
     */
    public static String getNextVersion(String currentVersion, boolean minorVersion) {
        // TODO: implement this method
    }
}