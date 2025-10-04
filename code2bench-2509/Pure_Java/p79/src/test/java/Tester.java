package p79;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.stream.Stream;
import static org.junit.jupiter.api.Assertions.assertTrue;
import p79.Helper;
import p79.Tested;

public class Tester {

    static class TestCase {
        public Inputs Inputs;
        public float[] Expected;

        static class Inputs {
            public float x;
            public float y;
            public float lx;
            public float ly;
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
    void testGetClampedAnalogPosition(TestCase tc) {
        float[] actual = Tested.getClampedAnalogPosition(tc.Inputs.x, tc.Inputs.y, tc.Inputs.lx, tc.Inputs.ly);
        assertTrue(
            Helper.deepCompare(tc.Expected, actual, 0),
            String.format(
                "Test case failed:%nInputs: x=%.2f, y=%.2f, lx=%.2f, ly=%.2f%nExpected: [%.2f, %.2f]%nActual: [%.2f, %.2f]",
                tc.Inputs.x, tc.Inputs.y, tc.Inputs.lx, tc.Inputs.ly, tc.Expected[0], tc.Expected[1], actual[0], actual[1]
            )
        );
    }
}