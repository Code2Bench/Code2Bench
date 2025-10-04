package p182;
public class GroundTruth {
    public static int calcNoteIndex(final int[] intervals, final int note, final int tonic /* 0=C .. 11=B */) {
        final int rel = Math.floorMod(note - tonic, 12);
        for (int i = 0; i < intervals.length; i++)
            if (intervals[i] == rel)
                return i;
        return 0;
    }
}