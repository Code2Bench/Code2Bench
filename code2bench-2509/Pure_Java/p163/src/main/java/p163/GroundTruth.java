package p163;
public class GroundTruth {
    public static String escape(String value) {
        StringBuilder builder = new StringBuilder();
        builder.append("\"");
        for (char c : value.toCharArray()) {
            if (c == '\'') builder.append("\\'");
            else if (c == '\"') builder.append("\\\"");
            else if (c == '\r') builder.append("\\r");
            else if (c == '\n') builder.append("\\n");
            else if (c == '\t') builder.append("\\t");
            else if (c < 32 || c >= 127) builder.append(String.format("\\u%04x", (int) c));
            else builder.append(c);
        }
        builder.append("\"");
        return builder.toString();
    }
}