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
    REQUIRED tells which batch to use
     */
    public RawDataInstancesBuilder forBatch(Integer batchID) {
        this.batchID = batchID;
        return this;
    }

    /**
    OPTIONAL, if used it just gets data for that subject
     */
    public RawDataInstancesBuilder forSubject(Integer subjectID) {
        this.subjectID = subjectID;
        return this;
    }

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
    public Instances build(Connection connection) {
        assert features.size() > 0 : "need atleast one feature";
        FastVector attributes = new FastVector(features.size() + 1);
        final Attribute subjectIdAttribute = new Attribute("subjectID");
        Map<Integer, Attribute> attributeMap = new HashMap<Integer, Attribute>();
        Instances dataset;
        attributes.addElement(subjectIdAttribute);
        try {
            String fields = "";
            String joins = "";
            String ands = "";
            String currentAlias;
            boolean first = true;
            Statement stmt = connection.createStatement();

            for (Map.Entry<Integer, String> feature : features.entrySet()) {
                currentAlias = feature.getValue();
                Attribute a = new Attribute(feature.getKey().toString());
                attributes.addElement(a);
                attributeMap.put(feature.getKey(), a);

                if (first) {
                    first = false;
                    fields += currentAlias + ".subjectID";
                    joins += " data as " + currentAlias;
                } else {
                    joins += " JOIN data as " + currentAlias + " USING (subjectID, batchID)";
                }

                fields += ", " + currentAlias + ".featureValue AS " + currentAlias + "fv";

                ands += " AND " + currentAlias + ".featureID = " +  feature.getKey();

            }
            ResultSet rs = stmt.executeQuery("SELECT " + fields +
                                             " FROM " + joins +
                                             " WHERE " + ands.substring(4) + ";");


            dataset =  resultSetToInstances(attributes, subjectIdAttribute, attributeMap, rs);
            stmt.close();

        } catch (SQLException e) {
            e.printStackTrace();
            throw new RuntimeException("SQL failed to fetch data");
        }
        return dataset;
    }

    private Instances resultSetToInstances(FastVector attributes,
                                           Attribute subjectIdAttribute,
                                           Map<Integer, Attribute> attributeMap,
                                           ResultSet rs) throws SQLException {
        Instances dataset;
        dataset = new Instances("data", attributes, 10);
        Instance inst;
        int numFeatures = attributes.size();
        while (rs.next()) {
            inst = new Instance(numFeatures);
            inst.setValue(subjectIdAttribute, rs.getInt("subjectID"));
            for (Map.Entry<Integer, String> feature : features.entrySet()) {
                inst.setValue(attributeMap.get(feature.getKey()),
                                                rs.getDouble(feature.getValue() + "fv"));
            }

            dataset.add(inst);

        }
        return dataset;
    }
}
