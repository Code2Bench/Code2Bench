package p118;
public class GroundTruth {
    public static boolean isSafeExecutable(String exec) {
        if (exec == null || exec.isBlank()) return false;
        // allow word chars, dot, slash, backslash, dash and underscore (no spaces or shell metas)
        return exec.matches("^[\\w./\\\\-]+$");
    }
}