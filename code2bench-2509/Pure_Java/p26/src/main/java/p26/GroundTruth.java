package p26;
public class GroundTruth {
    public static String formatSize(long size) {
        if (size <= 0) {
            return "0 B";
        }
        String[] units = {"B", "KB", "MB", "GB", "TB"};
        int digitGroups = (int) (Math.log10(size) / Math.log10(1000));
        return String.format("%.1f %s", size / Math.pow(1000, digitGroups), units[digitGroups]);
    }
}