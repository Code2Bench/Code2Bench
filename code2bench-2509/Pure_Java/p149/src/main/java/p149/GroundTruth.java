package p149;
public class GroundTruth {
    public static int unhex(byte[] hex) {
        int n = 0;
        byte b;
        for (int i = 0; i < 4; i++) {
            b = hex[i];
            switch (b) {
                case '0':
                case '1':
                case '2':
                case '3':
                case '4':
                case '5':
                case '6':
                case '7':
                case '8':
                case '9':
                    b -= '0';
                    break;
                case 'a':
                case 'b':
                case 'c':
                case 'd':
                case 'e':
                case 'f':
                    b = (byte) (b - 'a' + 10);
                    break;
                case 'A':
                case 'B':
                case 'C':
                case 'D':
                case 'E':
                case 'F':
                    b = (byte) (b - 'A' + 10);
                    break;
                default:
                    return -1;
            }
            n = (n << 4) | (b & 0xff);
        }
        return n;
    }
}