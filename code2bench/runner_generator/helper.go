package main

import (
	"math"
	"reflect"
)

// DeepCompare recursively compares two data structures with a tolerance for floating-point numbers.
func DeepCompare(a, b interface{}, tolerance float64) bool {
	// Handle nil values
	if a == nil || b == nil {
		return a == b
	}

	// Get the reflect.Value of both inputs
	va := reflect.ValueOf(a)
	vb := reflect.ValueOf(b)

	// If types differ, return false
	if va.Type() != vb.Type() {
		return false
	}

	// Compare based on type
	switch va.Kind() {
	case reflect.Float32, reflect.Float64:
		// Compare floats with tolerance
		return math.Abs(va.Float()-vb.Float()) <= tolerance
	case reflect.Map:
		// Compare maps recursively
		if va.Len() != vb.Len() {
			return false
		}
		for _, key := range va.MapKeys() {
			if !vb.MapIndex(key).IsValid() || !DeepCompare(va.MapIndex(key).Interface(), vb.MapIndex(key).Interface(), tolerance) {
				return false
			}
		}
		return true
	case reflect.Slice, reflect.Array:
		// Compare slices/arrays recursively
		if va.Len() != vb.Len() {
			return false
		}
		for i := 0; i < va.Len(); i++ {
			if !DeepCompare(va.Index(i).Interface(), vb.Index(i).Interface(), tolerance) {
				return false
			}
		}
		return true
	case reflect.Struct:
		// Compare structs field by field
		for i := 0; i < va.NumField(); i++ {
			if !DeepCompare(va.Field(i).Interface(), vb.Field(i).Interface(), tolerance) {
				return false
			}
		}
		return true
	default:
		// Use strict equality for other types
		return reflect.DeepEqual(a, b)
	}
}
