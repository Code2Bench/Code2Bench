package p232;
public class GroundTruth {
    public static String removeExtension(final String fileName) {
        final int pos = fileName.lastIndexOf(".");
        if (pos < 0) {
            return fileName;
        }
        return fileName.substring(0, pos);
    }
}