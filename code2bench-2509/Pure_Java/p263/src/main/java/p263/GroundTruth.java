package p263;
public class GroundTruth {
    public static String safe(String src) {
        StringBuffer sb = new StringBuffer();
        for (int i = 0; i < src.length(); i++) {
            char c = src.charAt(i);
            if (c >= 32 && c < 128) {
                sb.append(c);
            } else {
                sb.append("<" + (int) c + ">");
            }
        }
        return sb.toString();
    }
}