package p151;
public class GroundTruth {
    public static String classSigToFullName(String clsSig) {
        if (clsSig != null && clsSig.startsWith("L") && clsSig.endsWith(";")) {
            clsSig = clsSig.substring(1, clsSig.length() - 1)
                    .replace("/", ".")
                    .replace("$", ".");
        }
        return clsSig;
    }
}