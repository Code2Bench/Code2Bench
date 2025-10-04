package p5;
public class GroundTruth {
    public static String preProcessJson(String jsonStr) {
        if (jsonStr == null) {
            return "{}";
        }

        // 去除前后空白
        jsonStr = jsonStr.trim();

        // 如果是空字符串，返回空对象
        if (jsonStr.isEmpty()) {
            return "{}";
        }

        // 确保JSON对象和数组有正确的开始和结束
        if (jsonStr.startsWith("{") && !jsonStr.endsWith("}")) {
            jsonStr = jsonStr + "}";
        } else if (jsonStr.startsWith("[") && !jsonStr.endsWith("]")) {
            jsonStr = jsonStr + "]";
        } else if (!jsonStr.startsWith("{") && !jsonStr.startsWith("[")) {
            // 如果不是以{或[开头，尝试将其包装为对象
            jsonStr = "{" + jsonStr + "}";
        }

        return jsonStr;
    }
}