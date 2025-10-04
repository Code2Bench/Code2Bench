package main

import (
	"fmt"
	"go/ast"
	"go/parser"
	"go/token"
	"io/ioutil"
	"os"
	"path/filepath"
	"regexp"
	"sort"
	"strconv"
	"strings"
)

var basicTypes = map[string]bool{
	"bool": true, "string": true,
	"int": true, "int8": true, "int16": true, "int32": true, "int64": true,
	"uint": true, "uint8": true, "uint16": true, "uint32": true, "uint64": true,
	"float32": true, "float64": true,
	"byte": true, "rune": true, "error": true,
}

type TypeCheckResult struct {
	HasNonBasicTypes bool
	NonBasicTypes    []string
}

// 提取并检查文件中的函数签名
func CheckFileForNonBasicTypes(fileContent string) (TypeCheckResult, string, error) {
	result := TypeCheckResult{
		NonBasicTypes: []string{},
	}

	// 首先尝试提取函数签名
	fset := token.NewFileSet()
	file, err := parser.ParseFile(fset, "", fileContent, parser.ParseComments)
	if err != nil {
		return result, "", fmt.Errorf("Error parsing file: %v", err)
	}

	// 查找函数声明
	for _, decl := range file.Decls {
		if fn, ok := decl.(*ast.FuncDecl); ok {
			signature := funcDeclToString(fn)

			// 检查非基本类型
			result = checkSignatureTypes(fn.Type, signature)
			return result, signature, nil
		}
	}

	// 如果没有找到函数声明，尝试正则表达式提取签名
	re := regexp.MustCompile(`func\s+[\w_]+\s*\([^)]*\)\s*(?:\w+|(?:\([^)]*\)))`)
	match := re.FindString(fileContent)

	if match != "" {
		// 使用HasNonBasicTypes函数分析提取的签名
		result = HasNonBasicTypes(match)
		return result, match, nil
	}

	return result, "", fmt.Errorf("No function declaration found")
}

func HasNonBasicTypes(funcSig string) TypeCheckResult {
	fset := token.NewFileSet()
	result := TypeCheckResult{
		NonBasicTypes: []string{},
	}

	// 尝试解析为完整文件
	file, err := parser.ParseFile(fset, "", "package p\n"+funcSig, parser.ParseComments)
	if err == nil {
		// 如果解析成功，提取函数签名并检查
		for _, decl := range file.Decls {
			if fn, ok := decl.(*ast.FuncDecl); ok {
				sig := funcDeclToString(fn)
				return checkSignatureTypes(fn.Type, sig)
			}
		}
	}

	// 如果文件解析失败，尝试作为表达式解析
	expr, err := parser.ParseExprFrom(fset, "", "package p; var _ = "+funcSig, 0)
	if err != nil {
		result.HasNonBasicTypes = true
		result.NonBasicTypes = append(result.NonBasicTypes, "PARSE_ERROR: "+err.Error())
		return result
	}

	callExpr, ok := expr.(*ast.CallExpr)
	if !ok {
		result.HasNonBasicTypes = true
		result.NonBasicTypes = append(result.NonBasicTypes, "INVALID_SIGNATURE")
		return result
	}

	funcLit, ok := callExpr.Fun.(*ast.FuncLit)
	if !ok {
		result.HasNonBasicTypes = true
		result.NonBasicTypes = append(result.NonBasicTypes, "INVALID_SIGNATURE")
		return result
	}

	return checkSignatureTypes(funcLit.Type, funcSig)
}

func checkSignatureTypes(ft *ast.FuncType, sig string) TypeCheckResult {
	result := TypeCheckResult{
		NonBasicTypes: []string{},
	}

	// 检查参数
	if ft.Params != nil {
		for _, field := range ft.Params.List {
			checkType(field.Type, &result)
		}
	}

	// 检查返回值
	if ft.Results != nil {
		for _, field := range ft.Results.List {
			checkType(field.Type, &result)
		}
	}

	result.HasNonBasicTypes = len(result.NonBasicTypes) > 0
	return result
}

func checkType(expr ast.Expr, result *TypeCheckResult) {
	switch t := expr.(type) {
	case *ast.Ident:
		if !basicTypes[t.Name] {
			result.NonBasicTypes = appendUnique(result.NonBasicTypes, t.Name)
		}

	case *ast.StarExpr:
		checkType(t.X, result)

	case *ast.ArrayType:
		checkType(t.Elt, result)

	case *ast.MapType:
		checkType(t.Key, result)
		checkType(t.Value, result)

	case *ast.ChanType:
		checkType(t.Value, result)

	case *ast.StructType, *ast.InterfaceType, *ast.FuncType:
		typeStr := typeToString(t)
		result.NonBasicTypes = appendUnique(result.NonBasicTypes, typeStr)

	case *ast.SelectorExpr:
		typeStr := typeToString(t)
		result.NonBasicTypes = appendUnique(result.NonBasicTypes, typeStr)

	case *ast.Ellipsis:
		checkType(t.Elt, result)

	default:
		typeStr := fmt.Sprintf("%T", t)
		result.NonBasicTypes = appendUnique(result.NonBasicTypes, typeStr)
	}
}

func appendUnique(slice []string, item string) []string {
	for _, s := range slice {
		if s == item {
			return slice
		}
	}
	return append(slice, item)
}

