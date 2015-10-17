package ml.compute;

/**
 * Created by mikeecb on 17/10/2015.
 */
public interface InputDataVisitable {

    public <T> T accept(InputDataVisitor<T> visitor);

}
