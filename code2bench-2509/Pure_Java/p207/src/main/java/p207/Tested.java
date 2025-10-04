package p207;

import java.util.regex.Pattern;

public class Tested {
    /**
     * Transforms the given file path by replacing a specific date-based subdirectory pattern
     * with a simplified path. The method searches for a subdirectory pattern matching
     * "/test/result/YYYY/MM/DD/" (where YYYY, MM, and DD are digits representing year, month,
     * and day respectively) and replaces it with "/test/result/".
     *
     * <p>If the input path is {@code null}, the method returns {@code null}.
     *
     * @param path The file path to transform. Can be {@code null}.
     * @return The transformed path with the date-based subdirectory pattern replaced, or
     *         {@code null} if the input path is {@code null}.
     */
    public static String getBlobPathStr(String path) {
        if (path == null) {
            return null;
        }
        
        // Regular expression to match the date-based subdirectory pattern
        Pattern pattern = Pattern.compile("/test/result/\\d{4}/\\d{2}/\\d{2}/");
        
        // Replace the matched pattern with the simplified path
        return pattern.matcher(path).replaceAll("/test/result/");
    }
}