package p162;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.stream.Stream;
import static org.junit.jupiter.api.Assertions.assertTrue;
import p162.Helper;
import p162.Tested;

public class Tester {

    static class TestCase {
        public Inputs Inputs;
        public double Expected;

        static class Inputs {
            public double p1;
            public double p2;
            public double a1;
            public double a2;
            public double b1;
            public double b2;
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
    void testOffset(TestCase tc) {
        double actual = Tested.offset(tc.Inputs.p1, tc.Inputs.p2, tc.Inputs.a1, tc.Inputs.a2, tc.Inputs.b1, tc.Inputs.b2);
        assertTrue(
            Helper.deepCompare(tc.Expected, actual, 0),
            String.format(
                "Test case failed:%nInputs: p1=%f, p2=%f, a1=%f, a2=%f, b1=%f, b2=%f%nExpected: %f%nActual: %f",
                tc.Inputs.p1, tc.Inputs.p2, tc.Inputs.a1, tc.Inputs.a2, tc.Inputs.b1, tc.Inputs.b2, tc.Expected, actual
            )
        );
    }
}