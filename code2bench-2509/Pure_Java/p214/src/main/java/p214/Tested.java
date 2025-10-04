package p214;

import java.util.regex.Pattern;

public class Tested {
    /**
     * Extracts the file extension from the given file name. The file extension is defined as the substring
     * after the last occurrence of the '.' character in the file name. If the file name does not contain a
     * valid extension (e.g., no '.' character, or the '.' is the first or last character), an empty string
     * is returned. The extension is converted to lowercase before being returned.
     *
     * @param fileName the file name from which to extract the extension. Must not be null.
     * @return the file extension in lowercase, or an empty string if no valid extension is found.
     */
    public static String getFileExtension(final String fileName) {
        if (fileName == null) {
            throw new IllegalArgumentException("File name cannot be null");
        }

        int lastDotIndex = fileName.lastIndexOf('.');
        if (lastDotIndex == -1 || lastDotIndex == 0 || lastDotIndex == fileName.length() - 1) {
            return "";
        }

        return fileName.substring(lastDotIndex + 1).toLowerCase();
    }
}