package p33;
public class GroundTruth {
    public static String getStorageId(String storageId,
                                      String storageAndRepositoryId)
    {
        String[] storageAndRepositoryIdTokens = storageAndRepositoryId.split(":");

        return storageAndRepositoryIdTokens.length == 2 ? storageAndRepositoryIdTokens[0] : storageId;
    }
}