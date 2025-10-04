package p119;
public class GroundTruth {
    public static String stripExtension(String filename) {
        int i = filename.lastIndexOf('.');
        if (i > 0) return filename.substring(0, i);
        return filename;
    }
}