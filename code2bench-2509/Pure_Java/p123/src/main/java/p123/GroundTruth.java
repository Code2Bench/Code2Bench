package p123;
public class GroundTruth {
    public static String cleanFormatForNumber(String formatStr) {
        StringBuilder sb = new StringBuilder(formatStr);
        // If they requested spacers, with "_",
        // remove those as we don't do spacing
        // If they requested full-column-width
        // padding, with "*", remove those too
        for (int i = 0; i < sb.length(); i++) {
            char c = sb.charAt(i);
            if (c == '_' || c == '*') {
                if (i > 0 && sb.charAt((i - 1)) == '\\') {
                    // It's escaped, don't worry
                    continue;
                }
                if (i < sb.length() - 1) {
                    // Remove the character we're supposed
                    // to match the space of / pad to the
                    // column width with
                    sb.deleteCharAt(i + 1);
                }
                // Remove the _ too
                sb.deleteCharAt(i);
                i--;
            }
        }

        // Now, handle the other aspects like
        // quoting and scientific notation
        for (int i = 0; i < sb.length(); i++) {
            char c = sb.charAt(i);
            // remove quotes and back slashes
            if (c == '\\' || c == '"') {
                sb.deleteCharAt(i);
                i--;

                // for scientific/engineering notation
            } else if (c == '+' && i > 0 && sb.charAt(i - 1) == 'E') {
                sb.deleteCharAt(i);
                i--;
            }
        }

        return sb.toString();
    }
}