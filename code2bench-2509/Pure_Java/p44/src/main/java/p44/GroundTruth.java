package p44;
import java.io.File;
public class GroundTruth {
    public static String getFileName(String path) {
        if (path == null) {
            return null;
        }
        File dummy = new File(path);
        return dummy.getName();
    }
}