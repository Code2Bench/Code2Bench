package p7;
public class GroundTruth {
    public static String handleTrailingCommas(String jsonStr) {
        // 处理对象中的多余逗号
        StringBuilder sb = new StringBuilder(jsonStr);
        int i = 0;
        while (i < sb.length() - 1) {
            if (sb.charAt(i) == ',' && 
                    (sb.charAt(i + 1) == '}' || sb.charAt(i + 1) == ']')) {
                sb.deleteCharAt(i);
                continue;
            }
            i++;
        }
        
        return sb.toString();
    }
}