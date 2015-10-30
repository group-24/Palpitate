package database;

import matchers.SqlDataTableMatcher;
import org.jmock.Expectations;
import org.jmock.Mockery;
import org.jmock.integration.junit4.JUnit4Mockery;
import org.junit.Test;

import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Arrays;
import java.util.HashSet;

/**
 * Created by Timotej on 31-Oct-15.
 */
public class RawDataInstancesBuilderTest {


    RawDataInstancesBuilder dib = new RawDataInstancesBuilder();
    Mockery context = new JUnit4Mockery();


    @Test
    public void canDoOneFeature() throws SQLException {
        final Statement stmt = context.mock(Statement.class);
        final Connection con = context.mock(Connection.class);

        context.checking(new Expectations(){{
            oneOf(stmt).executeQuery(with(new SqlDataTableMatcher(
                                                new HashSet<Integer>(Arrays.asList(1)))));
            oneOf(con).createStatement(); will(returnValue(stmt));
            allowing(stmt).close();
        }});

        dib.withFeature(1).forBatch(1).build(con);

    }


    @Test
    public void canDoMultipleFeatures() throws SQLException {
        final Statement stmt = context.mock(Statement.class);
        final Connection con = context.mock(Connection.class);

        context.checking(new Expectations(){{
            oneOf(stmt).executeQuery(with(new SqlDataTableMatcher(
                                    new HashSet<Integer>(Arrays.asList(1, 2, 3, 4)))));
            oneOf(con).createStatement(); will(returnValue(stmt));
            allowing(stmt).close();
        }});

        dib.withFeature(1).
            withFeature(2).
            withFeature(3).
            withFeature(4).
            forBatch(1).
            build(con);

    }
}
