package p27;
public class GroundTruth {
    public static String getSubPath(String url, int index) {
        String[] args = url.split("/");
        if (args.length < index + 1) {
            return null;
        }
        return args[index];
    }
}