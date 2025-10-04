package p272;
public class GroundTruth {
    public static byte[] getCJKEncodingBytes(int[] glyph, int size) {
        byte[] result = new byte[size * 2];
        for (int i = 0; i < size; i++) {
            int g = glyph[i];
            result[i * 2] = (byte) (g >> 8);
            result[i * 2 + 1] = (byte) (g & 0xFF);
        }
        return result;
    }
}