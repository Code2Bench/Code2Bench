package p164;

import java.util.Objects;

public class Tested {
    /**
     * Extracts the file suffix from the given file name. The file suffix is defined as the substring
     * starting from the last occurrence of the '.' character to the end of the string. If the file name
     * is null or does not contain a '.', an empty string is returned.
     *
     * <p>Examples:
     * <ul>
     *   <li>{@code extractFileSuffix("example.txt")} returns {@code ".txt"}</li>
     *   <li>{@code extractFileSuffix("document")} returns {@code ""}</li>
     *   <li>{@code extractFileSuffix(null)} returns {@code ""}</li>
     * </ul>
     *
     * @param fileName the file name from which to extract the suffix, may be null
     * @return the file suffix, or an empty string if the file name is null or does not contain a '.'
     */
    public static String extractFileSuffix(String fileName) {
        if (fileName == null) {
            return "";
        }
        
        int lastDotIndex = fileName.lastIndexOf('.');
        if (lastDotIndex == -1) {
            return "";
        }
        
        return fileName.substring(lastDotIndex);
    }
}