package p113;
public class GroundTruth {
    public static String formatNodeIds(int[] nodes) {
        StringBuilder b = new StringBuilder("[");
        if (nodes != null) {
            for (int i = 0; i < nodes.length; i++) {
                b.append(nodes[i]);
                if (i < nodes.length - 1) {
                    b.append(',');
                }
            }
        }
        b.append("]");
        return b.toString();
    }
}