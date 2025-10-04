package p6;
public class GroundTruth {
    public static boolean isWithinString(String jsonStr, int pos) {
        boolean inString = false;
        boolean escaped = false;
        
        for (int i = 0; i < pos; i++) {
            char c = jsonStr.charAt(i);
            if (c == '\\' && !escaped) {
                escaped = true;
            } else if (c == '\"' && !escaped) {
                inString = !inString;
                escaped = false;
            } else {
                escaped = false;
            }
        }
        
        return inString;
    }
}