package p170;
public class GroundTruth {
    public static int[] getUtf8(byte[] array, int offset) {
        int val = array[offset];

        // We skip the utf16 length of the string.
        if ((val & 0x80) != 0) {
            offset += 2;
        } else {
            offset += 1;
        }

        // And we read only the utf-8 encoded length of the string.
        val = array[offset];
        offset += 1;
        int length;
        if ((val & 0x80) != 0) {
            int low = array[offset] & 0xFF;
            length = ((val & 0x7F) << 8) + low;
            offset += 1;
        } else {
            length = val;
        }

        return new int[] { offset, length };
    }
}