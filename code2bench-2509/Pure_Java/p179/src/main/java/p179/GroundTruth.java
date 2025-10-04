package p179;
public class GroundTruth {
    public static String create(int codelength) {
        String vcode = "";
        for (int i = 0; i < codelength; i++) {
            vcode = vcode + (int)(Math.random() * 9);
        }
        return vcode;
    }
}