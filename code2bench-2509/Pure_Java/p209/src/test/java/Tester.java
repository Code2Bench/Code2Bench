package p209;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.stream.Stream;
import static org.junit.jupiter.api.Assertions.assertTrue;
import p209.Helper;
import p209.Tested;

public class Tester {

    static class TestCase {
        public Inputs Inputs;
        public long Expected;

        static class Inputs {
            public float initialPos;
            public float velocity;
            public float acceleration;
            public Long targetTime;
            public Float targetVelocity;
            public int minBound;
            public int maxBound;
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
    void testComputeBound(TestCase tc) {
        long actual = Tested.computeBound(
            tc.Inputs.initialPos,
            tc.Inputs.velocity,
            tc.Inputs.acceleration,
            tc.Inputs.targetTime,
            tc.Inputs.targetVelocity,
            tc.Inputs.minBound,
            tc.Inputs.maxBound
        );
        assertTrue(
            Helper.deepCompare(tc.Expected, actual, 0),
            String.format(
                "Test case failed:%nInputs: initialPos=%f, velocity=%f, acceleration=%f, targetTime=%s, targetVelocity=%s, minBound=%d, maxBound=%d%nExpected: %d%nActual: %d",
                tc.Inputs.initialPos, tc.Inputs.velocity, tc.Inputs.acceleration, tc.Inputs.targetTime, tc.Inputs.targetVelocity, tc.Inputs.minBound, tc.Inputs.maxBound, tc.Expected, actual
            )
        );
    }
}