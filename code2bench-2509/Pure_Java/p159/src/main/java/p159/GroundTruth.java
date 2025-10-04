package p159;
public class GroundTruth {
    public static String getOutputStatement(String toDisplay) {
        // We will use out:print function to output statements
        StringBuilder stringBuffer = new StringBuilder();
        stringBuffer.append("out:print(\"");

        int length = toDisplay.length();
        for (int i = 0; i < length; i++) {
            char c = toDisplay.charAt(i);
            switch (c) {
                case '"':
                    stringBuffer.append("\\\"");
                    break;
                case '\\':
                    stringBuffer.append("\\\\");
                    break;
                default:
                    stringBuffer.append(c);
                    break;
            }
        }
        stringBuffer.append("\")");
        return stringBuffer.toString();
    }
}