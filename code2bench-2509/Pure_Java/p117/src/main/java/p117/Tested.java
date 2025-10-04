package p117;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Tested {
    /**
     * Extracts the file extension from the given filename and returns it in lowercase.
     * If the filename does not contain a valid extension (e.g., no dot, dot at the start, or dot at the end),
     * the method defaults to returning "jpg".
     *
     * @param filename the filename from which to extract the extension. Must not be null.
     * @return the lowercase file extension, or "jpg" if no valid extension is found.
     */
    private static String getFileExtension(String filename) {
        // Regular expression to match a valid file extension
        Pattern pattern = Pattern.compile("^(.*?\\.[^\\.]*)?$");
        Matcher matcher = pattern.matcher(filename);
        
        if (matcher.find()) {
            String extension = matcher.group(1).toLowerCase();
            return extension;
        } else {
            return "jpg";
        }
    }
}