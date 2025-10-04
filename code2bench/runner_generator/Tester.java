package p0;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import java.io.File;
import java.util.List;
import java.util.Map;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class Tester {

    static class TestCase {
        public Map<String, Object> Inputs;
        public Object Expected;
    }

    @Test
    public void testFromJson() throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        List<TestCase> cases = mapper.readValue(
                new File("src/test/java/test_cases/test_cases.json"),
                new TypeReference<List<TestCase>>() {
                });

        for (int i = 0; i < cases.size(); i++) {
            TestCase tc = cases.get(i);
            Object actual = Tested._get_correct_indent_level(tc.Inputs);

            assertTrue(
                    Helper.deepCompare(tc.Expected, actual, 1e-6),
                    String.format("Test case %d failed%nInputs: %s%nExpected: %s%nActual: %s",
                            i, tc.Inputs, tc.Expected, actual));
        }
    }
}