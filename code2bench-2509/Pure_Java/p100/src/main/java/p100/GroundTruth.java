package p100;
public class GroundTruth {
    public static String replaceInvalidChars(String str) {
        char[] chars = null;
        final int strLen = str.length();
        int pos = 0;

        for (int i = 0; i < strLen; i++) {
            final char c = str.charAt(i);
            switch (c) {
                case '>':
                case '<':
                case '"':
                    // remove character by not moving cursor
                    if (chars == null) {
                        chars = str.toCharArray();
                    }
                    break;

                case ' ':
                    if (chars == null) {
                        chars = str.toCharArray();
                    }
                    chars[pos++] = '_';
                    break;

                case ',':
                case '=':
                case ';':
                case ':':
                case '?':
                case '\'':
                case '*':
                    if (chars == null) {
                        chars = str.toCharArray();
                    }
                    chars[pos++] = '-';
                    break;

                default:
                    if (chars != null) {
                        chars[pos] = c;
                    }
                    pos++;
            }
        }

        return chars == null ? str : new String(chars, 0, pos);
    }
}