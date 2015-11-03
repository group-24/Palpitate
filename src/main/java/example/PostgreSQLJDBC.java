package example;

import database.NameDataInstancesBuilder;
import database.RawDataInstancesBuilder;
import database.DatabaseConnection;

import java.sql.*;

import java.sql.Connection;
import java.sql.Statement;

/**
 * Created by tlfrd on 29/10/2015.
 */
public class PostgreSQLJDBC {
    public static void main(String args[]) throws SQLException {
        Connection c = null;
        Statement stmt = null;

        c = DatabaseConnection.getDatabaseConnection();
        System.out.println("Opened database successfully");

        stmt = c.createStatement();
        String sql = "SELECT * FROM data WHERE subjectID = 1;";
        ResultSet rs = stmt.executeQuery(sql);
        while (rs.next()) {
            int subjectID = rs.getInt("subjectID");
            double featureValue = rs.getDouble("featureValue");
            System.out.println(subjectID + "\t" + featureValue + "\n");
        }
        stmt.close();

        //test our thing with real database
        RawDataInstancesBuilder dib = new RawDataInstancesBuilder();
        System.out.println( dib.withFeature(1).
                            withFeature(2).
                            withFeature(3).
                            build(c).getBatch(1, 0));

        NameDataInstancesBuilder ndib = new NameDataInstancesBuilder(new RawDataInstancesBuilder());
        System.out.println( ndib.withFeature("f1").
                withFeature("f3").
                withFeature("BPM").
                build(c).getBatch(1, 0));

        c.close();

        System.out.println("Table read successfully");
    }
}
