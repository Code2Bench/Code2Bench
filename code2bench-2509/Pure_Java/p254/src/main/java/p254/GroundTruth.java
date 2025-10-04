package p254;
public class GroundTruth {
    public static boolean hasSimpleNameContract(String input) {
        int lastDot = input.lastIndexOf('.');
        String simpleName;
        if (lastDot == -1) {
            simpleName = input;
        } else {
            simpleName = input.substring(lastDot + 1);
        }
        return simpleName.equals("Contract");
    }
}