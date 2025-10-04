package p133;
public class GroundTruth {
    public static boolean isValidIdentifierStart(int codePoint) {
        char ch = Character.toChars(codePoint)[0];
        return Character.isJavaIdentifierStart(codePoint)
                || ch == '@'
                || ch == '.'
                || ch == '#';
    }
}