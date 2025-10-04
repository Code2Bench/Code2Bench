package template;

public class GroundTruth {
    // 你的被测函数
    public static int func0(int x, int y) {
        if (x > 0 && y > 0) {
            return x + y;
        } else if (x < 0 && y < 0) {
            return x - y;
        } else {
            return x * y;
        }
    }
}