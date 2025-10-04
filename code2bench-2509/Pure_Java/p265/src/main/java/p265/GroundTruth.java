package p265;
public class GroundTruth {
    public static byte[] readASCII(byte[] data, int start, int end) {
        // each byte of output is derived from one character (two bytes) of
        // input
        byte[] o = new byte[(end - start) / 2];

        int count = 0;
        int bit = 0;

        for (int loc = start; loc < end; loc++) {
            char c = (char) (data[loc] & 0xff);
            byte b = (byte) 0;

            if (c >= '0' && c <= '9') {
                b = (byte) (c - '0');
            } else if (c >= 'a' && c <= 'f') {
                b = (byte) (10 + (c - 'a'));
            } else if (c >= 'A' && c <= 'F') {
                b = (byte) (10 + (c - 'A'));
            } else {
                // linefeed or something.  Skip.
                continue;
            }

            // which half of the byte are we?
            if ((bit++ % 2) == 0) {
                o[count] = (byte) (b << 4);
            } else {
                o[count++] |= b;
            }
        }

        return o;
    }
}