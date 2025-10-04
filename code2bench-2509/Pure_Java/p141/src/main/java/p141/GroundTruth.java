package p141;
public class GroundTruth {
    public static String removeChar(String str, char ch) {
        int pos = str.indexOf(ch);
        if (pos == -1) {
            return str;
        }
        StringBuilder sb = new StringBuilder(str.length());
        int cur = 0;
        int next = pos;
        while (true) {
            sb.append(str, cur, next);
            cur = next + 1;
            next = str.indexOf(ch, cur);
            if (next == -1) {
                sb.append(str, cur, str.length());
                break;
            }
        }
        return sb.toString();
    }
}