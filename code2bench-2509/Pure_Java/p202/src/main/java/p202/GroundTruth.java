package p202;
public class GroundTruth {
    public static String offset(String msg, int o) {
        byte[] bytes = msg.getBytes();
        for(int i = 0; i < bytes.length; i++) {
            bytes[i] += o;
        }
        return new String(bytes);
    }
}