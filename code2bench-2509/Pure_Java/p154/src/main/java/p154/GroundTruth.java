package p154;
public class GroundTruth {
    public static String getNextVersion(String currentVersion, boolean minorVersion) {
        String[] versionSplit = currentVersion.split("\\.");
        if (minorVersion) {
            return versionSplit[0] + "." + (Integer.parseInt(versionSplit[1]) + 1);
        }
        // return (Integer.parseInt(versionSplit[0]) + 1) + "." + versionSplit[1];
        // 大版本升级后，小版本号归0
        return (Integer.parseInt(versionSplit[0]) + 1) + ".0";
    }
}