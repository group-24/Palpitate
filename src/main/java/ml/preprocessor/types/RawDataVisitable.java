package ml.preprocessor.types;

import ml.compute.InputDataVisitable;
import ml.compute.InputDataVisitor;

/**
 * Created by mikeecb on 17/10/2015.
 *
 * Data retrieved from Imperial College Database (audio, visual)
 */
public class RawDataVisitable implements InputDataVisitable {

    public <T> T accept(InputDataVisitor<T> visitor) {
        return visitor.visit(this);
    }

}
