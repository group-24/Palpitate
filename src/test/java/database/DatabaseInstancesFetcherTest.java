package database;

import matchers.SqlDataTableMatcher;
import org.jmock.Expectations;
import org.jmock.Mockery;
import org.jmock.integration.junit4.JUnit4Mockery;
import org.junit.Test;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.Arrays;
import java.util.HashSet;

import static org.junit.Assert.*;

/**
 * Created by Timotej on 03-Nov-15.
 */
public class DatabaseInstancesFetcherTest {

    RawDataInstancesBuilder dib = new RawDataInstancesBuilder();
    Mockery context = new JUnit4Mockery();

    @Test
    public void testGetBatch() throws Exception {
        final Connection con = context.mock(Connection.class);
        final PreparedStatement stmt = context.mock(PreparedStatement.class);
        final ResultSet rs = context.mock(ResultSet.class);

        final int batchID = 1;
        final int timeslice = 1;

        context.checking(new Expectations(){{
            allowing(con).prepareStatement(with(any(String.class))); will(returnValue(stmt));
            oneOf(stmt).executeQuery(); will(returnValue(rs));
            allowing(rs).next();
            allowing(rs).getInt(with(any(String.class)));
            allowing(rs).getDouble(with(any(String.class)));
            oneOf(stmt).setInt(1, batchID);
            oneOf(stmt).setInt(with(2), with(any(Integer.class)));
            oneOf(stmt).setBoolean(3, true);
            oneOf(stmt).setInt(4, timeslice);
        }});

        dib.withFeature(1).build(con).getBatch(batchID, timeslice);
    }

    @Test
    public void testGetBatchForSubject() throws Exception {
        final Connection con = context.mock(Connection.class);
        final PreparedStatement stmt = context.mock(PreparedStatement.class);
        final ResultSet rs = context.mock(ResultSet.class);

        final int batchID = 1;
        final int subjectID = 1;
        final int timeslice = 1;

        context.checking(new Expectations(){{
            allowing(con).prepareStatement(with(any(String.class))); will(returnValue(stmt));
            oneOf(stmt).executeQuery(); will(returnValue(rs));
            allowing(rs).next();
            allowing(rs).getInt(with(any(String.class)));
            allowing(rs).getDouble(with(any(String.class)));
            oneOf(stmt).setInt(1, batchID);
            oneOf(stmt).setInt(2, subjectID);
            oneOf(stmt).setBoolean(3, false);
            oneOf(stmt).setInt(4, timeslice);
        }});

        dib.withFeature(1).build(con).getBatchForSubject(subjectID, batchID, timeslice);
    }

    @Test
    public void testClose() throws Exception {
        final Connection con = context.mock(Connection.class);
        final PreparedStatement stmt = context.mock(PreparedStatement.class);

        context.checking(new Expectations(){{
            allowing(con).prepareStatement(with(any(String.class))); will(returnValue(stmt));
            oneOf(stmt).close();
        }});

        dib.withFeature(1).build(con).close();
    }
}
