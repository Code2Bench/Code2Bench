package p97;
public class GroundTruth {
    public static Integer extractStatusCodeFromDebugInfo(String debugInfo) {
        String[] lines = debugInfo.split("\n");
        for (String line : lines) {
            if (line.contains("Status Code:")) {
                try {
                    String statusStr = line.substring(line.indexOf("Status Code:") + 12).trim();
                    return Integer.parseInt(statusStr);
                }
                catch (Exception e) {
                    // 忽略解析错误
                }
            }
        }
        return null;
    }
}