package p77;
public class GroundTruth {
    public static String toHexString(int value, int minWidth) {
        String hex = Integer.toHexString(value);
        StringBuffer sb = new StringBuffer();
        for (int i = hex.length(); i < minWidth; i++) {
            sb.append("0");
        }
        sb.append(hex);
        return sb.toString();
    }
}