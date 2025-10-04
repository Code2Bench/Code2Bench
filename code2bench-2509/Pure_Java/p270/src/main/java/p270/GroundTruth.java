package p270;
public class GroundTruth {
    public static String escape(String content) {
        StringBuilder buf = new StringBuilder();
        for (int i = 0; i < content.length(); i++) {
            switch (content.charAt(i)) {
                case '<':
                    buf.append("&lt;");
                    break;
                case '>':
                    buf.append("&gt;");
                    break;
                case '\'':
                    buf.append("&apos;");
                    break;
                case '\"':
                    buf.append("&quot;");
                    break;
                case '&':
                    buf.append("&amp;");
                    break;
                default:
                    buf.append(content.charAt(i));
            }
        }
        return buf.toString();
    }
}