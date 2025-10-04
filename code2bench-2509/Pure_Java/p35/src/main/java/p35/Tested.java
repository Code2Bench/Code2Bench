public class Tested {
    /**
     * Extracts the file extension from the given file path. The extension is defined as the substring
     * after the last occurrence of the '.' character in the path. If the path does not contain a '.',
     * or if the path is null, this method returns null.
     *
     * <p>Examples:
     * <pre>{@code
     * getExtension("file.txt")    → "txt"
     * getExtension("archive.tar.gz") → "gz"
     * getExtension("no_extension")  → null
     * getExtension(null)            → null
     * }</pre>
     *
     * @param path the file path from which to extract the extension; may be null
     * @return the file extension as a String, or null if no extension is found or if the path is null
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