func funcDeclToString(fn *ast.FuncDecl) string {
	var buf strings.Builder

	buf.WriteString("func ")
	if fn.Recv != nil {
		buf.WriteString("(")
		for i, field := range fn.Recv.List {
			if i > 0 {
				buf.WriteString(", ")
			}
			for j, name := range field.Names {
				if j > 0 {
					buf.WriteString(", ")
				}
				buf.WriteString(name.Name)
			}
			if len(field.Names) > 0 {
				buf.WriteString(" ")
			}
			buf.WriteString(typeToString(field.Type))
		}
		buf.WriteString(") ")
	}
	buf.WriteString(fn.Name.Name)

	buf.WriteString("(")
	if fn.Type.Params != nil {
		for i, field := range fn.Type.Params.List {
			if i > 0 {
				buf.WriteString(", ")
			}
			for j, name := range field.Names {
				if j > 0 {
					buf.WriteString(", ")
				}
				buf.WriteString(name.Name)
			}
			if len(field.Names) > 0 {
				buf.WriteString(" ")
			}
			buf.WriteString(typeToString(field.Type))
		}
	}
	buf.WriteString(")")

	if fn.Type.Results != nil {
		if len(fn.Type.Results.List) == 1 && fn.Type.Results.List[0].Names == nil {
			buf.WriteString(" ")
			buf.WriteString(typeToString(fn.Type.Results.List[0].Type))
		} else {
			buf.WriteString(" (")
			for i, field := range fn.Type.Results.List {
				if i > 0 {
					buf.WriteString(", ")
				}
				for j, name := range field.Names {
					if j > 0 {
						buf.WriteString(", ")
					}
					buf.WriteString(name.Name)
				}
				if len(field.Names) > 0 {
					buf.WriteString(" ")
				}
				buf.WriteString(typeToString(field.Type))
			}
			buf.WriteString(")")
		}
	}

	return buf.String()
}

func typeToString(expr ast.Expr) string {
	switch t := expr.(type) {
	case *ast.Ident:
		return t.Name
	case *ast.StarExpr:
		return "*" + typeToString(t.X)
	case *ast.ArrayType:
		if t.Len == nil {
			return "[]" + typeToString(t.Elt)
		}
		return "[" + typeToString(t.Len) + "]" + typeToString(t.Elt)
	case *ast.MapType:
		return "map[" + typeToString(t.Key) + "]" + typeToString(t.Value)
	case *ast.ChanType:
		var prefix string
		switch t.Dir {
		case ast.SEND:
			prefix = "chan<- "
		case ast.RECV:
			prefix = "<-chan "
		default:
			prefix = "chan "
		}
		return prefix + typeToString(t.Value)
	case *ast.StructType:
		return "struct{...}"
	case *ast.InterfaceType:
		return "interface{...}"
	case *ast.FuncType:
		return "func(...)"
	case *ast.SelectorExpr:
		return typeToString(t.X) + "." + t.Sel.Name
	case *ast.Ellipsis:
		return "..." + typeToString(t.Elt)
	default:
		return fmt.Sprintf("%T", t)
	}
}

// 检查目录下的所有数字文件夹
func CheckBenchmarkDirs(basePath string, outputFile string) error {
	// 准备输出文件
	file, err := os.Create(outputFile)
	if err != nil {
		return fmt.Errorf("Error creating output file: %v", err)
	}
	defer file.Close()

	// 写入标题
	file.WriteString("# Go Benchmark 自定义类型检查结果\n\n")
	file.WriteString("| 文件夹编号 | 函数签名 | 自定义类型 |\n")
	file.WriteString("|------------|----------|------------|\n")

	// 读取目录
	entries, err := ioutil.ReadDir(basePath)
	if err != nil {
		return fmt.Errorf("Error reading directory: %v", err)
	}

	// 过滤并排序数字文件夹
	var numericDirs []int
	for _, entry := range entries {
		if entry.IsDir() {
			if id, err := strconv.Atoi(entry.Name()); err == nil {
				numericDirs = append(numericDirs, id)
			}
		}
	}
	sort.Ints(numericDirs)

	// 遍历每个数字文件夹
	count := 0
	for _, id := range numericDirs {
		dirName := strconv.Itoa(id)
		dirPath := filepath.Join(basePath, dirName)
		instructionPath := filepath.Join(dirPath, "instruction.txt")

		// 检查instruction.txt是否存在
		if _, err := os.Stat(instructionPath); os.IsNotExist(err) {
			fmt.Printf("Warning: No instruction.txt in folder %s\n", dirName)
			continue
		}

		// 读取instruction.txt
		instructionContent, err := ioutil.ReadFile(instructionPath)
		if err != nil {
			fmt.Printf("Error reading instruction.txt in folder %s: %v\n", dirName, err)
			continue
		}

		// 检查非基本类型
		result, signature, err := CheckFileForNonBasicTypes(string(instructionContent))
		if err != nil {
			fmt.Printf("Error checking types in folder %s: %v\n", dirName, err)
			continue
		}

		// 如果有非基本类型，记录到文件
		if result.HasNonBasicTypes {
			count++

			// 格式化签名，移除换行符
			cleanSignature := strings.ReplaceAll(signature, "\n", " ")

			// 格式化自定义类型列表
			typesList := strings.Join(result.NonBasicTypes, ", ")

			// 写入到表格
			line := fmt.Sprintf("| %s | `%s` | %s |\n", dirName, cleanSignature, typesList)
			file.WriteString(line)

			fmt.Printf("Folder %s: Found non-basic types: %v\n", dirName, result.NonBasicTypes)
		}
	}

	// 写入统计信息
	file.WriteString(fmt.Sprintf("\n共发现 %d 个包含自定义类型的基准测试。\n", count))
	fmt.Printf("Total folders with non-basic types: %d\n", count)
	fmt.Printf("Results written to %s\n", outputFile)

	return nil
}

func main() {
	basePath := ""
	outputFile := "go_custom_types.md"

	if err := CheckBenchmarkDirs(basePath, outputFile); err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}
}
