package p203;
public class GroundTruth {
    public static String getShortNumber(long l) {
        if(l >= Math.pow(10, 18)) {
            double res = l / Math.pow(10, 18);
            res = Math.round(res * 100.0) / 100.0;
            return res + "E";
        }
        if(l >= Math.pow(10, 15)) {
            double res = l / Math.pow(10, 15);
            res = Math.round(res * 100.0) / 100.0;
            return res + "P";
        }
        if(l >= Math.pow(10, 12)) {
            double res = l / Math.pow(10, 12);
            res = Math.round(res * 100.0) / 100.0;
            return res + "T";
        }
        if(l >= Math.pow(10, 9)) {
            double res = l / Math.pow(10, 9);
            res = Math.round(res * 100.0) / 100.0;
            return res + "G";
        }
        if(l >= Math.pow(10, 6)) {
            double res = l / Math.pow(10, 6);
            res = Math.round(res * 100.0) / 100.0;
            return res + "M";
        }
        if(l >= Math.pow(10, 3)) {
            double res = l / Math.pow(10, 3);
            res = Math.round(res * 100.0) / 100.0;
            return res + "k";
        }
        return Long.toString(l);
    }
}