package p266;
public class GroundTruth {
    public static int findSlashName(byte[] d, String name) {
        int i;
        for (i = 0; i < d.length; i++) {
            if (d[i] == '/') {
                // check for key
                boolean found = true;
                for (int j = 0; j < name.length(); j++) {
                    if (d[i + j + 1] != name.charAt(j)) {
                        found = false;
                        break;
                    }
                }
                if (found) {
                    return i;
                }
            }
        }
        return -1;
    }
}