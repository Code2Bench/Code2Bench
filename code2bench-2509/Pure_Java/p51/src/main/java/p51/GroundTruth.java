package p51;
public class GroundTruth {
    public static String calculateParameterName(String property, int n) {
        if (property == null) {
            return "";
        }
        property = property.replace(".toLowerCase()", "");
        property = property.replace("@", "");
        return String.format("%s_%s", property.substring(property.lastIndexOf(".") + 1), n);
    }
}