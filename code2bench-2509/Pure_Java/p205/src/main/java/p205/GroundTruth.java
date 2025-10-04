package p205;
public class GroundTruth {
    public static int transformMetaDecoModel(int meta, int coordBaseMode) {
        if(coordBaseMode == 0) return meta;
        int rot = (meta + coordBaseMode) % 4;
        int type = (meta / 4) * 4;

        return rot | type;
    }
}