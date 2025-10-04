package p137;
public class GroundTruth {
    public static String fromName(String name) {
        if (name == null || name.isEmpty()) {
            return null;
        }
        if (name.toUpperCase().equals(name)) {
            // all characters are upper case
            return name.toLowerCase();
        }
        String v1 = Character.toLowerCase(name.charAt(0)) + name.substring(1);
        if (!v1.equals(name)) {
            return v1;
        }
        if (name.length() < 3) {
            return name + "Var";
        }
        return null;
    }
}