package p47;
public class GroundTruth {
    public static String calculateIndexPath(String crateName) {
        String ret;
        if (crateName.length() == 1) {
            ret = "1/" + crateName;
        } else if (crateName.length() == 2) {
            ret = "2/" + crateName;
        } else if (crateName.length() == 3) {
            ret = "3/" + crateName.charAt(0) + "/" + crateName;
        } else {
            ret = crateName.substring(0, 2) + "/" + crateName.substring(2, 4) + "/" + crateName;
        }
        return ret;
    }
}