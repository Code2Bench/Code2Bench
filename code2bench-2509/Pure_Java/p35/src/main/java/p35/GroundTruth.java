package p35;
public class GroundTruth {
    public static String getExtension(String path) {
        if (path == null) {
            return null;
        } else {
            int dotPos = path.lastIndexOf(46);
            return dotPos < 0 ? null : path.substring(dotPos + 1);
        }
    }
}