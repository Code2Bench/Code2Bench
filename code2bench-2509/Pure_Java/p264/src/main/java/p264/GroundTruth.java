package p264;
public class GroundTruth {
    public static byte[] decrypt(byte[] d, int start, int end, int key, int skip) {
        if (end - start - skip < 0) {
            skip = 0;
        }
        byte[] o = new byte[end - start - skip];
        int r = key;
        int ipos;
        int c1 = 52845;
        int c2 = 22719;
        for (ipos = start; ipos < end; ipos++) {
            int c = d[ipos] & 0xff;
            int p = (c ^ (r >> 8)) & 0xff;
            r = ((c + r) * c1 + c2) & 0xffff;
            if (ipos - start - skip >= 0) {
                o[ipos - start - skip] = (byte) p;
            }
        }
        return o;
    }
}