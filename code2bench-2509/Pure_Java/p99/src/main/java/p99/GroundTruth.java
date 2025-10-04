package p99;
public class GroundTruth {
    public static String escapeFFmpegString(String text) {
        if (text == null)
            return "";
        return text
                .replace("\\", "\\\\") // Escape backslashes
                .replace(":", "\\:") // Escape colons
                .replace("'", "") // Remove single quotes entirely (safer than escaping)
                .replace("\"", "") // Remove double quotes
                .replace("%", "%%"); // Escape percent signs
    }
}