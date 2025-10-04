package p113;

import java.util.Objects;

public class Tested {
    /**
     * Formats an array of node IDs into a string representation enclosed in square brackets.
     * The node IDs are separated by commas. If the input array is {@code null}, the method
     * still returns a string with empty brackets.
     *
     * @param nodes An array of node IDs to format. Can be {@code null}.
     * @return A string representation of the node IDs in the format "[id1,id2,...]". 
     *         If the input array is {@code null}, returns "[]".
     */
    private static String formatNodeIds(int[] nodes) {
        if (nodes == null) {
            return "[]";
        }
        
        StringBuilder sb = new StringBuilder();
        sb.append("[");
        
        for (int i = 0; i < nodes.length; i++) {
            sb.append(nodes[i]);
            if (i < nodes.length - 1) {
                sb.append(",");
            }
        }
        
        sb.append("]");
        return sb.toString();
    }
}