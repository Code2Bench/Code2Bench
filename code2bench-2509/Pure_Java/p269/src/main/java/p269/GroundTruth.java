package p269;
public class GroundTruth {
    public static String convertFromUtf32(int codePoint) {
        if (codePoint < 0x10000) {
            return Character.toString((char) codePoint);
        }
        codePoint -= 0x10000;
        return new String(new char[]{(char) ((codePoint / 0x400) + 0xd800), (char) ((codePoint % 0x400) + 0xdc00)});
    }
}