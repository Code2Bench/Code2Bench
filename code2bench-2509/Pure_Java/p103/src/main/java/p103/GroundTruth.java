package p103;
public class GroundTruth {
    public static int consumeInQuotes(
            String string, char quote, int cursor, StringBuilder builder) {
        for (int i = cursor + 1; i < string.length(); i++) {
            char c = string.charAt(i);
            if (c == quote) {
                if (i + 1 < string.length() && string.charAt(i + 1) == quote) {
                    builder.append(c);
                    i += 1;
                } else {
                    return i + 1;
                }
            } else {
                builder.append(c);
            }
        }

        throw new IllegalArgumentException(
                "Could not split string. Quoting was not closed properly.");
    }
}