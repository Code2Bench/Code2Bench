package p273;
public class GroundTruth {
    public static int calculateEANParity(String code) {
        int mul = 3;
        int total = 0;
        for (int k = code.length() - 1; k >= 0; --k) {
            int n = code.charAt(k) - '0';
            total += mul * n;
            mul ^= 2;
        }
        return (10 - (total % 10)) % 10;
    }
}