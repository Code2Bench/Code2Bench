package p45;
public class GroundTruth {
    public static String getExtension(String path) {
        if (path == null) {
            return null;
        }
        int dotPos = path.lastIndexOf('.');
        if (dotPos < 0) {
            return null;
        }
        return path.substring(dotPos + 1);
    }
}