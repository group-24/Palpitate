package ml.compute;

import ml.preprocessor.types.PreprocessedDataVisitable;
import ml.preprocessor.types.RawDataVisitable;

/**
 * Created by mikeecb on 17/10/2015.
 *
 * @param <T> is the type of data that the visitor will return and will be passed to a
 *           implementation of HeartRateComputer
 */
public interface InputDataVisitor<T> {

    public T visit(PreprocessedDataVisitable data);

    public T visit(RawDataVisitable data);

}
