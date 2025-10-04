package p10;
public class GroundTruth {
    public static String parseServerUrl(String serverUrl) {
        if (serverUrl.startsWith("http://") || serverUrl.startsWith("https://")) {
            return serverUrl;
        } else {
            // Assume host:port format
            return "http://" + serverUrl;
        }
    }
}