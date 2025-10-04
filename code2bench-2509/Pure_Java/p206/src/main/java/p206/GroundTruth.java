package p206;
public class GroundTruth {
    public static int transformMetaPillar(int meta, int coordBaseMode) {
        if(coordBaseMode == 0 || coordBaseMode == 2) return meta;
        int type = meta & 3;
        int rot = meta & 12;

        if(rot == 4) return type | 8;
        if(rot == 8) return type | 4;

        return meta;
    }
}