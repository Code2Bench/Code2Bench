package p232;

import java.util.regex.Pattern;

public class Tested {
    /**
     * Removes the file extension from the given file name. If the file name does not contain an
     * extension (i.e., no '.' character is present), the original file name is returned.
     *
     * <p>This method searches for the last occurrence of the '.' character in the file name and
     * returns the substring from the beginning of the file name up to, but not including, the '.'.
     * If no '.' is found, the entire file name is returned unchanged.
     *
     * @param fileName the file name from which to remove the extension. Must not be null.
     * @return the file name without its extension, or the original file name if no extension exists.
     * @throws NullPointerException if {@code fileName} is null.
     */
    public static String removeExtension(final String fileName) {
        if (fileName == null) {
            throw new NullPointerException("fileName cannot be null");
        }

        int lastDotIndex = fileName.lastIndexOf('.');
        if (lastDotIndex == -1) {
            return fileName;
        } else {
            return fileName.substring(0, lastDotIndex);
        }
    }
}