package p191;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.stream.Stream;
import static org.junit.jupiter.api.Assertions.assertTrue;
import p191.Helper;
import p191.Tested;

public class Tester {

    static class TestCase {
        public Inputs Inputs;
        public double Expected;

        static class Inputs {
            public double time;
            public double begin;
            public double change;
            public double duration;
            public double overshoot;
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
    void testBLI_easing_back_ease_in_out(TestCase tc) {
        double actual = Tested.BLI_easing_back_ease_in_out(tc.Inputs.time, tc.Inputs.begin, tc.Inputs.change, tc.Inputs.duration, tc.Inputs.overshoot);
        assertTrue(
            Helper.deepCompare(tc.Expected, actual, 0),
            String.format(
                "Test case failed:%nInputs: time=%f, begin=%f, change=%f, duration=%f, overshoot=%f%nExpected: %f%nActual: %f",
                tc.Inputs.time, tc.Inputs.begin, tc.Inputs.change, tc.Inputs.duration, tc.Inputs.overshoot, tc.Expected, actual
            )
        );
    }
}