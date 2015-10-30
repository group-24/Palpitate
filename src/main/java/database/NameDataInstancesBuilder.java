package database;

import weka.core.Instances;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.HashSet;

/**
 * Created by tk1713 on 02/11/15.
 */
public class NameDataInstancesBuilder implements DataInstancesBuilder<String, Integer, Integer> {

    private final DataInstancesBuilder<Integer, Integer, Integer> builder;
    private final HashSet<String> features = new HashSet<String>();

    public NameDataInstancesBuilder(DataInstancesBuilder<Integer, Integer, Integer> builder) {
        this.builder = builder;
    }

    public NameDataInstancesBuilder forBatch(Integer batchID) {
        builder.forBatch(batchID);
        return this;
    }

    public NameDataInstancesBuilder forSubject(Integer subjectID) {
        builder.forSubject(subjectID);
        return this;
    }

    public NameDataInstancesBuilder withFeature(String featureName) {
        features.add(featureName);
        return this;
    }

    public Instances build(Connection conn) {
        try {
            PreparedStatement stmt = conn.prepareStatement("SELECT featureID, name FROM feature");
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                if (features.contains(rs.getString("name"))) {
                    builder.withFeature(rs.getInt("featureID"));
                }
            }
            stmt.close();
        } catch (SQLException e) {
            e.printStackTrace();
            throw new RuntimeException("SQL failed to fetch data");
        }

        return builder.build(conn);
    }
}
