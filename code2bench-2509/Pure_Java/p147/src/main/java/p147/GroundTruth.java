package p147;
public class GroundTruth {
    public static String hexify(byte[] bytes) {
        char[] hexDigits = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F' };
        StringBuilder buf = new StringBuilder(bytes.length * 3);
        for (byte aByte : bytes) {
            buf.append(hexDigits[(aByte & 0xf0) >> 4]);
            buf.append(hexDigits[aByte & 0x0f]);
            buf.append(' ');
        }
        return buf.toString();
    }
}