package p14;
public class GroundTruth {
    public static String escapeCsvField(Object field) {
        if (field == null) {
            return "";
        }
        String s = String.valueOf(field);
        if (s.contains(",") || s.contains("\"") || s.contains("\n")) {
            return "\"" + s.replace("\"", "\"\"") + "\"";
        }
        return s;
    }
}