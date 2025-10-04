package p140;
public class GroundTruth {
    public static String escape(String str) {
        int len = str.length();
        StringBuilder sb = new StringBuilder(len);
        for (int i = 0; i < len; i++) {
            char c = str.charAt(i);
            switch (c) {
                case '.':
                case '/':
                case ';':
                case '$':
                case ' ':
                case ',':
                case '<':
                    sb.append('_');
                    break;

                case '[':
                    sb.append('A');
                    break;

                case ']':
                case '>':
                case '?':
                case '*':
                    break;

                default:
                    sb.append(c);
                    break;
            }
        }
        return sb.toString();
    }
}