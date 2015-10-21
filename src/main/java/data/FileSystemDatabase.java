package data;

import ml.preprocessor.types.RawDataVisitable;

import java.io.File;
import java.io.FilenameFilter;
import java.util.LinkedList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Created by Timotej on 21-Oct-15.
 */
public class FileSystemDatabase extends RawDataVisitable {
    private final String rootPath;
    private final List<SubjectRawData> subjectData = new LinkedList<SubjectRawData>();

    public FileSystemDatabase(String rootPath) {
        this.rootPath = rootPath;
        populateSubjectData();

    }

    private void populateSubjectData() {
        File[] files = new File(rootPath).listFiles();
        Pattern subjectPattern = Pattern.compile("Subject(\\d+)");
        Matcher matcher;
        for (File f : files) {
            matcher  = subjectPattern.matcher(f.getName());
            if (matcher.matches()) {
                subjectData.add(new SubjectRawDataBuilder()
                        .withId(Integer.parseInt(matcher.group(1)))
                        .asBCMDir(f)
                        .build());
            }
        }
    }

    public List<SubjectRawData> getSubjects() {
        return subjectData;
    }
}
