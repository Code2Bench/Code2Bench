package p259;
public class GroundTruth {
    public static String asBasicString(byte[] bytes, int offset, int length) {
        final char[] c = new char[length];
        for (int i = 0; i < c.length; ++i) {
            c[i] = (char) bytes[i + offset];
        }
        return new String(c);
    }
}