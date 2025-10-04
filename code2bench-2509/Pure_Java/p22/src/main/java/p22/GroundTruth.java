package p22;
public class GroundTruth {
    public static String[] stringToStringArray(String src, int length) {
        int len = src.length();
        int startIndex = 0;
        int endIndex = length;
        int numChunks = (int) Math.ceil((double) len / length); // 计算需要的子字符串数量
        String[] chunks = new String[numChunks];
        for (int i = 0; i < numChunks; i++) {
            if (endIndex > len) {
                endIndex = len;
            }
            String substring = src.substring(startIndex, endIndex);
            chunks[i] = substring;
            startIndex = endIndex;
            endIndex += length;
        }
        return chunks;
    }
}