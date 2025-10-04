package p76;
public class GroundTruth {
    public static byte[] hexToBinary(String hex) {
        byte[] result = new byte[hex.length() / 2];
        for (int i = 0; i < result.length; i++) {
            int index = i * 2;
            int value = Integer.parseInt(hex.substring(index, index + 2), 16);
            result[i] = (byte)value;
        }
        return result;
    }
}