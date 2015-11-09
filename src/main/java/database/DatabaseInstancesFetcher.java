package database;

import weka.core.Attribute;
import weka.core.FastVector;
import weka.core.Instance;
import weka.core.Instances;

import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Map;

/**
 * Created by Timotej on 02-Nov-15.
 */
public class DatabaseInstancesFetcher implements DatabaseDataset<Instances>{
    private final PreparedStatement stmt;
    private final FastVector attributes;
    private final Attribute subjectIdAttribute;
    //Maps feautreID to attributes
    private final Map<Integer, Attribute> attributeMap;
    //Maps feautreID to the alias of the relation from where it's from
    private final Map<Integer, String> features;

    /*
        Should not be constructed on it's own. Use DataInstancesBuilder
    */
    DatabaseInstancesFetcher(PreparedStatement stmt,
                             FastVector attributes,
                             Attribute subjectIdAttribute,
                             Map<Integer, Attribute> attributeMap,
                             Map<Integer, String> features) {
        this.stmt = stmt;
        this.attributes = attributes;
        this.subjectIdAttribute = subjectIdAttribute;
        this.attributeMap = attributeMap;
        this.features = features;
    }


    public Instances getBatch(int batchID, int timeslice){
        try {
            stmt.setInt(1, batchID);
            //don't care about that as we want all of them
            stmt.setInt(2, 2342);
            //we want all the subjects
            stmt.setBoolean(3, true);
            stmt.setInt(4, timeslice);
            ResultSet rs = stmt.executeQuery();
            return resultSetToInstances(rs);

        } catch (SQLException e) {
            e.printStackTrace();
            throw new RuntimeException("SQL failed to fetch data");
        }
    }

    public Instances getBatchForSubject(int subjectID, int batchID, int timeslice) {
        try {
            stmt.setInt(1, batchID);
            //don't care about that as we want all of them
            stmt.setInt(2, subjectID);
            //we want all the subjects
            stmt.setBoolean(3, false);
            stmt.setInt(4, timeslice);
            ResultSet rs = stmt.executeQuery();
            return resultSetToInstances(rs);

        } catch (SQLException e) {
            e.printStackTrace();
            throw new RuntimeException("SQL failed to fetch data");
        }
    }

    public void close() {
        try {
            stmt.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    private Instances resultSetToInstances(ResultSet rs) throws SQLException {
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
        //if BPM (featureID == 1) is one of the attributes, set is as the class
        if (attributeMap.keySet().contains(1)) {
            dataset.setClass(attributeMap.get(1));
        }
        return dataset;
    }
}
