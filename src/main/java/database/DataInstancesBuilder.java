package database;

import weka.core.Instances;

import java.sql.Connection;
import java.sql.Statement;

/**
 * Created by tk1713 on 02/11/15.
 *  @param <T_batch> type of the batch selection input
 *  @param <T_subject> type of the subject selection input
 *  @param <T_feature> type of the feature selection input
 */
public interface DataInstancesBuilder<T_feature, T_subject, T_batch> {
    DataInstancesBuilder<T_feature, T_subject, T_batch> forBatch(T_batch batch);

    DataInstancesBuilder<T_feature, T_subject, T_batch> forSubject(T_subject subject);

    DataInstancesBuilder<T_feature, T_subject, T_batch> withFeature(T_feature feature);

    Instances build(Connection connection);
}
