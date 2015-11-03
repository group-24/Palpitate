package database;

/**
 * Created by Timotej on 02-Nov-15.
 * @param <T> return type in which this dataset should be returned
 */
public interface DatabaseDataset<T> {
    public T getBatch(int batchID, int timeslice);
    public T getBatchForSubject(int subjectID, int batchID, int timeslice);
}
