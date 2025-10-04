package p31;
public class GroundTruth {
    public static String toCaseInsensitiveRegex(String regex) {
        StringBuilder caseInsensitiveRegex = new StringBuilder();
        for (char c : regex.toCharArray()) {
            if (Character.isLetter(c)) {
                caseInsensitiveRegex.append("[").append(Character.toLowerCase(c)).append(Character.toUpperCase(c)).append("]");
            } else {
                caseInsensitiveRegex.append(c);
            }
        }
        return caseInsensitiveRegex.toString();
    }
}