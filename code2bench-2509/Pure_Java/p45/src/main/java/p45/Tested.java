package p45;

import java.util.Objects;

public class Tested {
    /**
     * Extracts the file extension from the given file path. The extension is defined as the substring
     * after the last occurrence of the '.' character in the path. If the path does not contain a '.'
     * character or is null, this method returns null.
     *
     * <p>Examples:
     * <pre>{@code
     * getExtension("file.txt") returns "txt"
     * getExtension("archive.tar.gz") returns "gz"
     * getExtension("no_extension") returns null
     * getExtension(null) returns null
     * }</pre>
     *
     * @param path the file path from which to extract the extension, may be null
     * @return the file extension, or null if the path is null or does not contain a '.'
     */
    public static String getExtension(String path) {
        if (path == null) {
            return null;
        }
        
        int lastDotIndex = path.lastIndexOf('.');
        if (lastDotIndex == -1) {
            return null;
        }
        
        return path.substring(lastDotIndex + 1);
    }
}