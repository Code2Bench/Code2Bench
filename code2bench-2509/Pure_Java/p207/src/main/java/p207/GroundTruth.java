package p207;
public class GroundTruth {
    public static String getBlobPathStr(String path) {
        if (path == null) {
            return null;
        }
        String relativePath = path.replaceAll("/test/result/\\d{4}/\\d{2}/\\d{2}/", "/test/result/");
        return relativePath;
    }
}