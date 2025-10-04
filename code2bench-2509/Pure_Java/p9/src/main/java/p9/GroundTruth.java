package p9;
public class GroundTruth {
    public static String cleanText(String text) {
        if (text == null) {
            return null;
        }
        
        // 移除HTML标签
        text = text.replaceAll("<[^>]*>", "");
        
        // 移除多余的空白字符
        text = text.replaceAll("\\s+", " ");
        
        return text.trim();
    }
}