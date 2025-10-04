package p96;
public class GroundTruth {
    public static String extractUrlFromDebugInfo(String debugInfo) {
        // 简单的字符串匹配，实际实现可能需要更复杂的解析
        String[] lines = debugInfo.split("\n");
        for (String line : lines) {
            if (line.contains("Full URL:")) {
                return line.substring(line.indexOf("Full URL:") + 9).trim();
            }
        }
        return null;
    }
}