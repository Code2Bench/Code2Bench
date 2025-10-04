package p116;
public class GroundTruth {
    public static String stripTrailingSlash(String uri) {
        return uri.endsWith("/") && uri.length() > "file:///".length()
            ? uri.substring(0, uri.length() - 1)
            : uri;
    }
}