package p201;
public class GroundTruth {
    public static int log2(int in) {
        int log = 0;
        if((in & 0xffff0000) != 0) { in >>>= 16; log = 16; }
        if(in >= 256) { in >>>= 8; log += 8; }
        if(in >= 16) { in >>>= 4; log += 4; }
        if(in >= 4) { in >>>= 2; log += 2; }
        return log + (in >>> 1);
    }
}