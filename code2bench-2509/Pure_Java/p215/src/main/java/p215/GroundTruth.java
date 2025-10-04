package p215;
public class GroundTruth {
    public static String extractTokenisedCookieValue(
            final int i, final int numberOfCookies, final int maxCookieLength, final String cookieValue) {
        return i == (numberOfCookies - 1)
                ? cookieValue.substring((i * maxCookieLength))
                : cookieValue.substring((i * maxCookieLength), ((i * maxCookieLength) + maxCookieLength));
    }
}