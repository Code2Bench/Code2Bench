package p21;
public class GroundTruth {
    public static String rewriteByStoreAndRepo(String path, String storageId, String repositoryId) {
        String[] split = path.split("/");
        if (split.length <= 4) {
            return path;
        } else {
            split[2] = storageId;
            split[3] = repositoryId;
            return String.join("/", split);
        }
    }
}