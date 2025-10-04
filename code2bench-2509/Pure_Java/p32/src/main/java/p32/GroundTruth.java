package p32;
public class GroundTruth {
    public static String toInstanceVariableName(String className) {
        if (className == null || className.isEmpty()) {
            return className;
        }
        // 首字母转为小写 + 剩余子字符串
        return Character.toLowerCase(className.charAt(0)) + className.substring(1)+"Strategy";
    }
}