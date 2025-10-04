package p34;
public class GroundTruth {
    public static String getRepositoryId(String storageAndRepositoryId) {
        String[] storageAndRepositoryIdTokens = storageAndRepositoryId.split(":");
        return storageAndRepositoryIdTokens[storageAndRepositoryIdTokens.length < 2 ? 0 : 1];
    }
}