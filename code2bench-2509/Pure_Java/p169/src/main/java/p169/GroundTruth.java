package p169;
public class GroundTruth {
    public static String getPreferredString(String stringPoolValue, String resourceMapValue) {
        String value = stringPoolValue;

        if (stringPoolValue != null && resourceMapValue != null) {
            int slashPos = stringPoolValue.lastIndexOf('/');
            int colonPos = stringPoolValue.lastIndexOf(':');

            // Handle a value with a format of "@yyy/xxx", but avoid "@yyy/zzz:xxx"
            if (slashPos != -1) {
                if (colonPos == -1) {
                    String type = stringPoolValue.substring(0, slashPos);
                    value = type + "/" + resourceMapValue;
                }
            } else if (!stringPoolValue.equals(resourceMapValue)) {
                value = resourceMapValue;
            }
        }
        return value;
    }
}