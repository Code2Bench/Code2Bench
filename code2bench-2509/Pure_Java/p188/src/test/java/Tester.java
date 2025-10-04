package p188;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.stream.Stream;
import static org.junit.jupiter.api.Assertions.assertTrue;
import p188.Helper;
import p188.Tested;

public class Tester {

    static class TestCase {
        public Inputs Inputs;
        public float Expected;

        static class Inputs {
            public float[] data1;
            public float[] data2;
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
    void testCalculateCorrelation(TestCase tc) {
        float actual = Tested.calculateCorrelation(tc.Inputs.data1, tc.Inputs.data2);
        assertTrue(
            Helper.deepCompare(tc.Expected, actual, 0),
            String.format(
                "Test case failed:%nInputs: data1=%s, data2=%s%nExpected: %s%nActual: %s",
                java.util.Arrays.toString(tc.Inputs.data1), java.util.Arrays.toString(tc.Inputs.data2), tc.Expected, actual
            )
        );
    }
}