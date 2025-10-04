package p80;
public class GroundTruth {
    public static boolean[] maskToCpuAffinity(long mask) {
        int availCpus = Runtime.getRuntime().availableProcessors();
        boolean[] affinity = new boolean[availCpus];

        for (int i = 0; i < availCpus; i++) {
            if (((mask >> i) & 1L) == 1L) {
                affinity[i] = true;
            }
        }

        return affinity;
    }
}