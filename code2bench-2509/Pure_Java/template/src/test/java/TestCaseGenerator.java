import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.io.*;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;
// 添加属性测试框架所需的导入
import net.jqwik.api.*;
import net.jqwik.api.lifecycle.AfterContainer;
// 这个需要根据用户传入的是p1还是pn来调整，反正后面都是跟着一个Tested类
import template.GroundTruth;

public class TestCaseGenerator {

    static class TestCase {
        Map<String, Object> Inputs;
        Object Expected;
        TestCase(Map<String, Object> inputs, Object expected) {
            this.Inputs = inputs;
            this.Expected = expected;
        }
    }

    static List<TestCase> generatedCases = new ArrayList<>();
    static AtomicInteger caseCount = new AtomicInteger(0);
    static final int MAX_CASES = 500;


    @Property(tries = 10000)
    void generateTestCases(@ForAll("int32") int x, @ForAll("int32") int y) {
        if (caseCount.get() >= MAX_CASES) return;
        int result;
        try {
            result = GroundTruth.func0(x, y);
        } catch (Exception e) {
            return;
        }
        // 可选：只收集能覆盖不同分支的用例
        boolean meaningful = (x > 0 && y > 0) || (x < 0 && y < 0) || (x * y == result);
        if (!meaningful) return;

        Map<String, Object> inputs = new LinkedHashMap<>();
        inputs.put("x", x);
        inputs.put("y", y);
        generatedCases.add(new TestCase(inputs, result));
        caseCount.incrementAndGet();
    }

    @Provide
    Arbitrary<Integer> int32() {
        return Arbitraries.integers().between(-2147483648, 2147483647);
    }

    @AfterContainer
    static void saveTestCases() throws IOException {
        if (generatedCases.isEmpty()) return;
        String dir = "src/test/java/test_cases"; // 这个路径修改了
        new File(dir).mkdirs();
        String file = dir + "/test_cases.json";
        Gson gson = new GsonBuilder().setPrettyPrinting().create();
        try (Writer writer = new FileWriter(file)) {
            gson.toJson(generatedCases, writer);
        }
        System.out.println("✅ Saved " + generatedCases.size() + " test cases to " + file);
    }
}