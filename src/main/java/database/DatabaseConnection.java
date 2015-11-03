package database;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Map;

/**
 * Created by Timotej on 31-Oct-15.
 */
public class DatabaseConnection {
    /*
     Gets the connection to our database. The information about the database is
     stored in enviroment variables for 2 reasons. Firstly to not commit that data
     to git and secondly so we can potentialy easily set up a database for travis.
     It is easy to push encrypted enviroment variables to Travis.
     */
    public static Connection getDatabaseConnection() {
        Connection connection;
        Map<String, String> env = System.getenv();
        if (!env.containsKey("PGHOST") || !env.containsKey("PGPORT") ||
                !env.containsKey("PGDATABASE") || !env.containsKey("PGUSER") ||
                !env.containsKey("PGPASS")) {
            throw new RuntimeException("Cannot get db data from enviroment variables PGHOST, " +
                    "PGPORT, PGDATABASE, PGUSER, PGPASS");
        }

        final String host = env.get("PGHOST");
        final String port = env.get("PGPORT");
        final String database = env.get("PGDATABASE");
        final String username = env.get("PGUSER");
        final String password = env.get("PGPASS");
        try {
            Class.forName("org.postgresql.Driver");
            connection = DriverManager
                    .getConnection("jdbc:postgresql://" + host + ":" + port + "/" + database +
                                    //need this to fix SSL error
                                    "?ssl=true&sslfactory=org.postgresql.ssl.NonValidatingFactory",
                            username, password);
        } catch (SQLException e) {
            throw new RuntimeException("Cannot connect to your database " + database +
                        " user: "  + username);
        } catch (ClassNotFoundException e) {
            throw new RuntimeException("JDBC not setup, build with gradle");
        }
        return connection;
    }
}
