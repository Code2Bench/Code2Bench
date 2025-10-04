package p271;
public class GroundTruth {
    public static String removeCRLF(String text) {
        if (text.indexOf('\n') >= 0 || text.indexOf('\r') >= 0) {
            char[] p = text.toCharArray();
            StringBuilder sb = new StringBuilder(p.length);
            for (int k = 0; k < p.length; ++k) {
                char c = p[k];
                if (c == '\n') {
                    sb.append(' ');
                } else if (c == '\r') {
                    sb.append(' ');
                    if (k < p.length - 1 && p[k + 1] == '\n') {
                        ++k;
                    }
                } else {
                    sb.append(c);
                }
            }
            return sb.toString();
        }
        return text;
    }
}