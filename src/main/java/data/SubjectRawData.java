package data;

import java.io.File;
import java.util.SortedMap;

/**
 * Created by Timotej on 21-Oct-15.
 */
public final class SubjectRawData {
    private final int id;
    private final SortedMap<Double, Double> bpm;
    private final File audioFile;

    SubjectRawData(int id, SortedMap<Double,Double> bpm, File audioFile) {
        this.id = id;
        this.bpm = bpm;
        this.audioFile = audioFile;
    }

    public int getId() {
        return id;
    }

    public SortedMap<Double,Double> getBpm() {
        return bpm;
    }
}
