package p251;
public class GroundTruth {
    public static String escapeForLua(String text) {
        if (text == null) return "";
    
        // For Frame display, remove newlines entirely since they cause syntax errors
        // Frame doesn't support multi-line text display anyway
        return text
            .replace("\\", "\\\\")
            .replace("'", "\\'")
            .replace("\"", "\\\"")
            .replace("\n", " ")  // Replace newlines with spaces
            .replace("\r", " ")  // Replace carriage returns with spaces
            .replace("\t", " ");  // Replace tabs with spaces
    }
}