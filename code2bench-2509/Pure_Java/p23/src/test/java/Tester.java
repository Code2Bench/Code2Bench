package p23;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.stream.Stream;
import static org.junit.jupiter.api.Assertions.assertTrue;
import p23.Helper;
import p23.Tested;

public class Tester {

    static class TestCase {
        public Inputs Inputs;
        public boolean Expected;

        static class Inputs {
            public String ip;
            public String cidr;
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
    void testIsInRange(TestCase tc) {
        boolean actual = Tested.isInRange(tc.Inputs.ip, tc.Inputs.cidr);
        assertTrue(
            Helper.deepCompare(tc.Expected, actual, 0),
            String.format(
                "Test case failed:%nInputs: ip=%s, cidr=%s%nExpected: %s%nActual: %s",
                tc.Inputs.ip, tc.Inputs.cidr, tc.Expected, actual
            )
        );
    }
}