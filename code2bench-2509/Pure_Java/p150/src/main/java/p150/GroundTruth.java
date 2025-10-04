package p150;
public class GroundTruth {
    public static String[] sepClassAndMthSig(String fullSig) {
        int pos = fullSig.indexOf('(');
        if (pos != -1) {
            pos = fullSig.lastIndexOf('.', pos);
            if (pos != -1) {
                String[] sigs = new String[2];
                sigs[0] = fullSig.substring(0, pos);
                sigs[1] = fullSig.substring(pos + 1);
                return sigs;
            }
        }
        return null;
    }
}