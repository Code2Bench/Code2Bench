package p135;
public class GroundTruth {
    public static boolean isPrintableCodePoint(int codePoint) {
        if (Character.isISOControl(codePoint)) {
            return false;
        }
        if (Character.isWhitespace(codePoint)) {
            // don't print whitespaces other than standard one
            return codePoint == ' ';
        }
        switch (Character.getType(codePoint)) {
            case Character.CONTROL:
            case Character.FORMAT:
            case Character.PRIVATE_USE:
            case Character.SURROGATE:
            case Character.UNASSIGNED:
                return false;
        }
        return true;
    }
}