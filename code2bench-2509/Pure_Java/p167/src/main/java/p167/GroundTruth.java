package p167;
public class GroundTruth {
    public static String formatJsonStr(String jstr) {
        StringBuilder result = new StringBuilder();
        boolean insideQuotes = false;
        char lastChar = ' ';

        for (int i = 0; i < jstr.length(); i++) {
            char currentChar = jstr.charAt(i);

            if (lastChar != '\\' && currentChar == '"') {
                insideQuotes = !insideQuotes;
            }

            lastChar = currentChar;

            if (!insideQuotes && currentChar == '\n') {
                continue;
            }

            if (insideQuotes && currentChar == '\n') {
                result.append("\\n");
            } else if (insideQuotes && currentChar == '\t') {
                result.append("\\t");
            } else {
                result.append(currentChar);
            }
        }

        return result.toString();
    }
}