package p177;

import java.util.Objects;

public class Tested {
    /**
     * Appends JDBC credentials (username and password) to the provided JDBC URL. If the password is
     * null, only the username is included in the credentials. The credentials are appended as query
     * parameters, prefixed with "&" if the URL already contains a query string, or "?" otherwise.
     *
     * <p>For example:
     * <pre>{@code
     * setJDBCCredentials("jdbc:mysql://localhost:3306/mydb", "admin", "secret")
     * // Returns "jdbc:mysql://localhost:3306/mydb?user=admin&password=secret"
     *
     * setJDBCCredentials("jdbc:mysql://localhost:3306/mydb?useSSL=true", "admin", "secret")
     * // Returns "jdbc:mysql://localhost:3306/mydb?useSSL=true&user=admin&password=secret"
     *
     * setJDBCCredentials("jdbc:mysql://localhost:3306/mydb", "admin", null)
     * // Returns "jdbc:mysql://localhost:3306/mydb?user=admin"
     * }</pre>
     *
     * @param jdbcURL the JDBC URL to which credentials will be appended. Must not be null.
     * @param username the username to include in the credentials. Must not be null.
     * @param password the password to include in the credentials. May be null.
     * @return the JDBC URL with the appended credentials.
     * @throws NullPointerException if {@code jdbcURL} or {@code username} is null.
     */
    public static String setJDBCCredentials(String jdbcURL, String username, String password) {
        // TODO: implement this method
    }
}