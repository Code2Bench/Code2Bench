package p267;
public class GroundTruth {
    public static int stringToTag(String tag) {
        char[] c = tag.toCharArray();

        if (c.length != 4) {
            throw new IllegalArgumentException("Bad tag length: " + tag);
        }

        return c[0] << 24 | c[1] << 16 | c[2] << 8 | c[3];
    }
}