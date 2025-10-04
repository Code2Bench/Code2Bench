package p82;
public class GroundTruth {
    public static String getBaseUrlSafely(String url) {
        int queryOrFragmentIndex = Math.min(url.indexOf('?'), url.indexOf('#'));
        if (queryOrFragmentIndex < 0) {
            queryOrFragmentIndex = url.length();
        }
        return url.substring(0, queryOrFragmentIndex);
    }
}