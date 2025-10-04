package p176;
public class GroundTruth {
    public static String unquote(String value) {
        if (value != null && value.length() > 1 && value.startsWith("'") && value.endsWith("'")) {
            return value.substring(1, value.length() - 1).replace("''", "'");
        }
        return value;
    }
}