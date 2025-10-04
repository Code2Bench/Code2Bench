package p21;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.stream.Stream;
import static org.junit.jupiter.api.Assertions.assertTrue;
import p21.Helper;
import p21.Tested;

public class Tester {

    static class TestCase {
        public Inputs Inputs;
        public String Expected;

        static class Inputs {
            public String path;
            public String storageId;
            public String repositoryId;
        }
    }

    private static List<TestCase> loadTestCases(String filePath) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        File file = new File(filePath);
        try {
            return mapper.readValue(file, new TypeReference<List<TestCase>>() {});
        } catch (IOException e) {
            throw new IOException("Failed to load test cases from " + filePath + ": " + e.getMessage(), e);
        }
    }

    private static Stream<TestCase> testCases() throws IOException {
        return loadTestCases("src/test/java/test_cases/test_cases.json").stream();
    }

    @ParameterizedTest(name = "TestCase{index}")
    @MethodSource("testCases")
    void testRewriteByStoreAndRepo(TestCase tc) {
        String actual = Tested.rewriteByStoreAndRepo(tc.Inputs.path, tc.Inputs.storageId, tc.Inputs.repositoryId);
        assertTrue(
            Helper.deepCompare(tc.Expected, actual, 0),
            String.format(
                "Test case failed:%nInputs: path=%s, storageId=%s, repositoryId=%s%nExpected: %s%nActual: %s",
                tc.Inputs.path, tc.Inputs.storageId, tc.Inputs.repositoryId, tc.Expected, actual
            )
        );
    }
}