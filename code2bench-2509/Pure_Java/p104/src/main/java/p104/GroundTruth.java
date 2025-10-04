package p104;
public class GroundTruth {
    public static int consumeUnquoted(
            String string, char delimiter, int cursor, StringBuilder builder) {
        int i;
        for (i = cursor; i < string.length(); i++) {
            char c = string.charAt(i);
            if (c == delimiter) {
                return i;
            }

            builder.append(c);
        }

        return i;
    }
}