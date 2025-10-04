package p243;
public class GroundTruth {
    public static int calculateProgress(long bytesDownloaded, long totalBytes) {
        if (totalBytes <= 0) {
            return 0;
        }
        
        int progress = (int) ((bytesDownloaded * 100) / totalBytes);
        return Math.min(progress, 100); // Ensure progress doesn't exceed 100%
    }
}