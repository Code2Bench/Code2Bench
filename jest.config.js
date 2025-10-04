export default {
  modulePathIgnorePatterns: [
    "<rootDir>/autocodebench/workspace"
  ],
  preset: 'ts-jest',
  testEnvironment: 'node',
  transform: {
    // 新写法：将 ts-jest 配置直接嵌入
    '^.+\\.ts$': [
      'ts-jest',
      {
        isolatedModules: true, // 避免全局类型检查，减少内存
      },
    ],
    "^.+\\.js$": "babel-jest"
  },
};