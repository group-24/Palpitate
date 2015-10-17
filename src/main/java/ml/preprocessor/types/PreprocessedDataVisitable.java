package ml.preprocessor.types;

import ml.compute.InputDataVisitable;
import ml.compute.InputDataVisitor;

/**
 * Created by mikeecb on 17/10/2015.
 *
 * Preprocessed data produced by openSMILE
 */
public class PreprocessedDataVisitable implements InputDataVisitable {

    public <T> T accept(InputDataVisitor<T> visitor) {
        return visitor.visit(this);
    }

}
