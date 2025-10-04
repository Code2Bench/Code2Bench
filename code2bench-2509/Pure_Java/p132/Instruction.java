package p132;

public class Tested {
    /**
     * Removes the file extension from the given file name. If the file name does not contain a file
     * extension (i.e., no '.' character is present), the original file name is returned unchanged.
     *
     * <p>This method searches for the last occurrence of the '.' character in the file name and
     * returns the substring from the beginning of the file name up to, but not including, that
     * character. If no '.' character is found, the entire file name is returned.
     *
     * @param fileName the file name from which to remove the extension. Must not be null.
     * @return the file name without its extension, or the original file name if no extension is found.
     * @throws NullPointerException if {@code fileName} is null.
     */
    public static String removeFileExtension(String fileName) {
        // TODO: implement this method
    }
}