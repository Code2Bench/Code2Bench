package p134;
public class GroundTruth {
    public static boolean isValidIdentifierPart(int codePoint) {
        char ch = Character.toChars(codePoint)[0];

        return Character.isJavaIdentifierPart(codePoint)
                || ch == '@'
                || ch == '.'
                || ch == '-'
                || ch == '+'
                || ch == '='
                || ch == '/'
                || ch == '#';
    }
}