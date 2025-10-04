def levenshtein_distance(s1: str, s2: str) -> int:
    # Ensure s1 is the shorter string to optimize space
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    
    # Initialize a 2D array for dynamic programming
    dp = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]
    
    # Base case: when the second string is empty
    for i in range(len(s1) + 1):
        dp[i][0] = i
    
    # Fill the first row and column
    for i in range(1, len(s1) + 1):
        dp[0][i] = dp[i-1][i-1] + 1
    
    # Fill the DP table
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1] + 1)
    
    return dp[len(s1)][len(s2)]