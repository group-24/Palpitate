package database;

import matchers.SqlDataTableMatcher;
import org.jmock.Expectations;
import org.jmock.Mockery;
import org.jmock.integration.junit4.JUnit4Mockery;
import org.junit.Test;

import java.sql.Connection;
import java.sql.PreparedStatement;
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
        final Connection con = context.mock(Connection.class);

        context.checking(new Expectations(){{
            oneOf(con).prepareStatement(with(new SqlDataTableMatcher(
                    new HashSet<Integer>(Arrays.asList(1)))));
        }});

        dib.withFeature(1).build(con);

    }


    @Test
    public void canDoMultipleFeatures() throws SQLException {
        final Connection con = context.mock(Connection.class);

        context.checking(new Expectations(){{
            oneOf(con).prepareStatement(with(new SqlDataTableMatcher(
                                    new HashSet<Integer>(Arrays.asList(1, 2, 3, 4)))));

        }});

        dib.withFeature(1).
            withFeature(2).
            withFeature(3).
            withFeature(4).
            build(con);
    }
}
