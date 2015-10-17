package ml.compute;

import core.types.HeartRate;

/**
 * Created by mikeecb on 17/10/2015.
 */
public interface HeartRateComputer {

    public HeartRate compute(InputDataVisitable inputDataVisitable);

}
