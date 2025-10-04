package p234;
public class GroundTruth {
    public static String y2yyyy(String str) {
        char[] carr = str.toCharArray();
        StringBuilder sb = new StringBuilder();
        boolean inside = false;
        char c;
        for (int i = 0; i < carr.length; i++) {
            c = carr[i];
            if (c == '\'') inside = !inside;
            else if (!inside && c == 'y') {
                if ((i == 0 || carr[i - 1] != 'y') && (i == (carr.length - 1) || carr[i + 1] != 'y')) {
                    sb.append("yyyy");
                    continue;
                }
            }
            sb.append(c);
        }
        return sb.toString();
    }
}