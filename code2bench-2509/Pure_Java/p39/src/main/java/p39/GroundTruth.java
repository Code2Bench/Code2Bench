package p39;
public class GroundTruth {
    public static String removeNonPrintableCharacters(String str) {
        if (str == null)
            return null;
        return str.replaceAll("[^\\n\\r\\t\\p{Print}]", "");
    }
}