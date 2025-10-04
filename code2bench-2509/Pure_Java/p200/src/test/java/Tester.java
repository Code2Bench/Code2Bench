package p200;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.stream.Stream;
import static org.junit.jupiter.api.Assertions.assertTrue;
import p200.Helper;
import p200.Tested;

public class Tester {

    static class TestCase {
        public Inputs Inputs;
        public double Expected;

        static class Inputs {
            public char operator;
            public double x;
            public double y;
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
    void testEvaluateOperator(TestCase tc) {
        double actual = Tested.evaluateOperator(tc.Inputs.operator, tc.Inputs.x, tc.Inputs.y);
        assertTrue(
            Helper.deepCompare(tc.Expected, actual, 0),
            String.format(
                "Test case failed:%nInputs: operator=%c, x=%f, y=%f%nExpected: %f%nActual: %f",
                tc.Inputs.operator, tc.Inputs.x, tc.Inputs.y, tc.Expected, actual
            )
        );
    }
}