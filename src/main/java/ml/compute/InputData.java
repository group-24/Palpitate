package ml.compute;

import java.util.Set;

import ml.preprocessor.types.PreprocessedData;
import ml.preprocessor.types.RawData;

/**
 * Created by mikeecb on 17/10/2015.
 */
public class InputData {

    private final Set<PreprocessedData> preprocessedDataSet;
    private final Set<RawData> rawDataSet;

    public InputData(Set<PreprocessedData> preprocessedDataSet, Set<RawData> rawDataSet) {
        this.preprocessedDataSet = preprocessedDataSet;
        this.rawDataSet = rawDataSet;
    }

    public Set<PreprocessedData> getPreprocessedDataSet() {
        return preprocessedDataSet;
    }

    public Set<RawData> getRawDataSet() {
        return rawDataSet;
    }
}
