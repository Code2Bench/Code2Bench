package p115;
public class GroundTruth {
    public static String stripLeadingTrailingSlash(String location) {
        if (location.startsWith("/")) {
            return stripLeadingTrailingSlash(location.substring(1));
        }
        if (location.endsWith("/")) {
            return location.substring(0, location.length() - 1);
        } else {
            return location;
        }
    }
}