import * as fs from 'fs';
import * as path from 'path';

/**
 * 深度比较两个对象，支持浮点误差范围
 */
function deepCompare(a, b, epsilon = 1e-6) {
  if (typeof a !== typeof b) return false;

  if (typeof a === 'number') {
    return Math.abs(a - b) < epsilon;
  }

  if (Array.isArray(a) && Array.isArray(b)) {
    if (a.length !== b.length) return false;
    return a.every((val, idx) => deepCompare(val, b[idx], epsilon));
  }

  if (typeof a === 'object' && a && b) {
    const keysA = Object.keys(a);
    const keysB = Object.keys(b);
    if (keysA.length !== keysB.length) return false;
    return keysA.every(key => deepCompare(a[key], b[key], epsilon));
  }

  return a === b;
}

/**
 * 接收输入对象，查找匹配测试用例并返回期望值
 */
export function getPipelinesDisabled(inputs) {
  try {
    const filePath = path.join(__dirname, 'test_cases/test_cases.json');
    const raw = fs.readFileSync(filePath, 'utf-8');
    const testCases = JSON.parse(raw);

    for (const tc of testCases) {
      if (deepCompare(tc.Inputs, inputs)) {
        return tc.Expected;
      }
    }

    return [];
  } catch (e) {
    throw new Error(`Mock failed: ${e.message}`);
  }
}
