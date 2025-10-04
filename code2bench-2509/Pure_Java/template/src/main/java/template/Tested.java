package template;

import java.util.List;

public class Tested {
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