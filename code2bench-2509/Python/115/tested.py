def calculate_diff_rate(text1: str, text2: str) -> float:
    # Calculate the Levenshtein edit distance
    def levenshtein_distance(s: str, t: str) -> int:
        m, n = len(s), len(t)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s[i-1] == t[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
        return dp[m][n]

    # Calculate the normalized difference rate
    distance = levenshtein_distance(text1, text2)
    max_length = max(len(text1), len(text2))
    return distance / max_length