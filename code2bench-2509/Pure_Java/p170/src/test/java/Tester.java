package p170;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.stream.Stream;
import static org.junit.jupiter.api.Assertions.assertTrue;
import p170.Helper;
import p170.Tested;

public class Tester {

    static class TestCase {
        public Inputs Inputs;
        public int[] Expected;

        static class Inputs {
            public byte[] array;
            public int offset;
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
    void testGetUtf8(TestCase tc) {
        int[] actual = Tested.getUtf8(tc.Inputs.array, tc.Inputs.offset);
        assertTrue(
            Helper.deepCompare(tc.Expected, actual, 0),
            String.format(
                "Test case failed:%nInputs: array=%s, offset=%d%nExpected: [%d, %d]%nActual: [%d, %d]",
                java.util.Arrays.toString(tc.Inputs.array), tc.Inputs.offset, tc.Expected[0], tc.Expected[1], actual[0], actual[1]
            )
        );
    }
}