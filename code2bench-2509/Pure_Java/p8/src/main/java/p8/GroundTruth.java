package p8;
public class GroundTruth {
    public static String extractFirstJsonObject(String text) {
        int startIndex = text.indexOf('{');
        if (startIndex != -1) {
            // Find matching closing brace
            int braceCount = 1;
            for (int i = startIndex + 1; i < text.length(); i++) {
                char c = text.charAt(i);
                if (c == '{') braceCount++;
                else if (c == '}') braceCount--;
                
                if (braceCount == 0) {
                    return text.substring(startIndex, i + 1);
                }
            }
        }
        return "{}"; // Return empty object if no JSON found
    }
}