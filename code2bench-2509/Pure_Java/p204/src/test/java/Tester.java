package p204;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.stream.Stream;
import static org.junit.jupiter.api.Assertions.assertTrue;
import p204.Helper;
import p204.Tested;

public class Tester {

    static class TestCase {
        public Inputs Inputs;
        public double Expected;

        static class Inputs {
            public int x1;
            public int z1;
            public int x2;
            public int z2;
            public int px;
            public int pz;
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
    void testPointSegmentDist(TestCase tc) {
        double actual = Tested.pointSegmentDist(tc.Inputs.x1, tc.Inputs.z1, tc.Inputs.x2, tc.Inputs.z2, tc.Inputs.px, tc.Inputs.pz);
        assertTrue(
            Helper.deepCompare(tc.Expected, actual, 0),
            String.format(
                "Test case failed:%nInputs: x1=%d, z1=%d, x2=%d, z2=%d, px=%d, pz=%d%nExpected: %s%nActual: %s",
                tc.Inputs.x1, tc.Inputs.z1, tc.Inputs.x2, tc.Inputs.z2, tc.Inputs.px, tc.Inputs.pz, tc.Expected, actual
            )
        );
    }
}