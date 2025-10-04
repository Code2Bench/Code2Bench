package p81;
public class GroundTruth {
    public static String createSimpleTypePattern(String type) {
        String pattern = type.trim()
                .replace(".", "\\.")
                .replace("$", "\\$")
                .replace("[", "\\[")
                .replace("]", "\\]");

        // Allow both simple and fully qualified names
        if (!type.contains(".") && !type.equals("*")) {
            // For simple names like "List", "Map", etc.
            // Allow matching against both simple and fully qualified names
            pattern = "((.*\\.)?" + pattern + ")";
        } else if (type.contains(".")) {
            // For fully qualified names like java.util.List
            // Also match against simple names
            String simpleName = type.substring(type.lastIndexOf('.') + 1);
            pattern = "(" + pattern + "|" + simpleName + ")";
        }

        return pattern;
    }
}