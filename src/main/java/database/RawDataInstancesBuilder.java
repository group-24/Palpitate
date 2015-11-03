package database;

import utils.RandomString;
import weka.core.Attribute;
import weka.core.FastVector;
import weka.core.Instance;
import weka.core.Instances;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.*;

/**
 * Created by Timotej on 31-Oct-15.
 *
 * This class builds up weka dataset (Instances)
 */
public class RawDataInstancesBuilder implements DataInstancesBuilder<Integer, Integer, Integer> {

    private int batchID = -1;
    private int subjectID = -1;
    private Map<Integer, String> features = new HashMap<Integer, String>();
    private RandomString rndStr = new RandomString((int) Math.ceil(Math.pow(
            features.size(),
            1 / RandomString.alphabetSize())) + 1);

    /**
     REQUIRED tells which features to put into the dataset
     Call multiple times to add more features
     */
    public RawDataInstancesBuilder withFeature(Integer featureID) {
        features.put(featureID, rndStr.nextString());
        return this;
    }


    /*
    This is kind of horrible as we are building large SQL quesries dynamicaly and
    without using PreparedStatements. As far as I see this is the best way to do it
    given this structure of the data.

    An alternative would be to query each feature individualy and then join the coloumnds
    in Java. This would take advantage of PreparedStatements but it would be horrbile for other
    reasons. It would be either slow and memory ineffcient, because we would be holding all
    the data in memory at the same time and then copying it over into Instances. Another option
    would then be to iterate through all the result sets simultaneously, but that would
     mean we would have an ungodly amount of open connections to the database.

     Therefore I conclude this is the best way of doing it. Only possible alternative
     I can think of is to use something like Big Table instead of Postgres.
     */
    public DatabaseInstancesFetcher build(Connection connection) {
        if (features.size() == 0) {
            throw new RuntimeException("builder needs atleast one feature");
        }
        FastVector attributes = new FastVector(features.size() + 1);
        final Attribute subjectIdAttribute = new Attribute("subjectID");
        Map<Integer, Attribute> attributeMap = new HashMap<Integer, Attribute>();
        attributes.addElement(subjectIdAttribute);
        try {
            String fields = "";
            String joins = "";
            String ands = "";
            String currentAlias = "";
            String firstAllias = "";

            for (Map.Entry<Integer, String> feature : features.entrySet()) {
                currentAlias = feature.getValue();
                Attribute a = new Attribute(feature.getKey().toString());
                attributes.addElement(a);
                attributeMap.put(feature.getKey(), a);

                if (firstAllias == "") {
                    firstAllias = currentAlias;
                    fields += currentAlias + ".subjectID";
                    joins += " data as " + currentAlias;
                } else {
                    joins += " JOIN data as " + currentAlias + " USING (subjectID, batchID)";
                }

                fields += ", " + currentAlias + ".featureValue AS " + currentAlias + "fv";

                ands += " AND " + currentAlias + ".featureID = " +  feature.getKey();

            }

            return new DatabaseInstancesFetcher(connection.prepareStatement(
                                    "SELECT " + fields +
                                    " FROM " + joins +
                                    " WHERE " + ands.substring(4) +
                                    //selects the right batch
                                    " AND " + firstAllias + ".batchID = ? AND " +
                                    //enables us to select either a specific subject or all of them
                                    "(" + firstAllias + ".subjectID = ? OR ?) AND " +
                                    firstAllias + ".timeslice = ?"),
                                    attributes,
                                    subjectIdAttribute,
                                    attributeMap,
                                    features
                                    );

        } catch (SQLException e) {
            e.printStackTrace();
            throw new RuntimeException("SQL failed to fetch data");
        }
    }
}
