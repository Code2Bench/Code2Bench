public class Tested {
    /**
     * Escapes special characters in the given text to make it safe for use in Lua strings.
     * Specifically, this method:
     * <ul>
     *   <li>Replaces backslashes (`\`) with double backslashes (`\\`).</li>
     *   <li>Escapes single quotes (`'`) with a backslash (`\'`).</li>
     *   <li>Escapes double quotes (`"`) with a backslash (`\"`).</li>
     *   <li>Replaces newlines (`\n`), carriage returns (`\r`), and tabs (`\t`) with spaces (` `).</li>
     * </ul>
     * If the input text is {@code null}, an empty string is returned.
     *
     * @param text the text to escape, may be {@code null}.
     * @return the escaped text, or an empty string if the input is {@code null}.
     */
    public static String escapeForLua(String text) {
        if (text == null) {
            return "";
        }

        StringBuilder escaped = new StringBuilder();
        for (int i = 0; i < text.length(); i++) {
            char c = text.charAt(i);
            switch (c) {
                case '\\':
                    escaped.append("\\\\");
                    break;
                case '\'':
                    escaped.append("\\'");
                    break;
                case '"':
                    escaped.append("\\\"");
                    break;
                case '\n':
                    escaped.append(" ");
                    break;
                case '\r':
                    escaped.append(" ");
                    break;
                case '\t':
                    escaped.append(" ");
                    break;
                default:
                    escaped.append(c);
                    break;
            }
        }
        return escaped.toString();
    }
}