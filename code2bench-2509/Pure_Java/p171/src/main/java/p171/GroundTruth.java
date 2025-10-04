package p171;
public class GroundTruth {
    public static boolean checkUpperHalfBitsFlipped(int original, int modified) {
        // Focus on bits 4-7 mask: 0b11110000 = 0xF0
        int originalMasked = original & 0xF0;
        int modifiedMasked = modified & 0xF0;
        return (originalMasked ^ modifiedMasked) != 0;
    }
}