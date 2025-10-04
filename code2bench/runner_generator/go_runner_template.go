package main

import (
	"encoding/json"
	"fmt"
	"os"
	"testing"
)

// TestCase represents the structure of our test cases
type TestCase struct {
	Inputs   map[string]interface{} `json:"Inputs"`
	Expected interface{}            `json:"Expected"`
}

func loadTestCases(filePath string) ([]TestCase, error) {
	file, err := os.ReadFile(filePath)
	if err != nil {
		return nil, fmt.Errorf("failed to read test cases: %v", err)
	}

	var testCases []TestCase
	if err := json.Unmarshal(file, &testCases); err != nil {
		return nil, fmt.Errorf("failed to parse test cases: %v", err)
	}

	return testCases, nil
}

func TestGetCorrectIndentLevel(t *testing.T) {
	testCases, err := loadTestCases("test_cases/test_cases.json")
	if err != nil {
		t.Fatalf("Failed to load test cases: %v", err)
	}

	for i, tc := range testCases {
		t.Run(fmt.Sprintf("Case%d", i), func(t *testing.T) {
			// Call the function under test
			actual := _get_correct_indent_level_wrapper(tc.Inputs)

			// Compare with expected result using DeepCompare
			if !DeepCompare(actual, tc.Expected, 1e-6) {
				t.Errorf(
					`Test case %d failed:
Input:    %v
Expected: %v
Actual:   %v
`, i, tc.Inputs, tc.Expected, actual)
			}
		})
	}
}
