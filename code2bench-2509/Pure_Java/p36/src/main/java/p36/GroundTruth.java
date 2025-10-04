package p36;
public class GroundTruth {
    public static String[] getPathElements(String path) {
        if (path == null) {
            return new String[0];
        } else {
            if (path.startsWith("/")) {
                path = path.substring(1);
            }

            return path.split("/");
        }
    }
}