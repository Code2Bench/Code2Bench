package p80;

import java.util.Objects;

public class Tested {
    /**
     * Converts a bitmask representing CPU affinity into a boolean array indicating which CPUs are enabled.
     * Each bit in the mask corresponds to a CPU index, where a value of 1 indicates the CPU is enabled.
     * The length of the resulting array is determined by the number of available processors on the system.
     *
     * @param mask A bitmask where each bit represents the affinity for a CPU. The least significant bit (LSB)
     *             corresponds to CPU index 0, the next bit to CPU index 1, and so on. Must be non-negative.
     * @return A boolean array of length equal to the number of available processors. Each element in the array
     *         is {@code true} if the corresponding CPU is enabled in the mask, otherwise {@code false}.
     * @throws NullPointerException if the mask is negative (though the method does not explicitly throw this,
     *         it is implied by the bitwise operations).
     */
    public static boolean[] maskToCpuAffinity(long mask) {
        // TODO: implement this method
    }
}