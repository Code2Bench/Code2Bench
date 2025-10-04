package p156;
public class GroundTruth {
    public static String[] parseVersion(String version) {
        if (version.startsWith("1.")) {
            version = version.substring(2); // 去掉前面的 "1."
        }
        version = version.replace("_", ".").replace("u", ".");
        return version.split("\\.");
    }
}