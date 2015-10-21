package data;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Date;
import java.util.Scanner;
import java.util.SortedMap;
import java.util.TreeMap;

/**
 * Created by Timotej on 21-Oct-15.
 */
public class SubjectRawDataBuilder {

    private Integer id;
    private File closeMic;
    private File BPMData;

    public SubjectRawDataBuilder withId(int id) {
        this.id = id;
        return this;
    }

    public SubjectRawDataBuilder withCloseMic(File closeMic) {
        this.closeMic = closeMic;
        return this;
    }

    public SubjectRawDataBuilder withBPMData(File BPMData) {
        this.BPMData = BPMData;
        return this;
    }

    /**
     * This methods finds closeMic file and BPMData files from the subject folder
     * @param subjectDir
     * @return
     */
    public SubjectRawDataBuilder asBCMDir(File subjectDir) {
        for(File f : subjectDir.listFiles()) {
            System.out.println(f.getName());
            if(f.getName().equals("BPM.txt")) {
                BPMData = f;
            }
            else if(f.getName().endsWith("close.wav")) {
                closeMic = f;
            }
        }

        return this;
    }

    private SortedMap<Double,Double> bpmDataParse(File f) throws FileNotFoundException {
        Scanner s = new Scanner(f);
        String[] line;
        SortedMap<Double,Double> bpm = new TreeMap<Double,Double>();
        while(s.hasNextLine()) {
            line = s.nextLine().split("\t");
            assert line[0].equals(line[1]): "the two times differ";
            bpm.put(Double.parseDouble(line[0]), Double.parseDouble(line[2]));
        }

        return bpm;
    }

    public SubjectRawData build(){
        if(id != null &&
           closeMic != null &&
           BPMData != null) {
            try {
                return new SubjectRawData(id, bpmDataParse(BPMData),closeMic);
            } catch (FileNotFoundException f) {
                throw new RuntimeException("Invalid bpm file for subject " + id);
            }

        }

        throw new RuntimeException("Trying to build an incomplete SubjectRawData");
    }
}
