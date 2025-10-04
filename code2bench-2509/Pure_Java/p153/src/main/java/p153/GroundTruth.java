package p153;
public class GroundTruth {
    public static String stringUtils(String text, String[] key, String[] values) {
        for (int i = 0; i < key.length; i++) {
            text = text.replace(key[i], values[i]);
        }
        return text;
    }
}