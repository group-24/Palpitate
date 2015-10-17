package ml.preprocessor;

import ml.preprocessor.types.PreprocessedData;

/**
 * Created by mikeecb on 17/10/2015.
 *
 * Data Access Object Interface used to read preprocessed data (ie. from a CSV file) produced by
 * openSMILE
 */
public interface PreprocessedDataDAO {

    public PreprocessedData getPreProcessedData();

}
