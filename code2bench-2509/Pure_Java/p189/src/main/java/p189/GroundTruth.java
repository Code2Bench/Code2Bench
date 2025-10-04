package p189;
public class GroundTruth {
    public static boolean urlEqualsIgnoreSlash(String a, String b) {
        if (!a.endsWith("/"))
            a += "/";
        if (!b.endsWith("/"))
            b += "/";
        return a.equals(b);
    }
}