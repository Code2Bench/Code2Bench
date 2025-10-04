package p165;
public class GroundTruth {
    public static String escapeString(String str) {
        if (str == null) {
            return "";
        }
        return str.replace("\"", "\\\"").replace("\n", "\\n").replace("\r", "\\r");
    }
}